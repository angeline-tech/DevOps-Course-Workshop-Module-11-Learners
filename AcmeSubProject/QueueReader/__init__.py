import logging

import azure.functions as func
import json
import uuid

def main(msg: func.QueueMessage,translatedMessage: func.Out[str], messageJSON) -> None:
    message = json.loads(messageJSON)
    subtitle = message.get('Subtitle')
    processed = process(subtitle)
    event_body = msg.get_body().decode('utf-8')

    loaded = json.loads(event_body)
    language = loaded.get('languageCode')

    logging.error(subtitle +' '+ language)

    rowKey = str(uuid.uuid4())

    table_data = {
        "RowKey":rowKey,
        "languageCode": language,
        "RawSubtitle":subtitle,
        "ProcessedSubtitle":processed
    }
    translatedMessage.set(json.dumps(table_data))

def process(msg:str):
    return msg.upper()