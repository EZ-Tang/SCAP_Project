"""
Author: Eric Tang
Date: 1/12/2022
SCAP Project V1.0

Updated: -
"""

import write
import requests
from bs4 import BeautifulSoup

url_headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
}

n = 0
url = "http://www.nipc.org.cn/vulnerability/1000274" #1000274

headers = ["name"] # 1 x n of header names
vulns = [] # m x n of NIPC vulns
try: 
  while n < 1000:
    print(n)
    n += 1
    f = requests.get("http://www.nipc.org.cn/vulnerability/" + str(n), headers = url_headers)
    soup = BeautifulSoup(f.content, 'lxml')

    #################

    name_tag = soup.findAll("h2", class_="card-title")
    vuln_tags = soup.findAll("div", class_="col-4")
    info_tags = soup.findAll("div", class_="card-text")


    """
    obtains basic header tags
    from the first vulnerability
    """
    if n == 1:
      for vuln_tag in vuln_tags:
        headers.append((str(vuln_tag).split()[2]).replace("：", ""))



    v = []

    """
    obtains name header tag 
    """
    v.append(str(name_tag[0])[23:-5])


    """
    obtains basic vulnerability info
    """
    for vuln_tag in vuln_tags:
      if(vuln_tag.a):
        v.append(str(vuln_tag.a)[9:-9])
      elif (vuln_tag.span):
        v.append(str(vuln_tag.span)[6:-7])


    #########################

    """
    obtains unique header tags
    """
    for info_tag in info_tags[2:]:
      header = str(info_tag.h6)[4:-5] # removes <h6> tags
      if header not in headers:
        headers.append(header)
        for i in range(0, len(vulns)):
          vulns[i].append("")



    """
    obtains unique info between <p class=\"\"> and </p>
    """
    for info_tag in info_tags[2:]:
      for head in headers:
        if head in str(info_tag):
          temp = str(info_tag).split("<p class=\"\">",1)[1] # data cleaning
          temp = temp.split("</p>")[0]
          temp = temp.replace("\n", "").strip()
          if headers.index(head) - 1 > len(v):
            v = v + ([""] * headers.index(head) - 1 - len(v))
          v.append(temp)
    vulns.append(v)


    
except:
  print("FAILURE")

write.feed_nipc(headers, vulns)
