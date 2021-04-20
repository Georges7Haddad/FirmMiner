import os

BOT_NAME = "FirmMiner"

SPIDER_MODULES = ["FirmMiner.spiders"]
NEWSPIDER_MODULE = "FirmMiner.spiders"

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure item pipelines
ITEM_PIPELINES = {
    "FirmMiner.pipelines.cleaning_pipelines.CleaningPipeline": 200,
    "FirmMiner.pipelines.writer_pipeline.WriteItemsPipeline": 300,
    "s3pipeline.S3Pipeline": 400,
    "sqspipeline.SQSPipeline": 500,
    "FirmMiner.pipelines.db_pipeline.DBPipeline": 600,
}

# region AWS Configuration
AWS_DEFAULT_REGION = os.getenv("AWS_DEFAULT_REGION", "eu-central-1")
AWS_REGION_NAME = AWS_DEFAULT_REGION
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "")
BUCKET_NAME = os.getenv("BUCKET_NAME", "robinai-lawfirm")

S3PIPELINE_URL = "s3://robinai-lawfirm/{name}/{time}/items.json"

SQSPIPELINE_QUEUE_NAME = os.getenv("QUEUE_NAME", "robinai-lawfirm")
print(os.environ)