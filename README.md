
map endpoints to endpoint_groups based on naming policy


Looks for mapping.csv for endpoint name to endpoint_group name:

short_name_prefix,group
IN,"India Roaming Users"
LIN,"India Roaming Users"
LFR,"France Roaming Users"
NAR,"US Roaming Users"
LNAR,"US Roaming Users"


Run example

----------
python3 ./botd-endpoints-to-endpoint_groups.py 
Mapping table:
short_name_prefix: IN, group: India Roaming Users
short_name_prefix: LIN, group: India Roaming Users
short_name_prefix: LFR, group: France Roaming Users
short_name_prefix: NAR, group: US Roaming Users
short_name_prefix: LNAR, group: US Roaming Users
---------------------------------------
Endpoints to remap:
fqdn: LNAR-A12.corp.local, current_group: All BloxOne Endpoints (Default), future_group US Roaming Users
fqdn: lnar-s123l.corp.local, current_group: All BloxOne Endpoints (Default), future_group US Roaming Users
fqdn: nar-fo23.corp.local, current_group: All BloxOne Endpoints (Default), future_group US Roaming Users
fqdn: NAR-FO23.corp.local, current_group: All BloxOne Endpoints (Default), future_group US Roaming Users
---------------------------------------
Adding ['42b3a1185e76b77b476fb3bceeeb9bdc', '34d52390218f5c3118d212687c4981d5', '5d3185127eebb634c85fa28aed1ddf73', '9b562d61dece28d64504fe8258076f55'] to group: US Roaming Users
Group before: 
{
    "created_time": "2020-04-07T09:20:32Z",
    "description": "",
    "id": 209169,
    "internal_domain_lists": [
        578741
    ],
    "is_default": false,
    "is_probe_enabled": true,
    "name": "US Roaming Users",
    "policy_id": 97845,
    "policy_name": "US",
    "probe_domain": "probe.infoblox.com",
    "probe_response": "C0XXY7OOBJXX96865P3QRT02SSINVMWZ",
    "roaming_devices": [
        "22795813648a44eaf81e62815cc8a7af",
        "a83b57e294d25edd8da1fb4c7e36ef38",
        "49dd712607f693be7d9def7bc477afa3",
        "2a64bca208575e7552f01cf6d598e9f4",
        "50be6f9e5dd201956e1c6918204789c4"
    ],
    "updated_time": "2020-04-07T09:20:52Z"
}
Group after: 
{
    "created_time": "2020-04-07T09:20:32Z",
    "description": "",
    "id": 209169,
    "internal_domain_lists": [
        578741
    ],
    "is_default": false,
    "is_probe_enabled": true,
    "name": "US Roaming Users",
    "policy_id": 97845,
    "policy_name": "US",
    "probe_domain": "probe.infoblox.com",
    "probe_response": "C0XXY7OOBJXX96865P3QRT02SSINVMWZ",
    "roaming_devices": [
        "22795813648a44eaf81e62815cc8a7af",
        "a83b57e294d25edd8da1fb4c7e36ef38",
        "49dd712607f693be7d9def7bc477afa3",
        "2a64bca208575e7552f01cf6d598e9f4",
        "50be6f9e5dd201956e1c6918204789c4",
        "42b3a1185e76b77b476fb3bceeeb9bdc",
        "34d52390218f5c3118d212687c4981d5",
        "5d3185127eebb634c85fa28aed1ddf73",
        "9b562d61dece28d64504fe8258076f55"
    ],
    "updated_time": "2020-04-07T09:20:52Z"
}
