
from __future__ import unicode_literals

from django.db import models
from django.db.models import (
    IntegerField, 
    CharField, 
    DecimalField, 
    ImageField, 
    DateField, 
    ForeignKey, 
    OneToOneField, 
    ManyToManyField, 
    BooleanField,
)
from django.template.defaultfilters import slugify

from modelcluster.fields import ParentalKey

from wagtail.admin.edit_handlers import (
    FieldPanel, InlinePanel, MultiFieldPanel,
)
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from django.template.defaultfilters import slugify

from wagtail.search import index

class ListingIndex(Page):
    """The ListingIndex page is the parent page of Listings. It serves as a
    container for all property listings. To add a listing to the listing index,
    create a listing subpage.
    """
    subpage_types = ('realestate.Listing',)
    description = CharField(max_length=250, blank=True)
    content_panels = Page.content_panels + [
        FieldPanel('description')
    ]


class Listing(Page, index.Indexed):
    """The Listing page represents property listings in the real estate web
    app.
    """
    def __init__(self, *args, **kwargs):
        super(Listing, self).__init__(*args, **kwargs)
    
    description = RichTextField()
    
    # Locations
    address_lotnumber = CharField(max_length=10)
    address_street = CharField(max_length=20)
    address_city = CharField(max_length=20)
    address_state = CharField(max_length=20)
    address_country = CharField(max_length=20)
    address_zip = IntegerField()

    """The location property is the complete address string of a property
    listing.
    """
    @property
    def location(self):
        return "%s %s %s %s %s %s" % (
            self.address_lotnumber,
            self.address_street,
            self.address_city,
            self.address_state,
            self.address_country,
            self.address_zip
        )

    _MODE = (
        (0, 'Sale'),
        (1, 'Rent')
    )
    purchase_mode = models.IntegerField(choices=_MODE)
    property_type = ForeignKey('realestate.ListingType', on_delete=models.PROTECT)
    price = DecimalField(max_digits=20, decimal_places=2)
    num_baths = IntegerField()
    num_beds = IntegerField()
    lot_size = DecimalField(max_digits=20, decimal_places=3)
    floor_area = DecimalField(max_digits=20, decimal_places=3)
    listed_date = DateField(verbose_name="Listed Date", name="listed_date")
    fully_furnished = BooleanField()
    build_year = IntegerField()
    content_panels =  [
        FieldPanel('description'),
        FieldPanel('purchase_mode'),
        FieldPanel('property_type'),
        FieldPanel('price'),
        InlinePanel("brokers", label="Broker"),
        MultiFieldPanel(
            [
                FieldPanel("address_lotnumber"),
                FieldPanel("address_street"),
                FieldPanel("address_city"),
                FieldPanel("address_state"),
                FieldPanel("address_country"),
                FieldPanel("address_zip"),
            ],
            heading="Address",
            classname="collapsible"
        ),
        MultiFieldPanel(
            [
                FieldPanel('num_baths'),
                FieldPanel('num_beds'),
                FieldPanel('lot_size'),
                FieldPanel('floor_area'),
                
                FieldPanel('fully_furnished'),
                FieldPanel('build_year'),
            ],
            heading="Property Details",
            classname="collapsible"
        ),
        InlinePanel('features', label='User defined details'),
        InlinePanel('image', label='Images'),
        InlinePanel('similarListing', label='Similar Properties'),
        FieldPanel('listed_date'),
        
    ]
    promote_panels = []

    def save(self, *args, **kwargs):
        """On save, the title of the listing page is set as the location plus
        the purchase mode (e.g. "12 Beach Drive - For Sale), and the slug is 
        automatically set.
        """
        self.title = "%s - For %s" % (
            self.location,
            'Rent' if self.purchase_mode == 1 else "Sale"
        )
        self.slug = slugify(self.location)

        """A newly created property will always go to either of the two 
        default catalogs (For Rent or For Sale), so make sure that these two
        pages are set-up before a property will be added.
        """
        cat = None
        try:
            if self.purchase_mode == 0: # if purchase mode is sale.
                cat = Catalog.objects.all().filter(name__iexact="For Sale")[0]                
            else:
                cat = Catalog.objects.all().filter(name__iexact="For Sale")[0]                
        except:
            throw ( # Throw exception if the default pages are not set-up.
                "Catalog not found. Please make sure that Catalogs with " +
                "name \"For Sale\" and \"For Rent\" exist."
            )

        try:
            CatalogItem.objects.create( # create a new catalogitem object
                prop = self,
                pr2 = cat
            )
        except:
            pass
        super(Listing, self).save(*args, **kwargs)
    
    """search_fields
    This variable is used to tell Wagtail to index the fields that are needed 
    for ElasticSearch
        >   Search Field, in this context, is used to index the address. The 
            first parameter passed is the
            name of the field to be indexed and partial_math tells 
            ElasticSearch to enable partial match.
        >   FilterField is used to index the filters needed for the search
    """
    search_fields = [
        index.SearchField('address_city', partial_match=True),
        index.SearchField('address_state', partial_match=True),
        index.SearchField('address_country', partial_match=True),
        index.FilterField('address_zip'),
        index.FilterField('purchase_mode'),
        index.FilterField('property_type'),
        index.FilterField('price'),
        index.FilterField('listed_date'),
        index.FilterField('num_baths'),
        index.FilterField('num_beds'),
        index.FilterField('lot_size'),
    ]

    def __str__():
        return self.title


