from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
print('1 - imports')

# Create an instance of Flask
app = Flask(__name__)
print('2 = flask-name')

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")
print('3 - MongoDB')

# Route to render index.html template using data from Mongo
@app.route("/")
def home():
    # Find one record of data from the mongo database
    mars_data = mongo.db.mars_scrape.find_one()
    # Return template and data
    return render_template("index.html", mars_data=mars_data)
print('4 - route /')

# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():
    # Run the scrape function
    mars_data = scrape_mars.scrape()
    mars_data
    # Update the Mongo database using update and upsert=True
    mongo.db.scrape_mars.update({}, mars_data, upsert=True)
    # Redirect back to home page
    return redirect("/")
print('5 - route scrape')

if __name__ == "__main__":
    app.run(debug=True)
print('6 - debug')