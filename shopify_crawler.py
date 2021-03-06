from pymongo import MongoClient, errors
import json
import requests
from time import sleep

def get_url(url, page):
    products_json = requests.get(url+'/products.json?page=' + str(page), timeout=10).json()
    return products_json

def main():
    url = 'https://www.wearebraindead.com'
    page = 0
    print("Connecting to database...")
    client = MongoClient('mongodb://root:password@mongo:27017/')
    db = client.everything_everywhere
    response = None

    print("Retrieving products...")
    while True:
        try:
            response = get_url(url, page)
        except Exception as e:
            print(e)

        if len(response["products"]) == 1: # Reached end of products
            break
        else: # Store product data
            try:
                db.products.insert_many(response["products"])
            except Exception as e:
                print(e)
        page+=1
        sleep(240)
                
    client.close()
    print("Success!")

main()