import requests
import json
import time
from datetime import datetime
from requests.adapters import HTTPAdapter
from urllib3 import Retry
from apscheduler.schedulers.background import BackgroundScheduler


def request_retry_session(retries=3,
                          backoff_factor=0.3,
                          status_forcelist=(500,),
                          session=None):
    session = session or requests.session()
    retry = Retry(total=retries,
                  read=retries,
                  connect=retries,
                  backoff_factor=backoff_factor,
                  status_forcelist=status_forcelist)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


def news_check():
    localtime = time.asctime(time.localtime(time.time()))
    print("checking - " + localtime)

    request = request_retry_session().get("https://reddit.com/r/worldnews/.json", headers={
        'User-Agent': 'some other than the python agent v 1.0123'})

    y = json.loads(request.content)

    data_we_want = y['data']['children']

    currentList = open("worldnewstext.txt", "r")
    currentList = currentList.read()
    f = open("worldnewstext.txt", "a")

    for i in range(0, 10):
        if data_we_want[i]['data']['title'] not in currentList:
            print(" - added data")
            f.write(data_we_want[i]['data']['title'] + " - " + datetime.utcfromtimestamp(data_we_want[i]['data']['created']).strftime('%Y-%m-%d %H:%M:%S'))
            f.write("\n")
            continue
    print("\n")
    f.flush()


scheduler = BackgroundScheduler()

scheduler.add_job(news_check, 'interval', seconds=60)
scheduler.start()

while 1:
    time.sleep(10000000)
