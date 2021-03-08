# encoding = utf-8

import json
import requests
import re
import agate

hostname = "csp.infoblox.com"
api_token = ""  # Your csp API key here
headers = {"Authorization": "Token {}".format(api_token)}

file = "mapping.csv"
delimiter = ","


def build_mapping_table(file):
    table = agate.Table.from_csv(file)
    print('Mapping table:')
    for row in table.rows:
        print("short_name_prefix: {}, group: {}".format(row['short_name_prefix'], row['group']))
    print('---------------------------------------')
    return table


def get_endpoints_to_map(hostname, api_token, table):
    try:
        response = requests.get("https://{}/api/atcep/v1/roaming_devices".format(hostname), headers=headers,
                                verify=True, timeout=(30, 30))
        try:
            r_json = response.json()
        except:
            raise Exception("Response is not valid json. Response:{}".format(response.text))
    except:
        raise Exception("Unable to perform polling from url:{}, status code:{}".format(url, response.status_code))

    endpoints_to_map = {}
    for row in table.rows:
        endpoints_to_map[row['group']] = []

    print('Endpoints to remap:')
    for result in r_json["results"]:
        for row in table.rows:
            if re.match("^{}.*".format(row["short_name_prefix"]), result["name"], re.IGNORECASE):
                if not re.match("^{}$".format(row["group"]), result["group_name"], re.IGNORECASE):
                    print("fqdn: {}, current_group: {}, future_group {}".format(result["name"], result["group_name"],
                                                                                row["group"]))
                    endpoints_to_map[row["group"]].append(result["client_id"])
    print('---------------------------------------')
    return endpoints_to_map


def get_endpoint_groups(hostname, api_token):
    try:
        response = requests.get("https://{}/api/atcep/v1/roaming_device_groups".format(hostname), headers=headers,
                                verify=True, timeout=(30, 30))
        try:
            r_json = response.json()
        except:
            raise Exception("Response is not valid json. Response:{}".format(response.text))
    except:
        raise Exception("Unable to perform polling from url:{}, status code:{}".format(url, response.status_code))
    return r_json["results"]


def map_endpoints_to_groups(hostname, api_token, endpoints_to_map, endpoint_groups):
    for group in endpoints_to_map:
        if len(endpoints_to_map[group]) > 0:

            if group == "disabled" or group == "deleted":
                print("Disabling {}".format(endpoints_to_map[group]))
                url = "https://{}/api/atcep/v1/roaming_devices".format(hostname)
                data = {}
                data["administrative_status"] = "DISABLED"
                data["client_ids"] = endpoints_to_map[group]

                try:
                    response = requests.put(url,
                                            headers=headers,
                                            data=json.dumps(data, indent=4),
                                            verify=True, timeout=(30, 30))
                    try:
                        print(response.json())
                    except:
                        raise Exception("Response is not valid json. Response:{}".format(response.text))
                except:
                    raise Exception("Unable to perform polling from url:{}, status code:{}".format(url,
                                                                                                   response.status_code))

                if group == "deleted":
                    print("Deleting {}".format(endpoints_to_map[group]))

                    url = "https://{}/api/atcep/v1/roaming_devices".format(hostname)
                    data = {}
                    data["administrative_status"] = "DELETED"
                    data["client_ids"] = endpoints_to_map[group]
                    try:
                        response = requests.put(url,
                                                headers=headers,
                                                data=json.dumps(data, indent=4),
                                                verify=True, timeout=(30, 30))
                        try:
                            print(response.json())
                        except:
                            raise Exception("Response is not valid json. Response:{}".format(response.text))
                    except:
                        raise Exception("Unable to perform polling from url:{}, status code:{}".format(url,
                                                                                                       response.status_code))


            else:
                print("Adding {} to group: {}".format(endpoints_to_map[group], group))
                for endpoint_group in endpoint_groups:
                    if endpoint_group['name'] == group:
                        print("Group before: \n{}".format(json.dumps(endpoint_group, indent=4, sort_keys=True)))
                        endpoint_group["roaming_devices"] = endpoint_group["roaming_devices"] + endpoints_to_map[group]
                        print("Group after: \n{}".format(json.dumps(endpoint_group, indent=4, sort_keys=True)))
                        url= "https://{}/api/atcep/v1/roaming_device_groups/{}".format(hostname,endpoint_group['id'])
                        try:
                            response = requests.put(url,
                                                    headers=headers,
                                                    data=json.dumps(endpoint_group, indent=4, sort_keys=True),
                                                    verify=True, timeout=(30, 30))
                            try:
                                print(response.json())
                            except:
                                raise Exception("Response is not valid json. Response:{}".format(response.text))
                        except:
                            raise Exception("Unable to perform polling from url:{}, status code:{}".format(url,
                                                                                                           response.status_code))


mapping_table = build_mapping_table(file)
endpoints_to_map = get_endpoints_to_map(hostname, api_token, mapping_table)
endpoint_groups = get_endpoint_groups(hostname, api_token)
map_endpoints_to_groups(hostname, api_token, endpoints_to_map, endpoint_groups)
