from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = '34.170.99.60'
app.config['MYSQL_USER'] = 'test'
app.config['MYSQL_PASSWORD'] = 'root'  # last 4 of onid
app.config['MYSQL_DB'] = 'new_schema'
# app.config['MYSQL_CURSORCLASS'] = "DictCursor"

mysql = MySQL(app)

def insert(insertCmd):
  try:
    cursor = mysql.connection.cursor()
    cursor.execute(insertCmd)
    mysql.connection.commit()
    return True
  except Exception as e:
    print("Problem inserting into db: " + str(e))
    return False
  return False


# Routes
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/clients', methods=['GET', 'POST'])
def clients():
    if request.method == 'POST':
        if 'name' in request.form:
            name = request.form['name']
            # Process the data and insert into the database using MySQL queries
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO Clients (name) VALUES (%s)", (name,))
            mysql.connection.commit()
            cur.close()
        return redirect(url_for('clients'))
    else:
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
        # ...

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
        # ...

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
        # ...

        return render_template('regions.html', regions=regions)


@app.route('/sales_history', methods=['GET', 'POST'])
def sales_history():
    if request.method == 'POST':
        # Add new sales history record to the database
        # ...
        return redirect(url_for('sales_history'))
    else:
        # Retrieve sales history records from the database
        # ...

        return render_template('sales_history.html', sales_history=sales_history)


if __name__ == '__main__':
    app.run(debug=True)
