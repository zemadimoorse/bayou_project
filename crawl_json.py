import os
import google.generativeai as genai
import json
from selenium import webdriver
from prompts import json_billing_prompt

API_KEY = '' # Add API key here.
# NOTE: In prod, we would put the API key in an environment variable.
genai.configure(api_key=API_KEY)

# In prod, we would need to put this in a class so these variables are scoped to the curren    rm -rf .gitt user's process instance.
visited_resources = set()

def filter_driver_requests(driver):
    json_requests = []

    for request in driver.requests:
        try:
            if request.response:  # Ensure a response exists for the request
                # Check if the 'Content-Type' header exists and contains 'application/json'
                # NOTE: In prod, we would want to look up multiple content-types, not just application/json.
                if 'Content-Type' in request.response.headers and \
                'application/json' in request.response.headers['Content-Type']:
                        json_requests.append(json.loads(request.response.body))
        except Exception as e:
            # print(f"Error processing json request: {e}")
            #TODO: Add error handling
            pass

    return json_requests

def crawl_json_for_billing(responses):
  model = genai.GenerativeModel('gemini-2.5-flash')
  generation_config = genai.GenerationConfig(response_mime_type="application/json")
  # TODO: add streaming here.
  # TODO: use defined response JSON format (standard list of fields).
  response = model.generate_content(
      json_billing_prompt + json.dumps(responses), generation_config=generation_config
  )
  return json.loads(response.text)