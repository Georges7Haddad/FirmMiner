import csv
import json

from itemadapter import ItemAdapter


class WriteItemsPipeline:
    def __init__(self):
        self.firms_json = open("output/firms.json", "w")
        self.attorneys_json = open("output/attorneys.json", "w")
        firms_fieldnames = [
            "name",
            "city_name",
            "address",
            "email",
            "website",
            "phone_number",
            "fax_number",
            "top_tier_firm_rankings",
            "firm_rankings",
        ]
        self.firms_csv = open("output/firms.csv", "w")
        self.firms_writer = csv.DictWriter(self.firms_csv, fieldnames=firms_fieldnames)
        attorneys_fieldnames = ["name", "phone_number", "email", "picture", "firm_name"]
        self.attorneys_csv = open("output/attorneys.csv", "w")
        self.attorneys_writer = csv.DictWriter(self.attorneys_csv, fieldnames=attorneys_fieldnames)

    def open_spider(self, spider):
        self.firms_writer.writeheader()
        self.attorneys_writer.writeheader()
        self.firms_json.write("[")
        self.attorneys_json.write("[")

    def close_spider(self, spider):
        self.firms_json.write("]")
        self.attorneys_json.write("]")
        self.attorneys_json.close()
        self.firms_json.close()

    def process_item(self, item, spider):
        line = json.dumps(ItemAdapter(item).asdict()) + ",\n"
        if item.__class__.__name__ == "FirmItem":
            self.firms_json.write(line)
            self.firms_writer.writerow(item)
        if item.__class__.__name__ == "AttorneyItem":
            self.attorneys_json.write(line)
            self.attorneys_writer.writerow(item)
        return item