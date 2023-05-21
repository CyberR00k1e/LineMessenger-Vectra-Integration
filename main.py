import requests
import datetime
import time
import json
from jsonpath_ng import jsonpath, parse

id_list = []
# enter your line API token below or save it in secrets manager; you can add it here (not the best practice or in the code segment below
line_token = ""
# enter your Vectra API token below or save it in secrets manager; you can add it here (not the best practice or in the code segment below
vectra_token = ''
while True:
    try:
        # check every 60 seconds for new detection
        time.sleep(60)
        # change the timedelta(days=1) and try and it should work
        timenow = datetime.datetime.now() - datetime.timedelta(seconds=60)
        timenow = timenow.replace(microsecond=0)

        timenow = timenow.isoformat() + "Z"
        print(timenow)
        payload = {'state': 'active', 'last_timestamp_gte': timenow}
        r = requests.get("https://demo.vectra.io/api/v2.5/detections", params=payload,
                         headers={"Authorization": "Token <token here>"}).json()

        resp = r["results"]
        dict_len = len(resp)
        print(dict_len)
        for i in range(dict_len):
            # detections=json.loads(resp)
            # jsonpath_expression=parse('$..summary,detection_url,category,detection')
            resp = r["results"][i]
            resp2 = resp["src_host"]

            resp3 = resp2["ip"]
            resp4 = resp2["name"]
            # print(resp2["ip"])
            # #print(resp3)
            resp5 = resp["detection"]
            # print(resp4)
            resp6 = resp["detection_category"]
            resp7 = resp["id"]
            print(resp7)

            print(id_list)

            if resp7 not in id_list:

                response = f"Detection is on Source : {resp3},hostname: {resp4}, detection name is : {resp5} and detection category is {resp6}."

                notify = {"message": response}
                line = requests.post("https://notify-api.line.me/api/notify",
                                     headers={'Authorization': 'Bearer <line token here>'}, params=notify, verify=False)
                id_list.append(resp7)
            else:
                pass

    except:
        pass





