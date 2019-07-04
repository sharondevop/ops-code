#!/usr/bin/env python
#
# [START app]
import os
import time
import requests
import json
from datadog import initialize, api
import logging
import uuid
import flask


# [start config]
app = flask.Flask(__name__)
# Configure this environment variable via app.yaml
API_KEY = os.environ['API_KEY']
#
# GCP image file url
GCP_IMAGE = 'https://storage.googleapis.com/xxx-testing-monitor/sample-invoice.png'
#
# S3 image file url
S3_IMAGE = 'https://s3-eu-west-1.amazonaws.com/xxx-public/xxx-testing-monitor/sample-invoice.png'
#
# Datadog authentication api
options = {
    'api_key': 'xxxx',
    'app_key': 'xxxx'
}
#
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


def _detect_document_uri(image_uri=GCP_IMAGE, image_source='gcp_storage', env='staging'):
    """Input image url location ,image source location,
       post response status code to datadog, return status code and latency time."""
    try:
        # verify that this is a cron job request
        #is_cron = flask.request.headers['X-Appengine-Cron']
        #logging.info('Received cron request {}'.format(is_cron))

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
            'host': 'gcp',
            'points': [[time.time(), float(latency)]],
            'tags': {'service': 'google-vision', 'env': env,
                                'status-code': status_code,
                                'location': 'google-cloud',
                                'image_location': image_source
                     }

        }])
        logging.info("METRIC:{} STATUS_CODE:{} LATENCY:{} PAYLOAD:{}".format(metric, status_code, float(latency), sending_request))
        status = '<html><p>STATUS CODE: {} LATENCY: {}</p> PAYLOAD: {}</html>'.format(status_code, float(latency), sending_request)
        return status

    except KeyError as e:
        status = '<html><p>Sorry, this capability is accessible only by the Cron service, but I got a KeyError for {}</p>' \
                 ' -- ' 'try invoking it from <a href="{}"> the GCP console / AppEngine / taskqueues </a></html>'\
                .format(e, 'http://console.cloud.google.com/appengine/taskqueues?tab=CRON')
        logging.info('Rejected non-Cron request')

    return status


@app.route('/call-google')
def call():
    gcp = _detect_document_uri()
    s3 = _detect_document_uri(S3_IMAGE, image_source='s3_storage')
    return "{}{}".format(gcp, s3)


@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END app]
