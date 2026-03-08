import os
import requests
import json
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning
from dotenv import load_dotenv

# 1. Setup
load_dotenv()
disable_warnings(InsecureRequestWarning)

# 2. Config from .env
HOST = "sbx-nxos-mgmt.cisco.com"
USER = os.getenv("NXOS_USER")
PASS = os.getenv("NXOS_PASS")

# Targeted RESTCONF path for physical interface items
URL = f"https://{HOST}/restconf/data/Cisco-NX-OS-device:System/intf-items/phys-items"

HEADERS = {
    "Accept": "application/yang-data+json",
    "Content-Type": "application/yang-data+json"
}

def fetch_nexus_interfaces():
    print(f"--- Querying RESTCONF Interface Tree on {HOST} ---")
    
    try:
        response = requests.get(
            URL, 
            auth=(USER, PASS), 
            headers=HEADERS, 
            verify=False,
            timeout=10
        )

        if response.status_code == 200:
            data = response.json()
            # Navigate the NX-OS YANG Hierarchy
            interfaces = data.get("Cisco-NX-OS-device:phys-items", {}).get("PhysIf-list", [])
            
            print(f"{'Interface ID':<15} | {'Admin State':<12} | {'Description':<25}")
            print("-" * 60)
            
            for eth in interfaces:
                print(f"{eth.get('id'):<15} | {eth.get('adminSt'):<12} | {eth.get('descr') or '--':<25}")
        else:
            print(f"Failed! Status: {response.status_code}")
            print(f"Detail: {response.text}")

    except Exception as e:
        print(f"Connection Error: {str(e)}")

if __name__ == "__main__":
    fetch_nexus_interfaces()
