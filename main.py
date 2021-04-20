import logging

import django

django.setup()

import boto3
from moto.sqs.exceptions import QueueDoesNotExist
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from FirmMiner.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, BUCKET_NAME, AWS_DEFAULT_REGION
from FirmMiner.spiders.law500 import Legal500Spider

logger = logging.getLogger(__name__)


def create_sqs_queue():
    sqs = boto3.client(
        "sqs",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_DEFAULT_REGION,
    )
    try:
        sqs.get_queue_url(QueueName=BUCKET_NAME)
    except QueueDoesNotExist as err:
        logger.warning(f"Queue {BUCKET_NAME} not found on SQS. Creating queue.")
        sqs.create_queue(QueueName=BUCKET_NAME)


def create_s3_bucket():
    s3 = boto3.resource(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_DEFAULT_REGION,
    )

    bucket = s3.Bucket(BUCKET_NAME)

    if not bucket.creation_date:
        logger.warning(f"Bucket {BUCKET_NAME} not found on S3. Creating bucket.")
        s3.create_bucket(Bucket=BUCKET_NAME, CreateBucketConfiguration={"LocationConstraint": AWS_DEFAULT_REGION})


if __name__ == "__main__":
    # initialize AWS
    create_s3_bucket()
    create_sqs_queue()

    # Start parsing
    process = CrawlerProcess(get_project_settings())
    process.crawl(Legal500Spider)
    process.start()