class ListingBroker(models.Model):
    """The ListingBroker model is an intermediary model to connect a listing to
    a broker.
    """
    prop = ParentalKey('realestate.Listing', related_name="brokers")
    broker = ForeignKey('realestate.Broker', on_delete=models.PROTECT)


class ListingTypeIndex(Page):
    """The ListingType index is a container page for property types. You can 
    add more property types (e.g. Condo, House and Lot) by editing ListingIndex
    page.
    """
    content_panels = [
        InlinePanel('listing_types', label="Listing Types")
    ]
    promote_panels = []
    def save(self, *args, **kwargs):
        self.title = "Listing Type Index"
        self.slug = "list-type-index"
        super(ListingTypeIndex, self).save(*args, **kwargs)


class ListingType(models.Model):
    """The ListingType is a model for representing the different types of pro-
    perties (e.g Condo, House and Lot). You can add more types by editing the 
    ListingIndex page.
    """
    p = ParentalKey(
        ListingTypeIndex, 
        on_delete=models.PROTECT, 
        related_name='listing_types'
    )
    name = CharField(
        max_length=30, 
        unique=True
    )
    content_panels = [
            FieldPanel('name'),
        ]
    def save(self, *args, **kwargs):
        self.title = self.name
        super(ListingType, self).save(*args, **kwargs)
    def __str__(self):
        return self.name


class SimilarListings(models.Model):
    """The SimilarListings model is the intermediary model for connecting a 
    lisitng with its similar listings/properties.
    """
    fkey = ParentalKey(Listing, related_name='similarListing')
    prop = ParentalKey(Listing, unique=False)
    class Meta: # similar properties cannot appear twice in a single listing
        unique_together = ('fkey', 'prop',)


class ListingFeature(models.Model):
    """The ListingFeature model represents the customizable/addable features of 
    a property (e.g. Jacuzzi, Hot&Cold Shower). To add Listing Features, see 
    the Edit Listing interface.
    """
    prop = ParentalKey(Listing, related_name='features')
    value = CharField(max_length=50)


class ListingImage(models.Model):
    """Foreign key to image for a single Listing.
    """
    pr2 = ParentalKey(Listing, related_name='image')
    image = ImageField(upload_to='uploads/%Y/%m/%d/')
    description = CharField(max_length=250, blank=True)
    content_panels = [
        FieldPanel('image'),
        FieldPanel('description')
    ]


