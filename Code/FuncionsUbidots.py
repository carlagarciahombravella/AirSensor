import time
import requests
import math
import random

# RETRIEVE DATA TO UBIDOTS
def get_var(device, variable,TOKEN):
    # gets variable value from a given device inside an account whose token is sppecified as well.
    try:
        url = "http://industrial.api.ubidots.com/"
        url = url + \
            "api/v1.6/devices/{0}/{1}/".format(device, variable)
        headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}
        req = requests.get(url=url, headers=headers)
        return req.json()['last_value']['value']
    except:
        pass

# SEND DATA TO UBIDOTS
def build_payload(medidas, var_labels):

    payload = {var_labels[0]: medidas['CO2'],
               var_labels[1]: medidas['Formaldehil'],
               var_labels[2]: medidas['TVOC'],
               var_labels[3]: medidas['PM25'],
               var_labels[4]: medidas['PM10'],
               var_labels[5]: medidas['Temperatura'],
               var_labels[6]: medidas['Humitat']}

    return payload


def post_request(payload,TOKEN,DEVICE_LABEL):
    # Creates the headers for the HTTP requests
    url = "http://things.ubidots.com"
    url = "{}/api/v1.6/devices/{}".format(url, DEVICE_LABEL)
    headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}

    # Makes the HTTP requests
    status = 400
    attempts = 0
    while status >= 400 and attempts <= 5:
        req = requests.post(url=url, headers=headers, json=payload)
        status = req.status_code
        attempts += 1
        time.sleep(1)

    # Processes results
    print(req.status_code, req.json())
    if status >= 400:
        print("[ERROR] Could not send data after 5 attempts, please check \
            your token credentials and internet connection")
        return False

    print("[INFO] request made properly, your device is updated")
    return True
