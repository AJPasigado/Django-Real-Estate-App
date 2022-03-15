from __future__ import absolute_import, unicode_literals

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render
from django.views import View


from wagtail.core.models import Page
from wagtail.search.backends import get_search_backend
from apps.realestate.models import Listing, ListingType


class Search(View):
    def get(self, request):

        """
        The backend of the search functionality of this project is powered by Elastic Search
        This is stated in WAGTAILSEARCH_BACKENDS of the common.py

        The search functionality is divided into three parts
        1. Getting the values of the GET request
        2. Filtering and Searching
        3. Pagination
        4. Return Result

        ======================================================================================

        1. Getting the values of the GET request
        They are stored in a dictionary so they can be fed in the filter

        price_min --> The minimum value for price range
        price_max --> The maximum value for price range
        lotsize_min --> The minimum value for lot size range
        lotsize_max --> The maximum value for lit size range
        bedrooms --> The number of bedrooms to be filtered (5+: More than 5, Any: Any value)
        bathrooms --> The number of bathrooms to be filtered (5+: More than 5, Any: Any value)

        Addresses:
            address_city --> The city where the listing is located
            address_state --> The state where the listing is located
            address_country --> The country where the listing is located
            address_zip --> The zip where the listing is located
        
        property_type -->   Filter for the type of lisitng. The integer passed in to this is the ID of the
                            type in the database
        purchase_mode -->   The mode of purchasing of the lisitng. (0: For Sale; 1: For Rent)
        
        order_by --> Used in the sorting mechanism
            0: Price: Highest to Lowest
            1: Price: Lowest to Highest
            2: Lot Size: Ascending
            3: Lot Size: Descending
            4: Most Recent
            5: Oldest First
            --> To add a new sorting, include it in the template and add an entry in the 'options' variable

        page --> Get the current page number of the result
        
        """

        m = dict()

        price_min = request.GET.get('price_min', None)
        if (price_min is not None and 
            price_min != ''):
            m['price__gte'] = float(price_min)

        price_max = request.GET.get('price_max', None)
        if (price_max is not None and 
            price_max != ''):
            m['price__lte'] = float(price_max)

        lotsize_min = request.GET.get('lotsize_min', None)
        if (lotsize_min is not None and 
            lotsize_min != ''):
            m['lot_size__gte'] = float(lotsize_min)

        lotsize_max = request.GET.get('lotsize_max', None)
        if (lotsize_max is not None and 
            lotsize_max != ''):
            m['lot_size__lte'] = float(lotsize_max)

        bedrooms = request.GET.get('bedrooms')
        if  bedrooms == "5+":
            m['num_beds__gte'] = 5
        elif   (bedrooms is not None and 
                bedrooms != ''):
            m['num_beds__iexact'] = int(bedrooms)

        bathrooms = request.GET.get('bathrooms')
        if  bedrooms == "5+":
            m['num_baths__gte'] = 5
        elif   (bathrooms is not None and 
                bathrooms != ''):
            m['num_baths__iexact'] = int(bathrooms)

        property_type = request.GET.get('type')
        if (property_type is not None and 
            property_type!=''):
            m['property_type__id__iexact'] = int(property_type)

        purchase_mode = request.GET.get('options')
        if (purchase_mode is not None and 
            purchase_mode!='' and purchase_mode != 'Any'):
            m['purchase_mode'] = int(purchase_mode)

        address = request.GET.get('address')
        if (address is None):
            address = " "

        order_by = request.GET.get('order')
        if (order_by is not None and 
            order_by!=''):
            options = { 0 : '-price',
                        1 : 'price',
                        2 : '-lot_size',
                        3 : 'lot_size',
                        4 : '-listed_date',
                        5 : 'listed_date',
            }
            order_by = options[int(order_by)]
        else:
            order_by = '-listed_date'        

        """
        2. Filtering and Searching
        Since the project is using a custom model for the Listings, get_search_backend() is utilized.
        This function gets the the elastic search backend and uses the search() function to query.

        elastic_search --> stores the elastic search backend functionality
        search_results --> stores the query result
            > operator: tells elastic search to take account all of the query. ("and" | "or")
        
        (address_city + address_state + address_country).strip() is not "" --> If the user did not input any query, there
        is no need to run Elastic Search

        """

        if (address).strip() is not "":
            elastic_search = get_search_backend()
            search_results = elastic_search.search("%s" % (address), Listing.objects.filter(**m).order_by(order_by), order_by_relevance=False, operator="and")
        else:
            search_results = Listing.objects.filter(**m).order_by(order_by)

        """
        3. Pagination
        This section provides the pagination for the search result.
        This uses the default Paginator of Django

        num_results --> Used to store the total number of results before being cut down by the paginator

        """
        
        num_results = len(search_results)
        page = request.GET.get('page', 1)
        paginator = Paginator(search_results, 10)

        try:
            search_results = paginator.page(page)
        except PageNotAnInteger:
            search_results = paginator.page(1)
        except EmptyPage:
            search_results = paginator.page(paginator.num_pages)

        """
        3. Return Result
        search_results --> Passes the result of the query
        num_results --> Passes the number of results
        request_params --> Passes the queries
        listing_types --> Passes the List Types to be used in the Search Filters
        
        """
        
        return render (request, 'search/search.html', 
                        {
                        'search_results': search_results,
                        'num_results': num_results,
                        'request_params': dict(request.GET),
                        'listing_types': ListingType.objects.all
                        }
        )
