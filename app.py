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

# Clients
@app.route('/clients', methods=['GET', 'POST'])
def clients():
    if request.method == 'POST':
        if 'name' in request.form:
            name = request.form['name']
            region_id = request.form['region_id']
            address = request.form['address']
            phone = request.form['phone']
            email = request.form['email']
            # Process the data and insert into the database using MySQL queries
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO Clients (region_id, name, address, phone, email) VALUES (%s,%s, %s, %s, %s)", (region_id,name, address, phone, email))
            mysql.connection.commit()
            cur.close()
        return redirect(url_for('clients'))
    else:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Clients")
        clients = cur.fetchall()
        print(clients[0])
        cur.close()
        return render_template('clients.html', clients=clients)


@app.route('/clients/edit/<int:client_id>', methods=['GET', 'POST'])
def edit_client(client_id):
    if request.method == 'POST':
        if 'name' in request.form:
            name = request.form['name']
            region_id = request.form['region_id']
            address = request.form['address']
            phone = request.form['phone']
            email = request.form['email']
            # Process the data and update the database using MySQL queries
            cur = mysql.connection.cursor()
            cur.execute("UPDATE Clients SET region_id = %s, name = %s, address = %s, phone = %s, email = %s WHERE client_id = %s", (region_id, name, address, phone, email, client_id))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('clients'))
    else:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Clients WHERE client_id = %s", (client_id,))
        client = cur.fetchone()
        cur.close()
        return render_template('edit_client.html', client=client)


@app.route('/clients/delete/<int:client_id>')
def delete_client(client_id):

    print(client_id)

    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM Clients WHERE client_id = %s", (client_id,))
    mysql.connection.commit()
    cur.close()
    return redirect("/clients")


# Foods
@app.route('/foods', methods=['GET', 'POST'])
def foods():
    if request.method == 'POST':
        if 'food_name' in request.form and 'price' in request.form:
            region_id = request.form['region_id']
            food_name = request.form['food_name']
            price = request.form['price']
            # Process the data and insert into the database using MySQL queries
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO Foods (region_id, food_name, price) VALUES (%s, %s, %s)", (region_id, food_name, price))
            mysql.connection.commit()
            cur.close()
        return redirect(url_for('foods'))
    else:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Foods")
        foods = cur.fetchall()
        cur.close()
        return render_template('foods.html', foods=foods)


@app.route('/foods/edit/<int:food_id>', methods=['GET', 'POST'])
def edit_food(food_id):
    if request.method == 'POST':
        if 'food_name' in request.form and 'price' in request.form:
            region_id = request.form['region_id']
            food_name = request.form['food_name']
            price = request.form['price']
            # Process the data and update the database using MySQL queries
            cur = mysql.connection.cursor()
            cur.execute("UPDATE Foods SET region_id = %s, food_name = %s, price = %s WHERE food_id = %s", (region_id, food_name, price, food_id))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('foods'))
    else:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Foods WHERE food_id = %s", (food_id,))
        food = cur.fetchone()
        cur.close()
        return render_template('edit_food.html', food=food)


@app.route('/foods/delete/<int:food_id>')
def delete_food(food_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM Foods WHERE food_id = %s", (food_id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('foods'))


# Inventories
@app.route('/inventories', methods=['GET', 'POST'])
def inventories():
    if request.method == 'POST':
        if 'client_id' in request.form and 'food_id' and 'item_count' and 'units' in request.form:
            client_id = request.form['client_id']
            food_id = request.form['food_id']
            item_count = request.form['item_count']
            units = request.form['units']
            # Process the data and insert into the database using MySQL queries
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO Inventories (client_id, food_id, item_count, units) VALUES (%s, %s, %s, %s)", (client_id, food_id, item_count, units))
            mysql.connection.commit()
            cur.close()
        return redirect(url_for('inventories'))
    else:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Inventories")
        inventories = cur.fetchall()
        cur.close()
        return render_template('inventories.html', inventories=inventories)


@app.route('/inventories/edit/<int:inventory_id>', methods=['GET', 'POST'])
def edit_inventory(inventory_id):
    if request.method == 'POST':
        if 'client_id' in request.form and 'food_id' and 'item_count' and 'units' in request.form:
            client_id = request.form['client_id']
            food_id = request.form['food_id']
            item_count = request.form['item_count']
            units = request.form['units']
            # Process the data and update the database using MySQL queries
            cur = mysql.connection.cursor()
            cur.execute("UPDATE Inventories SET client_id = %s, food_id = %s, item_count = %s, units = %s WHERE inventory_id = %s", (client_id, food_id, item_count, units, inventory_id))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('inventories'))
    else:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Inventories WHERE inventory_id = %s", (inventory_id,))
        inventory = cur.fetchone()
        cur.close()
        return render_template('edit_inventory.html', inventory=inventory)


