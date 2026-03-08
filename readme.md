curl -k -u "NXOS_USER:NXOS_PASS" \
-H "Accept: application/yang-data+json" \
"https://sbx-nxos-mgmt.cisco.com/restconf/data/Cisco-NX-OS-device:System" > schemas/nxos_system.json
