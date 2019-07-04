#!/usr/bin/env python
#
import os
import time
import requests
import json
import logging
import uuid
from datadog import initialize, api


# [start config]
# GCP image file url
GCP_IMAGE = 'https://storage.googleapis.com/xxx-testing-monitor/sample-invoice.png'

# S3 image file url
S3_IMAGE = 'https://s3-eu-west-1.amazonaws.com/xxx-public/xxx-testing-monitor/sample-invoice.png'

# Configure this environment variable via Dockerfile ENV
#
# Google API Key
API_KEY = os.environ['API_KEY']

# Datadog authentication api
options = {
    'api_key': 'xxx',
    'app_key': 'xxx'
}

initialize(**options)
#
logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO,
                    datefmt='%Y-%m-%d %I:%M:%S')
# [end config]


def _generate_payload_data(image_uri):
    """Generate the request payload data
    Format copied from https://cloud.google.com/vision/docs/ocr"""
    sending_request = {
        "requests": [
            {
                "image": {
                    "source": {
                        "imageUri": image_uri
                    }
                },
                "features": [
                    {
                        "type": "DOCUMENT_TEXT_DETECTION",
                        "maxResults": 1000
                    }
                ]
            }
        ]
    }
    return sending_request


def detect_document_uri(image_uri=GCP_IMAGE, image_source='gcp_storage', env='staging'):
    """Input image url location ,image source location,
       post response status code to datadog"""

    # make a UUID based on the host ID and current time
    uid = uuid.uuid1()

    # cache brake
    cache_brake = '?uuid={}'.format(uid)

    sending_request = _generate_payload_data("{}{}".format(image_uri, cache_brake))

    # start the timer
    start_timer = time.time()

    # submit the post
    response = requests.post(
        url='https://vision.googleapis.com/v1/images:annotate?key={}'.format(API_KEY),
        data=json.dumps(sending_request),
        headers={'Content-Type': 'application/json', 'Cache-Control': 'no-cache'}
    )

    status_code = str(response.status_code)

    # stop the timer second to millisecond
    latency = (time.time() - start_timer) * 1000

    metric = "probe.google.vision.gauge.latency"
    # Post data to datadog
    api.Metric.send([{
        'metric': metric,
        'type': 'gauge',
        'host': 'k8s',
        'points': [[time.time(), float(latency)]],
        'tags': {'service': 'google-vision', 'env': env,
                            'status-code': status_code,
                            'location': 'kuberntes',
                            'image_location': image_source
                 }

    }])
    logging.info("METRIC:{} STATUS_CODE:{} LATENCY:{}".format(metric, status_code, float(latency)))
    return float(latency)


if __name__ == '__main__':
        print(detect_document_uri())
        print(detect_document_uri(S3_IMAGE, image_source='s3_storage'))
