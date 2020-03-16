# import dependencies
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
print('1 - imports')

# Creating Flask instance
app = Flask(__name__)
print('2 = flask-name')

# Establish PyMongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_data")
print('3 - MongoDB')

# Route to render index.html template
@app.route("/")
def home():
    # Find one record of data from the mongo database
    mars_data = mongo.db.scrape_mars.find_one()
    # Return template and data
    return render_template("index.html", mars_data=mars_data)
print('4 - route /')

# Route that will start scrape function
@app.route("/scrape")
def scrape():
    # Runs the scrape function
    mars_data = scrape_mars.scrape()
    mars_data
    # Update the MongoDB using update and upsert
    mongo.db.scrape_mars.update({}, mars_data, upsert=True)
    # Redirects back to home page
    return redirect("/")
print('5 - route scrape')

if __name__ == "__main__":
    app.run(debug=True)
print('6 - debug')