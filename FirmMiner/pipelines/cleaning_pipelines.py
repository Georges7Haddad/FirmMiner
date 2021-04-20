import re

from itemadapter import ItemAdapter


class CleaningPipeline:
    def clean_firm_item(self, item, spider):
        adapter = ItemAdapter(item)
        adapter["name"] = adapter["name"][1:-1]
        adapter["address"] = re.sub("\s{2,}|\n", " ", adapter["address"])[1:-1] if adapter["address"] else None
        adapter["email"] = adapter["email"].split(":")[1].split("?")[0] if adapter["email"] else None
        adapter["phone_number"] = re.sub(" ", "", adapter["phone_number"]) if adapter["phone_number"] else None
        adapter["fax_number"] = re.sub(" ", "", adapter["fax_number"]) if adapter["fax_number"] else None
        return item

    def clean_attorney_item(self, item, spider):
        adapter = ItemAdapter(item)
        adapter["name"] = re.sub("\n|\t", "", adapter["name"])
        adapter["firm_name"] = adapter["firm_name"]
        adapter["email"] = adapter["email"].split(":")[1].split("?")[0] if adapter["email"] else None
        adapter["phone_number"] = re.sub(" ", "", adapter["phone_number"]) if adapter["phone_number"] else None
        return item

    def process_item(self, item, spider):
        if item.__class__.__name__ == "FirmItem":
            return self.clean_firm_item(item, spider)
        if item.__class__.__name__ == "AttorneyItem":
            return self.clean_attorney_item(item, spider)


