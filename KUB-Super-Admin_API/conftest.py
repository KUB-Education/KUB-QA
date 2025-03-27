import json
import pytest
import logging
from dotenv import load_dotenv

load_dotenv()

#hooks

def pytest_tavern_beta_before_every_request(request_args):
    if "json" in request_args:
        json_formatted_str = json.dumps(request_args["json"], indent=2)
        logging.info("Request input json data:\n"+json_formatted_str)

def pytest_tavern_beta_after_every_response(expected, response):
    try:
        expected_str = str(expected)
        expected_str = expected_str.replace("<", "\'")
        expected_str = expected_str.replace(">", "\'")
        expected_str = expected_str.replace("\'", "\"")
        expected_json = json.loads(expected_str)
        response_json = response.json()
        if "json" in expected_json:
            expected_str = json.dumps(json.loads(expected_str)["json"], indent=2)
            logging.info("Expected response output json data:\n"+expected_str)
    except:
        logging.info("Expected response output json data:\n"+str(expected))
    try:
        responce_str = json.dumps(response.json(), indent=2)
        logging.info("Actual response output json data:\n"+responce_str)
    except:
        pass