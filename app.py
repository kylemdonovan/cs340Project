import sqlite3
from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'classmysql.engr.oregonstate.edu'
app.config['MYSQL_USER'] = 'cs340_donovaky'
app.config['MYSQL_PASSWORD'] = '5175'  # last 4 of onid
app.config['MYSQL_DB'] = 'cs340_donovaky'
app.config['MYSQL_CURSORCLASS'] = "DictCursor"

mysql = MySQL(app)


# Routes
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/clients', methods=['GET', 'POST'])
def clients():
    if request.method == 'POST':
        # Add new client record to the database
        name = request.form['name']
        # Process the data and insert into the database using MySQL queries
        # ...

        return redirect(url_for('clients'))
    else:
        # Retrieve client records from the database
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Clients")
        clients = cur.fetchall()
        cur.close()

        return render_template('clients.html', clients=clients)


@app.route('/foods', methods=['GET', 'POST'])
def foods():
    if request.method == 'POST':
        # Add new food record to the database
        name = request.form['name']
        price = request.form['price']
        # Process the data and insert into the database using MySQL queries
        # ...

        return redirect(url_for('foods'))
    else:
        # Retrieve food records from the database
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Foods")
        foods = cur.fetchall()
        cur.close()

        return render_template('foods.html', foods=foods)


@app.route('/inventories', methods=['GET', 'POST'])
def inventories():
    if request.method == 'POST':
        # Add new inventory record to the database
        name = request.form['name']
        quantity = request.form['quantity']
        # Process the data and insert into the database using MySQL queries
        # ...

        return redirect(url_for('inventories'))
    else:
        # Retrieve inventory records from the database
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Inventories")
        inventories = cur.fetchall()
        cur.close()

        return render_template('inventories.html', inventories=inventories)


@app.route('/regions', methods=['GET', 'POST'])
def regions():
    if request.method == 'POST':
        # Add new region record to the database
        name = request.form['name']
        # Process the data and insert into the database using MySQL queries
        # ...

        return redirect(url_for('regions'))
    else:
        # Retrieve region records from the database
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Regions")
        regions = cur.fetchall()
        cur.close()

        return render_template('regions.html', regions=regions)


@app.route('/sales_history', methods=['GET', 'POST'])
def sales_history():
    if request.method == 'POST':
        # Add new sales history record to the database
        # ...
        return redirect(url_for('sales_history'))
    else:
        # Retrieve sales history records from the database
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Sales_History")
        sales_history = cur.fetchall()
        cur.close()

        return render_template('sales_history.html', sales_history=sales_history)


if __name__ == '__main__':
    app.run(port=68410, debug=True)
