"""
Saves a configuration file on the current directory
"""

import json
import requests
import re
import datetime

# Disable requests
requests.packages.urllib3.disable_warnings()

# Constants
URL = "https://devnetapi.cisco.com/sandbox/apic_em/api/v1"
PAYLOAD = json.dumps({
    "username": "devnetuser",
    "password": "Cisco123!"
})

def get_token():
    """ Gets an APIC-EM ticket. """
    endpoint = "/ticket"
    headers = {"content-type" : "application/json"}
    response = requests.post(
        URL + endpoint,
        data=PAYLOAD,
        headers=headers,
        verify=False
    ).json()
    return response["response"]["serviceTicket"]

def get_device_id():
    """ Get a device id. """
    endpoint = "/network-device"
    headers = {"X-AUTH-TOKEN": get_token()}
    response = requests.get(URL + endpoint, headers=headers, verify=False).json()
    # Iterate over the response and find device with access role.
    # Return ID number of the first device matching the `if` statement.
    for item in response["response"]:
        if item["role"] == "ACCESS":
            return item["id"]

def get_config(device_id):
    """ Get device configuration """
    endpoint = "/network-device/" + device_id + "/config"
    headers = {"X-AUTH-TOKEN": get_token()}
    response = requests.get(URL + endpoint, headers=headers, verify=False).json()
    # Find the hostname in the response body and save it to a hostname variable.
    hostname = re.findall('hostname\s(.+?)\s', response["response"])[0]
    # Create a date_time variable which will hold the current time.
    date_time = datetime.datetime.now()
    # Create a variable which will hold the hostname combined with the date and
    # time. The format will be hostname_year_month_day_hour.minute.second.
    file_name = (
        hostname
        + "_"
        + str(date_time.year)
        + "_"
        + str(date_time.month)
        + "_"
        + str(date_time.day)
        + "_"
        + str(date_time.hour)
        + "."
        + str(date_time.minute)
        + "."
        + str(date_time.second)
        + ".txt"
    )
    # Creates the file in the current working directory.
    configuration_file = open(file_name, "w")
    # Write the response body to the file.
    configuration_file.write(response["response"])
    # Close the file when writing is complete.
    configuration_file.close()

# Script body
# ===========

# Print a message to the user to let it know that something is happening
print("\nThis may take a while. \nPlease wait while we get the device \
configuration from the APIC-EM.\nYour configuration will be saved following \
this format: hostname_year_month_day_hour.minute.second.")

# Assign obtained ID to a variable. Provide authentication token and APIC-EM's URL address
DEVICE_ID = get_device_id()

# Call `get_config()` function to obtain and write device's configuration to a
# file. Provide authentication token, APIC-EM's URL address and device's ID
get_config(DEVICE_ID)
