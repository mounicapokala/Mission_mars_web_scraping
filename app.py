from flask import Flask,render_template,redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

@app.route("/")
def home():
    mars_data = mongo.db.collection.find_one()

    # Return template and data
    return render_template("index.html", mars_dict1=mars_data)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function
    mars_dict1 = scrape_mars.scrape()
    # Update the Mongo database using update and upsert=True
    mongo.db.collection.update({}, mars_dict1, upsert=True)

    # Redirect back to home page
    return redirect("/")
    


if __name__=="__main__":
    app.run(debug=True)