import pymongo
from dotenv import load_dotenv
from os import environ
import os


load_dotenv()

MONGODB_HOST = environ.get("MONGODB_HOST", "")
MONGODB_USER = environ.get("MONGODB_USER", "")
MONGODB_PWD = environ.get("MONGODB_PWD", "")
MONGODB_DBNM = environ.get("MONGODB_DBNM", "")

uri = f"mongodb+srv://{MONGODB_USER}:{MONGODB_PWD}@{MONGODB_HOST}"
print(uri)
mongo_client = pymongo.MongoClient(uri)
db = mongo_client['Cluster0']

class mongoDB:
	def __init__(self, collection_nm):
		self.collection_nm = collection_nm
		self.collection = db[self.collection_nm]

	def add_doc(self, doc):
		self.collection.insert_one(doc)

	def search(self, q):
		return self.collection.find(q)


