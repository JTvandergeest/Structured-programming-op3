from flask import Flask, request, session, render_template, redirect, url_for, g
from flask_restful import Api, Resource, reqparse
import os
from pymongo import MongoClient
from dotenv import load_dotenv
import psycopg2

app = Flask(__name__)
api = Api(app)

# We define these variables to (optionally) connect to an external MongoDB
# instance.
envvals = ["MONGODBUSER","MONGODBPASSWORD","MONGODBSERVER"]
dbstring = 'mongodb+srv://{0}:{1}@{2}/test?retryWrites=true&w=majority'

connect = psycopg2.connect("dbname=voordeelshopgpx user=postgres password=pgadminJTgeest")
c = connect.cursor()

# Since we are asked to pass a class rather than an instance of the class to the
# add_resource method, we open the connection to the database outside of the 
# Recom class.
load_dotenv()
if os.getenv(envvals[0]) is not None:
    envvals = list(map(lambda x: str(os.getenv(x)), envvals))
    client = MongoClient(dbstring.format(*envvals))
else:
    client = MongoClient()
database = client.huwebshop 

class Recom(Resource):
    """ This class represents the REST API that provides the recommendations for
    the webshop. At the moment, the API simply returns a random set of products
    to recommend."""

    def get(self, pid, count):
        """ This function represents the handler for GET requests coming in
        through the API. It currently returns a random sample of products. """
        c.execute("select id, prod1, prod2, prod3, prod4, prod5 from rec_eng1_ses_prods where id = '{}'".format(pid)) #brandrecommendation
        print(pid)
        data = c.fetchall()

        print(data)
        prodids = list(data)
        print(prodids)
        if not prodids:
            randcursor = database.products.aggregate([{'$sample': {'size': count}}])
            prodids = list(map(lambda x: x['_id'], list(randcursor)))
            return prodids, 200
        else:
            prodids = prodids[0]
            prodids = list(prodids)
            prodids.remove(prodids[0])
            print(prodids)

            if len(prodids) >= 5:
                return prodids, 200
            elif len(prodids) == 4:
                randcursor = database.products.aggregate([{'$sample': {'size': count}}])
                prodidsx = list(map(lambda x: x['_id'], list(randcursor)))
                prodids.append(prodidsx[:1])
                return prodids, 200
            elif len(prodids) == 3:
                randcursor = database.products.aggregate([{'$sample': {'size': count}}])
                prodidsx = list(map(lambda x: x['_id'], list(randcursor)))
                prodids.append(prodidsx[:2])
                return prodids, 200
            elif len(prodids) == 2:
                randcursor = database.products.aggregate([{'$sample': {'size': count}}])
                prodidsx = list(map(lambda x: x['_id'], list(randcursor)))
                prodids.append(prodidsx[:3])
                return prodids, 200
            elif len(prodids) == 1:
                randcursor = database.products.aggregate([{'$sample': {'size': count}}])
                prodidsx = list(map(lambda x: x['_id'], list(randcursor)))
                prodids.append(prodidsx[:4])
                return prodids, 200



# This method binds the Recom class to the REST API, to parse specifically
# requests in the format described below.
api.add_resource(Recom, "/<string:pid>/<int:count>")