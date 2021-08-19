import logging
import time
import azure.functions as func
import uuid
import json
import typing

def main(request: func.HttpRequest, message: func.Out[str],queue: func.Out[typing.List[str]]) -> func.HttpResponse:
    logging.info('HTTP trigger function received a request.')
    start = time.time()

    req_body = request.get_json()
    subtitle = req_body.get("subtitle")
    languages = req_body.get("languages")

    rowKey = str(uuid.uuid4())

    messages = []

    for language in languages:
        event_data = {
            "RowKey":rowKey,
            "languageCode": language
        }
        logging.warning(event_data)

        messages.append(json.dumps(event_data))

    queue.set(messages)

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

