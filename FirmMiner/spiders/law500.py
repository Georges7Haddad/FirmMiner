import logging

import scrapy
from scrapy import Request

from FirmMiner.items import FirmItem, AttorneyItem

logger = logging.getLogger(__name__)


class Legal500Spider(scrapy.Spider):
    name = "law500"
    base_url = "https://www.legal500.com"
    start_urls = ["https://www.legal500.com/united-kingdom-solicitors/"]

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url=url, callback=self.pre_parse, dont_filter=True)

    def pre_parse(self, response):
        for city in response.xpath('//*[@id="countryList"]/li'):
            city_url = city.xpath("a/@href").get()
            city_name = city.xpath("a/text()").get()
            logger.info(f"Generating directory for {city_name}")
            yield Request(
                url=f"{self.base_url}/{city_url}/directory/",
                callback=self.parse,
                dont_filter=True,  # we skip the request duplicate filtering because this is a search page
                meta={"city_name": city_name}
            )

    def parse(self, response, **kwargs):
        for firm in response.xpath('//*[@id="directoryUL"]/li'):
            firm_link = firm.xpath("a/@href").get()
            logger.info(f"Generating directory for attorney firm")
            yield Request(
                url=f"{self.base_url}{firm_link}",
                callback=self.post_parse,
                dont_filter=True, # we skip the request duplicate filtering because this is a search page
                meta={"city_name": response.meta["city_name"]}
            )

    def post_parse(self, response):
        firm_item = FirmItem()
        firm_item["city_name"] = response.meta["city_name"]
        firm_item["name"] = response.xpath('//*[@id="left-col"]/h2/text()').get()
        firm_item["address"] = ""
        for line in response.xpath('//*[@id="left-col"]/div[1]/address/text()'):
            firm_item["address"] += line.get()

        firm_item["email"] = response.xpath("//*[@id='left-col']/div[2]/div//a[@class='firm-email']/@href").get()
        firm_item["website"] = response.xpath("//*[@id='left-col']/div[2]/div//a[@class='firm-website']/@href").get()
        firm_item["phone_number"] = response.xpath(
            "//*[@id='left-col']/div[2]/div//i[@class='fa fa-phone-square']/../text()"
        ).get()
        firm_item["fax_number"] = response.xpath(
            "//*[@id='left-col']/div[2]/div//i[@class='fa fa-fax']/../text()"
        ).get()

        firm_item["top_tier_firm_rankings"] = []
        for ranking in response.xpath('//*[@id="top-ranked"]/li'):
            firm_item["top_tier_firm_rankings"].append(ranking.xpath("a/text()").get())

        firm_item["firm_rankings"] = []
        for ranking in response.xpath('//*[@id="other-ranked"]/li'):
            firm_item["firm_rankings"].append(ranking.xpath("a/text()").get())
        logger.info("Yielding firm item")
        yield firm_item

        for attorney in response.xpath('//*[@id="lawyer-profiles-list"]/tbody/tr'):
            attorney_link = attorney.xpath('td[@class="profile-link"]/a/@href').get()
            logger.info(f"Generating profile page for attorney")
            yield Request(
                url=f"{self.base_url}{attorney_link}",
                callback=self.post_post_parse,
                dont_filter=True,
                meta={"firm_name": firm_item["name"]}
            )

    def post_post_parse(self, response):
        attorney_item = AttorneyItem()
        attorney_item["name"] = response.xpath('//*[@id="lawyer"]/h2/text()').get()
        attorney_item["firm_name"] = response.meta["firm_name"]
        attorney_item["phone_number"] = response.xpath(
            "//*[@id='lawyer']/div/div//i[@class='fa fa-phone-square']/../../text()"
        ).get()
        attorney_item["email"] = response.xpath(
            "//*[@id='lawyer']/div/div//i[@class='fa fa-envelope']/../../a/@href"
        ).get()
        attorney_item["picture"] = response.xpath("//*[@id='lawyer']/div/img/@data-lazy-src").get()
        logger.info("Yielding attorney item")
        yield attorney_item
