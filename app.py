from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

app = Flask(__name__)

#use flask_pymongo to set up mongo connection

app.config['MONGO_URI'] = 'mongodb://localhost:27017/mars_app'
mongo = PyMongo(app)

#define routes for HTML page
@app.route("/")

def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)

#create new route and function

@app.route("/scape") #defines the route that Flask will be using. This route, “/scrape”, will run the function that we create just beneath it.
def scrape():
    mars = mongo.db.mars #we assign a new variable that points to our Mongo database
    mars_data = scraping.scrape_all() #we created a new variable to hold the newly scraped data we're referencing the scrape_all function in the scraping.py file exported from Jupyter Notebook.
    mars.update_one({}, {"$set":mars_data}, upsert=True) #Now that we've gathered new data, we need to update the database using

    return redirect('/',code=302)

if __name__ == "__main__":
    app.run()

