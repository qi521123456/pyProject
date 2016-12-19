from flask import Flask
from flask_pymongo import PyMongo
app=Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://root:aaa2016@localhost:27017/mongo_test'#未通过。。。。
mongo=PyMongo(app)
online_users = mongo.db.users.findOne()
print(online_users)