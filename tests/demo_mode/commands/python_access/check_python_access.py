import requests
requests.packages.urllib3.disable_warnings()

import os
from fs.onedatarestfs import OnedataRESTFS
onedata_onezone_host = os.getenv("OZ_IP")       
onedata_access_token = os.getenv("ACCESS_TOKEN")
odfs = OnedataRESTFS(onedata_onezone_host, onedata_access_token, verify_ssl=False)

odfs.listdir('')
# expected output: ['demo-space']

odfs.writetext('/demo-space/file.txt', 'TEST')
odfs.readtext('/demo-space/file.txt')
# expected output: 'TEST'