@app.route('/inventories/delete/<int:inventory_id>')
def delete_inventory(inventory_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM Inventories WHERE inventory_id = %s", (inventory_id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('inventories'))


# Regions
@app.route('/regions', methods=['GET', 'POST'])
def regions():
    if request.method == 'POST':
        if 'region_name' in request.form:
            region_name = request.form['region_name']
            # Process the data and insert into the database using MySQL queries
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO Regions (region_name) VALUES (%s)", (region_name,))
            mysql.connection.commit()
            cur.close()
        return redirect(url_for('regions'))
    else:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Regions")
        regions = cur.fetchall()
        cur.close()
        return render_template('regions.html', regions=regions)


@app.route('/regions/edit/<int:region_id>', methods=['GET', 'POST'])
def edit_region(region_id):
    if request.method == 'POST':
        if 'region_name' in request.form:
            region_name = request.form['region_name']
            # Process the data and update the database using MySQL queries
            cur = mysql.connection.cursor()
            cur.execute("UPDATE Regions SET region_name = %s WHERE region_id = %s", (region_name, region_id))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('regions'))
    else:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Regions WHERE region_id = %s", (region_id,))
        region = cur.fetchone()
        cur.close()
        return render_template('edit_region.html', region=region)


@app.route('/regions/delete/<int:region_id>')
def delete_region(region_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM Regions WHERE region_id = %s", (region_id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('regions'))


# Sales History
@app.route('/sales_history', methods=['GET', 'POST'])
def sales_history():
    if request.method == 'POST':
        if 'client_id' in request.form and 'date' in request.form and 'total_cost' in request.form:
            client_id = request.form['client_id']
            date = request.form['date']
            total_cost = request.form['total_cost']
            refund = request.form['refund']
            if refund == "":
                refund = None

            print(refund)
            cur = mysql.connection.cursor()
            cur.execute(
                "INSERT INTO Sales_history (client_id, date, total_cost, refund) VALUES (%s, %s, %s, %s)",
                (client_id, date, total_cost, refund))
            mysql.connection.commit()
            cur.close()

        return redirect(url_for('sales_history'))
    else:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Sales_history")
        sales_history = cur.fetchall()
        cur.close()

        return render_template('sales_history.html', sales_history=sales_history)


@app.route('/sales_history/edit/<int:sales_history_id>', methods=['GET', 'POST'])
def edit_sales_history(sales_history_id):
    if request.method == 'POST':
        if 'client_id' in request.form and 'date' in request.form and 'total_cost' in request.form:
            client_id = request.form['client_id']
            date = request.form['date']
            total_cost = request.form['total_cost']
            refund = request.form['refund']
            if refund == "":
                refund = None

            cur = mysql.connection.cursor()
            cur.execute(
                "UPDATE Sales_history SET client_id = %s, date = %s, total_cost = %s, refund = %s WHERE sales_history_id = %s",
                (client_id, date, total_cost, refund, sales_history_id))
            mysql.connection.commit()
            cur.close()

            return redirect(url_for('sales_history'))
    else:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Sales_history WHERE sales_history_id = %s", (sales_history_id,))
        sale = cur.fetchone()
        cur.close()

        return render_template('edit_sales_history.html', sale = sale)


@app.route('/sales_history/delete/<int:sales_history_id>')
def delete_sale_history(sales_history_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM Sales_history WHERE sales_history_id = %s", (sales_history_id,))
    mysql.connection.commit()
    cur.close()

    return redirect(url_for('sales_history'))

if __name__ == '__main__':
    app.run(debug=True)
