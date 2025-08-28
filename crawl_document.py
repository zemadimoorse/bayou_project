import os
import google.generativeai as genai
import json
from selenium import webdriver
from prompts import classify_links_prompt, extract_billing_prompt


API_KEY = '' # Add API key here.
# NOTE: In prod, we would put the API key in an environment variable.
genai.configure(api_key=API_KEY)

# In prod, we would need to put this in a class so these variables are scoped to the current user's process instance.
visited_links = set()

def crawl_for_links(driver): 
    model = genai.GenerativeModel('gemini-2.5-flash')
    # TODO: add schema from separate file.
    generation_config = genai.GenerationConfig(response_mime_type="application/json")
    # TODO: add streaming/async handling here.
    response = model.generate_content(
        classify_links_prompt + driver.page_source, generation_config=generation_config
    )
    # TODO: Wrap this in a try/catch and add logging.
    return json.loads(response.text)

def crawl_for_billing(driver, link_type):
  # Same here, hitting API limits so this is only evaluating billing views.
  if link_type == "billing":
    prompt = extract_billing_prompt
  
  # TODO: Add error here.
  if not prompt: 
    return

  if (driver.current_url in visited_links):
    return
  
  visited_links.add(driver.current_url)

  model = genai.GenerativeModel('gemini-2.5-flash')
  generation_config = genai.GenerationConfig(response_mime_type="application/json")
  # TODO: add streaming here.
  response = model.generate_content(
    extract_billing_prompt + driver.page_source, generation_config=generation_config
  )
  print(response.text)