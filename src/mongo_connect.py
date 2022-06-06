import os
from turtle import dot
import dotenv
import pymongo
dotenv.load_dotenv()

def get_mongodb():
    client = pymongo.MongoClient(os.getenv("MONGO_URL"))
    return client[os.getenv("MONGO_DB")]

if __name__=='__main__':
    try:
        connection = get_mongodb()
        print('connect successful ', connection.name)
    except:
        print('connection false')