from pymongo import MongoClient

mongo = MongoClient("mongodb+srv://vishalguptabiku98:Chiku%400298@cluster0.yaa9lqs.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")


db = mongo["webhookDB"]
collection = db["events"]
