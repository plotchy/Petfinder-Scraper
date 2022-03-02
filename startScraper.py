import sys
from dotenv import dotenv_values
import json
import os
import requests
from datetime import datetime, timedelta

PETFINDER_KEY = dotenv_values(".env")["PETFINDER_KEY"]
PETFINDER_SECRET = dotenv_values(".env")["PETFINDER_SECRET"]
PETFINDER_LOCATION = dotenv_values(".env")["PETFINDER_LOCATION"]

# URL = "https://api.petfinder.com/v2/animals?type=dog"
URL = "https://api.petfinder.com/v2/animals"


def scrape():
    access_token = setupAuth()
    filterTime = datetime.now() - timedelta(hours=8, minutes = 30)
    # print(filterTime)
    # print(filterTime.astimezone().replace(microsecond=0).isoformat())
    searchParams = {
        "type": "dog",
        # "page": 2,
        "age": ["young", "adult"],
        "location": PETFINDER_LOCATION,
        "sort": "recent",
        "limit": 100,
        "after": filterTime.astimezone().replace(microsecond=0).isoformat(),
        "distance": 100 ,
        "status": "adoptable",
    }
    result = requests.get(url = URL, headers = {"Authorization": "Bearer " + access_token}, params= searchParams)
    print(result)
    print(result.json())
    if result.status_code == 401:
        access_token = setupAuth()
    elif result.status_code == 200:
        return result

    pass

def sendText(result):
    animalsList = result.json()["animals"]
    for dogDict in animalsList:
        for k,v in dogDict.items():
            print(k, v)
    pass

def setupAuth():
    authEndpoint = "https://api.petfinder.com/v2/oauth2/token"
    authParams = {
        "grant_type": "client_credentials",
        "client_id": PETFINDER_KEY,
        "client_secret": PETFINDER_SECRET
    }
    authResult = requests.post(url = authEndpoint, data = authParams)
    if authResult.status_code == 200:
        # print(authResult.json())
        access_token = authResult.json()['access_token']
        return access_token


def main():
    result = scrape()
    if result:
        sendText(result)


if __name__ == '__main__':
    main()