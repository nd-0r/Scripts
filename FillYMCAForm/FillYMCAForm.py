# %%
from dataclasses import dataclass

from datetime import date
from datetime import datetime
from datetime import timedelta
from dateutil import parser

import requests

from urllib.parse import urlencode
from urllib.parse import quote_plus

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.expected_conditions import presence_of_element_located

import logging
from os.path import exists

logfile = './booker.log'

if (exists('./booker.log')):
  logging.basicConfig(filename='booker.log', filemode='a', format='%(name)s – %(levelname)s – %(message)s')
else:
  logging.basicConfig(filename='booker.log', filemode='w', format='%(name)s – %(levelname)s - %(message)s')


# %%
@dataclass
class User:
  """Class for organizing ymca user information"""
  name: list
  birthday: date
  email: str
  phone: str

@dataclass
class YMCA:
  """Class for organizing ymca registration information"""
  name: str
  dom_id: int
  desired_appt_type: list # preferred appt type first
  desired_staff_member: list # preferred staff member first


# %%


# %%
day_to_search = datetime.today().date() + timedelta(6) # TODO - make week | one week from today 

def get_selection_value(options, name_to_find):
  for element in options:
    if (element.text == name_to_find):
      return element.get_attribute("value")

def build_request_list_url(dom_id, sess_id, date_filter, appointment_type_filter="-1", trainer_filter="-1"):
  suffix = "&appt_sel=&external_cal=false"
  url = base_url + "?&request=get_list&domid=" + dom_id + "&sessid=" + sess_id + "&date_filter=" \
        + date_filter + "&appointment_type_filter=" + appointment_type_filter + "&trainer_filter=" \
        + trainer_filter + suffix

  return url

def build_request_appt_payload(dom_id, sess_id, datetime, appointment_type_id, appointment_id):
  payload = {'request' : 'make_request', \
             'domid' : dom_id, \
             'sessid' : sess_id, \
             'datetime' : datetime, \
             'availability_id' : '', \
             'appointment_type_id' : appointment_type_id, \
             'appointment_id' : appointment_id}

  return urlencode(payload).replace('%2B', '+') # HACK - Get an error otherwise

def build_request_appt_headers(driver, dom_id, sess_id):
  headers = {'Host' : base_url.split('/')[2], \
             'User-Agent' : driver.execute_script("return navigator.userAgent;"), \
             'Accept' : '*/*', \
             'Accept-Language' : 'en-US,en;q=0.5', \
             'Referer' : base_url + '?sessid=' + str(sess_id) + '&domid=' + str(dom_id) + '&logout=0', \
             'Content-Type' : 'application/x-www-form-urlencoded; charset=UTF-8', \
             'X-Requested-With' : 'XMLHttpRequest', \
             'Origin' : 'https://' + base_url.split('/')[2], \
             'Connection' : 'keep-alive', \
             'TE' : 'Trailers'}
  
  return headers
  
def find_best_appt_time(times_json, free_time):
  (time_pref, tolerance) = free_time
  best_time = None
  best_diff = tolerance # diff can't be more than the tolerance

  for time in times_json:
    pref_time = datetime.strptime(time_pref, '%H:%M').utcnow()
    candidate_time = datetime.strptime(time['time_24'], '%H:%M').utcnow()
    if (candidate_time - pref_time < best_diff):
      best_diff = candidate_time - pref_time
      best_time = datetime.strptime(time['time_24'], '%H:%M')

  return best_time

def book_best_appt(request_url, dom_id, sess_id, driver):
  listing_json = requests.get(request_url).json()

  if (len(listing_json) != 1):
    logging.error(f"No appointments available on date {str(day_to_search)}")
    exit() # IDEA - add push back respawn

  best_time = None # datetime

  for free_time in free_times[day_to_search.weekday()]:
    tmp = find_best_appt_time(listing_json[0]['times'], free_time)
    best_time = tmp if tmp else best_time

  if (best_time == None):
    logging.error(f"No suitable time found for date {str(day_to_search)}")
    exit()

  payload = build_request_appt_payload(dom_id, sess_id, day_to_search.strftime("%Y-%m-%d") + "+" + best_time.strftime("%H:%M:%S"), \
            listing_json[0]['appointment_type_id'], listing_json[0]['appointment_id'])
  heads = build_request_appt_headers(driver, dom_id, sess_id)

  response = requests.request('POST', base_url, data=payload, headers=heads)

  expected = 'request=make_request&domid=164&sessid=' + sess_id + '&datetime=2021-06-19+07%3A45%3A00&availability_id=&appointment_type_id=30764&appointment_id=5779352'

  # print("headers: ", response.request.headers) # TODO - remove
  # print("body: ", response.request.body) # TODO - remove
  # print(response.request.body == expected) # TODO - remove
  # print([i for i in ndiff(response.request.body, expected) if '+' in i or '-' in i]) # TODO - remove
  # print("url: ", response.request.url) # TODO - remove
  # print("response: ", response.content) # TODO - remove

  try:
    if (response.json()['success'] != '1'):
      logging.error(f'Could not schedule appointment for date {str(day_to_search)}')
      exit()
  except (KeyError):
    logging.exception(f'Could not schedule appointment for date {str(day_to_search)}')
    exit()

with webdriver.Firefox() as driver:
  for ymca in ymcas:
    driver.get(base_url + "?domid=" + str(ymca.dom_id))

    wait = WebDriverWait(driver, 10)

    driver.find_element(By.NAME, "first_name").send_keys(user.name[0] + Keys.TAB)
    driver.find_element(By.NAME, "last_name").send_keys(user.name[-1] + Keys.TAB)

    dropdown = Select(driver.find_element(By.NAME, "dob_month"))
    dropdown.select_by_index(user.birthday.month)
    driver.find_element(By.NAME, "dob_month").send_keys(Keys.TAB)

    driver.find_element(By.NAME, "dob_day").send_keys(str(user.birthday.day) + Keys.TAB)
    driver.find_element(By.NAME, "dob_year").send_keys(str(user.birthday.year) + Keys.TAB)
    driver.find_element(By.NAME, "email").send_keys(user.email + Keys.TAB)
    driver.find_element(By.NAME, "phone").send_keys(user.phone)

    driver.find_element(By.NAME, "submitbtn_login").send_keys(Keys.ENTER)

    wait.until(presence_of_element_located((By.CSS_SELECTOR, "h1")))

    sess_id = driver.find_element(By.ID, "sessid").get_attribute("value")

    request_url = ""

    if (ymca.desired_appt_type and not ymca.desired_staff_member): # use appointment dropdown
      appt_dropdown = Select(driver.find_element(By.NAME, "appointment-type-filter")).options

      for appt in ymca.desired_appt_type:
        appt_id = get_selection_value(appt_dropdown, appt)
        request_url = build_request_list_url(str(ymca.dom_id), sess_id, str(day_to_search), appointment_type_filter=appt_id)
        book_best_appt(request_url, ymca.dom_id, sess_id, driver)
        
    elif (ymca.desired_staff_member and not ymca.desired_appt_type): # use staff dropdown
      staff_dropdown = Select(driver.find_element(By.NAME, "trainer-filter")).options

      # TODO - re-implement |  for staff in ymca.desired_staff_member:
      staff_id = get_selection_value(staff_dropdown, ymca.desired_staff_member[0])
      request_url = build_request_list_url(str(ymca.dom_id), sess_id, str(day_to_search), trainer_filter=staff_id)
      book_best_appt(request_url, ymca.dom_id, sess_id, driver)

    # driver.get_screenshot_as_file("/Users/andreworals/Downloads/test.png")