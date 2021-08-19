import logging
import time
import azure.functions as func
import uuid
import json


def main(request: func.HttpRequest, message: func.Out[str],queue: func.Out[str]) -> func.HttpResponse:
    logging.info('HTTP trigger function received a request.')
    start = time.time()

    req_body = request.get_json()
    subtitle = req_body.get("subtitle")
    languages = req_body.get("languages")

    rowKey = str(uuid.uuid4())

    for language in languages:
        event_data = {
            "RowKey":rowKey,
            "languageCode": language
        }
        queue.set(json.dumps(event_data))


    data = {
        "Subtitle": subtitle,
        "PartitionKey": "message",
        "RowKey": rowKey
    }
    message.set(json.dumps(data))
    end = time.time()
    processingTime = end - start

    return func.HttpResponse(
        f"Processing took {str(processingTime)} seconds. Translation is: {subtitle}",
        status_code=200
    )

