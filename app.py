from flask import Flask, render_template, json, redirect
from flask_mysqldb import MySQL
from flask import request
import os

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'classmysql.engr.oregonstate.edu'
app.config['MYSQL_USER'] = 'cs340_donovaky'
app.config['MYSQL_PASSWORD'] = '5175' #last 4 of onid
app.config['MYSQL_DB'] = 'cs340_donovaky'
app.config['MYSQL_CURSORCLASS'] = "DictCursor"


mysql = MySQL(app)

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/clients')
def clients():
    return render_template('clients.html')

@app.route('/foods')
def foods():
    return render_template('foods.html')

@app.route('/inventories')
def inventories():
    return render_template('inventories.html')

@app.route('/regions')
def regions():
    return render_template('regions.html')

@app.route('/sales_history')
def sales_history():
    return render_template('sales_history.html')

@app.route('/sales_history_has_food')
def sales_history_has_food():
    return render_template('sales_history_has_food.html')

if __name__ == '__main__':
    app.run(debug=True)


# Listener
if __name__ == "__main__":

    #Start the app on port 3000, it will be different once hosted
    app.run(port=58610, debug=True)