class CatalogItem(models.Model):
    """CatalogItem is an intermediary model for connecting a Listing to a 
    Catalog. This is necessary, because a listing can appear in more than one 
    catalog. 
    """
    pr2 = ParentalKey('realestate.Catalog', related_name='items')
    prop = ForeignKey(Listing, db_column="fk_propertyid", on_delete=models.CASCADE)
    class Meta: # A property can only appear once in a specific catalog.
        unique_together = ['pr2', 'prop']

    @property
    def catalog_name(self):
        return self.pr2.name
    def __str__(self):
        return "%s: %s" % (self.catalog_name, self.prop.location)
    

class Catalog(Page):
    """The catalog page has foreign keys to the CatalogItem objects that are
    associated with that catalog. It also has foreign keys to FeaturedItem 
    objects, which is what the Catalog will display as "Featured Item" in the 
    catalog previews.
    """
    name = CharField(max_length=20)
    description = CharField(max_length=250, blank=True)
    content_panels = [
        FieldPanel('name'),
        FieldPanel('description'),
        InlinePanel('items', label='Listings'),
        InlinePanel('featured', label='Featured Items')
    ]
    promote_panels = []
    def save(self, *args, **kwargs):
        self.title = self.name
        self.slug = slugify(self.name)
        super(Catalog, self).save(*args, **kwargs)


class FeaturedItem(models.Model):
    """This class represents a featured item in a specific catalog. It is an 
    intermediary model to connect CatalogItem objects and Catalog objects.
    """
    fkey = ParentalKey(
        Catalog, related_name='featured', 
        verbose_name='Featured For Sale',
        )
    prop = models.ForeignKey(
        CatalogItem,
        on_delete=models.CASCADE
        )


class CatalogIndex(Page):
    """Container for catalogs
    """
    subpage_types = ['Catalog']


class BrokerIndex(Page):
    """A container page for brokers.
    """
    subpage_types = ('realestate.Broker',)


class Broker(Page):
    """Represents a broker in the app. It has a one-to-one relationship with 
    picture and brokeragency, and a one-to-many relation with contact.
    """
    name = CharField(max_length=50, blank=True)
    location_city = CharField(max_length=50, blank=True)
    location_state = CharField(max_length=50, blank=True)
    location_country = CharField(max_length=50, blank=True)
    picture = ImageField(upload_to='uploads/broker/images', blank=True)
    agency = ForeignKey('realestate.BrokerAgency', on_delete=models.PROTECT, blank=True)
    content_panels =  [
        FieldPanel('name'),
        MultiFieldPanel(
            [
                FieldPanel('location_city'),
                FieldPanel('location_state'),
                FieldPanel('location_country'),
            ],
            heading="Location",
            classname="collapsible"
        ),
        FieldPanel('picture'),
        InlinePanel(
            'contact',
            label='Contact'
        ),
        FieldPanel('agency'),
    ]

    def save(self, *args, **kwargs):
        promote_panels = []
        self.title = "%s - %s" % (
            self.name,
            self.agency
        )
        self.slug = slugify(self.title)
        super(Broker, self).save(*args, **kwargs)


class BrokerContact(models.Model):
    """Used to represent a contact detail of a single broker.
    """
    fkey = ParentalKey(
        Broker, related_name='contact', 
        verbose_name='Contact Numbers',
    )
    _MODE = (
        (0, 'Email'),
        (1, 'Phone'),
        (2, 'Telephone'),
    )
    contact_type = models.IntegerField(choices=_MODE)
    contact = CharField(max_length=50)


class BrokerAgencyIndex(Page):
    """Container model for BrokerAgency models.
    """
    content_panels = Page.content_panels + [
        InlinePanel(
            "agencies", 
            label="Agencies"
        )
    ]


class BrokerAgency(models.Model):
    """Represents a broker agency. One broker can have only 1 broker agency 
    associated with it.
    """
    fkey = ParentalKey(
        BrokerAgencyIndex, 
        related_name="agencies"
    )
    agency_name = CharField(max_length=50)
    def __str__(self):
        return self.agency_name
