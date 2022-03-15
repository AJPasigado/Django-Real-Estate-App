from __future__ import absolute_import, unicode_literals

from django.db import models
from django.db.models import CharField, BooleanField, ImageField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel

from wagtail.core.models import Page


class HomePage(Page):
    footer_title = CharField(max_length=30, blank=True)
    footer_subtitle = CharField(max_length = 100, blank=True)
    home_tagline = CharField(max_length = 30, blank=True)
    company_logo = ImageField(upload_to='uploads/home/logo/', blank=True)
    enable_footer = BooleanField()
    content_panels = Page.content_panels + [
        FieldPanel('home_tagline'),
        FieldPanel('company_logo'),
        MultiFieldPanel(
            [
                FieldPanel('enable_footer'),
                FieldPanel('footer_title'),
                FieldPanel('footer_subtitle'),
            ],
            heading="Footer Settings",
            classname="collapsible"
        ),
    ]
