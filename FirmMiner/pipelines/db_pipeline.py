from django.db import transaction

from FirmMiner.items import FirmItem, AttorneyItem
from FirmMiner.spiders.law500 import logger
from webapp.outreach.models import Ranking


class DBPipeline:
    def process_firm(self, item):
        try:
            firm = FirmItem.django_model.objects.get(name=item['name'])
        except FirmItem.django_model.DoesNotExist:
            firm = FirmItem()
            firm = firm.instance

        firm.name = item["name"]
        firm.city_name = item["city_name"]
        firm.address = item["address"]
        firm.email = item["email"]
        firm.website = item["website"]
        firm.phone_number = item["phone_number"]
        firm.fax_number = item["fax_number"]

        with transaction.atomic():
            firm.save()

        for ranking in item["top_tier_firm_rankings"]:
            with transaction.atomic():
                ranking, created = Ranking.objects.get_or_create(name=ranking)
                firm.top_tier_firm_rankings.add(ranking)

        for ranking in item["firm_rankings"]:
            with transaction.atomic():
                ranking, created = Ranking.objects.get_or_create(name=ranking)
                firm.firm_rankings.add(ranking)

        with transaction.atomic():
            firm.save()

    @staticmethod
    def process_attorney(item):
        attorney = AttorneyItem()
        attorney["name"] = item["name"]
        firm, created = FirmItem.django_model.objects.get_or_create(name=item["firm_name"])
        logger.debug(f"\n\n{item['name']} {item['firm_name']}\n\n")
        attorney["firm_name"] = firm
        attorney["email"] = item["email"]
        attorney["phone_number"] = item["phone_number"]
        attorney["picture"] = item["picture"]
        attorney.save()

    def process_item(self, item, spider):
        if item.__class__.__name__ == "FirmItem":
            self.process_firm(item)
        elif item.__class__.__name__ == "AttorneyItem":
            self.process_attorney(item)
        return item
