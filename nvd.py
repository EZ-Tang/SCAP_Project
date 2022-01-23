"""
Author: Eric Tang
Date: 11/21/2021
SCAP Project

Updated: 1/12/2022
"""
import urllib.request, json 
import write

key_rmv = ["tags", "nodes", "baseMetricV2"]
headers = [] # 1 x n of header names
vulns = [] # m x n of all NVD vulns

"""
This recursive function provides easier access to NVD dict keys and values.
Returns two equally size lists: keys and their values

"""
def key_recursion(key, ret = [], val = []):
    if isinstance(key, dict):
        for k in key:
            if k in key_rmv:
                continue
            elif not isinstance(key[k], dict) and not isinstance(key[k], list):
                ret.append(k)
            key_recursion(key[k], ret, val)
    elif isinstance(key, list) :
        for k in key:
            key_recursion(k, ret, val)
    else:
        val.append(key)
    return(ret, val)

# checks if data already exists
exist = bool(write.get_values("nvd_type"))
cve_list = []
if exist:
    #headers = write.get_values("nvd_type")[0] + write.get_values("nvd_data")[0] + write.get_values("nvd_date")[0]
    cve_list = write.get_values("nvd_type", "ID")


"""
Main function

Organizes the keys into a common structure
Creates a matrix of all vulnerabilities and their attributes
"""
index = 0
moreResults = 1
while moreResults != 0 and not exist: #and index < 5000: # measures totalResults per page
    with urllib.request.urlopen("https://services.nvd.nist.gov/rest/json/cves/1.0/?resultsPerPage=2000&startIndex=" + str(index)) as url:
        data = json.loads(url.read().decode())
        moreResults = data["totalResults"]
        for key in data['result']['CVE_Items']:
            list1 = []
            list2 = []
            list1, list2 = key_recursion(key, list1, list2)

            """
            Adds new header labels to the common format
            """
            v_index = []
            for h in list1:
                if h not in headers:
                    headers.append(h)
                v_index.append(headers.index(h))

            """
            Organizes the list into the common format
            Appends it to a matrix of lists
            """
            v = [""] * len(headers)
            for val in v_index:
                v[val] = list2.pop(0)
            vulns.append(v)

            """
            Ensures all vuln have the same # of headers 
            (regardless if they exist)
            """
            i = 0
            while (len(headers) > len(vulns[i])):
                vulns[i] = vulns[i] + ([""] * (len(headers) - len(vulns[i])))
                i = i + 1

        print(index)
        index += 2000 

if not exist:
    write.feed_nvd(headers, vulns) # feeds into google spreadsheet
