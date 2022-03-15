# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from .models import Catalog
from django.views import View

# Create your views here.

class ListingIndex(View):
    def get(self, request, page_title):

        order_by = request.GET.get('order')
        if (order_by is not None and 
            order_by!=''):
            options = { 0 : '-prop__price',
                        1 : 'prop__price',
                        2 : '-prop__lot_size',
                        3 : 'prop__lot_size',
                        4 : '-prop__listed_date',
                        5 : 'prop__listed_date',
            }
            order_by = options[int(order_by)]
        else:
            order_by = 'prop__listed_date'  

        """
        The methods for pagination
         """
        result_list = get_object_or_404(Catalog, pk=page_title)
        page_title = result_list.name

        result_list = result_list.items.all().order_by(order_by)
      
        page = request.GET.get('page', 1)
        paginator = Paginator(result_list, 10)

        try:
            result_list = paginator.page(page)
        except PageNotAnInteger:
            result_list = paginator.page(1)
        except EmptyPage:
            result_list = paginator.page(paginator.num_pages)
       

        return render (request, 'realestate/catalog.html', 
            {
            'result_list': result_list,
            'page_title': page_title
            }
        )
