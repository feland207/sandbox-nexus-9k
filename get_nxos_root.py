import os
import requests
import xmltodict
from dotenv import load_dotenv
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning

load_dotenv()
disable_warnings(InsecureRequestWarning)

HOST = "sbx-nxos-mgmt.cisco.com"
AUTH = (os.getenv("NXOS_USER"), os.getenv("NXOS_PASS"))

# The "Discovery" URL for all RESTCONF devices
URL = f"https://{HOST}/restconf/data/Cisco-NX-OS-device:System"

def discover_modules():
    print(f"--- Discovering YANG Modules on {HOST} ---")
    response = requests.get(URL, auth=AUTH, verify=False, headers={"Accept": "application/yang-data+xml"})
    
    if response.status_code in [200, 204]:
        data = xmltodict.parse(response.text)
        modules = data.get('System', [])
        
        print(f"{'Module Name':<30} | {'Revision':<15} | {'Namespace'}")
        print("-" * 80)
        for m in modules:
            # We filter for Cisco-specific models to find our "Root"
            if "Cisco-NX-OS" in m.get('name', ''):
                print(f"{m.get('name'):<30} | {m.get('revision'):<15} | {m.get('namespace')}")
    else:
        print(f"Discovery Failed: {response.status_code}")

if __name__ == "__main__":
    discover_modules()
