import os
import requests
import json
from dotenv import load_dotenv
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning

# Setup
load_dotenv()
disable_warnings(InsecureRequestWarning)

# Config
HOST = "sbx-nxos-mgmt.cisco.com"
USER = os.getenv("NXOS_USER")
PASS = os.getenv("NXOS_PASS")

# The specific URI for the hostname leaf
URL = f"https://{HOST}/restconf/data/Cisco-NX-OS-device:System/name"

# Headers - Note: We use 'patch' for a merge/update operation
HEADERS = {
    "Accept": "application/yang-data+json",
    "Content-Type": "application/yang-data+json"
}

# The payload must match the YANG container name
payload = {
    "Cisco-NX-OS-device:name": "Hola_Pepe"
}

def change_hostname():
    print(f"--- Changing Hostname to Hola_Pepe on {HOST} ---")
    
    response = requests.patch(
        URL, 
        auth=(USER, PASS), 
        headers=HEADERS, 
        data=json.dumps(payload),
        verify=False
    )

    if response.status_code in [200, 201, 204]:
        print(f"Success! Status Code: {response.status_code}")
    else:
        print(f"Failed! Status Code: {response.status_code}")
        print(f"Response: {response.text}")

if __name__ == "__main__":
    change_hostname()
