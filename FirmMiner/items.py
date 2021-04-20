import scrapy
from scrapy_djangoitem import DjangoItem

from webapp.outreach.models import Firm, Attorney


class FirmItem(DjangoItem):
    django_model = Firm
    top_tier_firm_rankings = scrapy.Field()
    firm_rankings = scrapy.Field()


class AttorneyItem(DjangoItem):
    django_model = Attorney
