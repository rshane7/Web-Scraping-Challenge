# From the separate python file in this directory, we'll import the code that is used to scrape mars
from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
#app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
mongo = PyMongo(app)

# set database (used this first time to create db)
#db=client.mars_db

#conn = 'mongodb://localhost:27017'
#client = pymongo.MongoClient(conn)

# This route will query the Mongo database and get the mars result
# and then render them to the html file

@app.route("/")
def index():
    mars_results = mongo.db.mars_results.find_one()
    return render_template("index.html", mars_results=mars_results)

# This route will trigger the webscraping, but it will then send us 
# back to the index route to render the results

@app.route("/scrape")
def scraper():
# drop any data that is already in database
    db.mars_results.drop()
    mars_data = scrape_mars.scrape()
    
    db.mars_results.insert_one(mars_data)
    
    # Use Flask's redirect function to send us to a different route once this task has completed.
    return redirect("http://localhost:5000/", code=302)

if __name__ == "__main__":
    app.run(debug=True)
