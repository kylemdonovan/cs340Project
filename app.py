from flask import Flask, redirect, url_for, request, render_template, json
import os
import database.db_connector as db
from flask_mysqldb import MySQL

app = Flask(__name__)
mysql = MySQL(app)


app.config['MYSQL_HOST'] = 'classmysql.engr.oregonstate.edu'
app.config['MYSQL_USER'] = 'cs340_donovaky'
app.config['MYSQL_PASSWORD'] = '5175'  # last 4 of onid
app.config['MYSQL_DB'] = 'cs340_donovaky'
app.config['MYSQL_CURSORCLASS'] = "DictCursor"


# Configuration

db_connection = db.connect_to_database()

# Routes 

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
    return render_template('index.j2')

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
            cur.execute("INSERT INTO Clients (region_id, name, address, phone, email) VALUES (%s, %s, %s, %s, %s)",
                        (region_id, name, address, phone, email))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('clients'))
    else:
        cur = mysql.connection.cursor()
        cur.execute("SELECT region_id, region_name FROM Regions")
        regions = cur.fetchall()
        cur.execute("SELECT * FROM Clients")
        clients = cur.fetchall()
        cur.close()
        return render_template('clients.j2', clients=clients, regions=regions)


# Add clients
@app.route('/add_client', methods=['POST'])
def add_client():
    region_id = request.form['region_id']
    name = request.form['name']
    address = request.form['address']
    phone = request.form['phone']
    email = request.form['email']

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO Clients (region_id, name, address, phone, email) VALUES (%s, %s, %s, %s, %s)",
                (region_id, name, address, phone, email))
    mysql.connection.commit()
    cur.close()

    return redirect(url_for('clients'))


@app.route('/edit_client/<int:client_id>', methods=['GET', 'POST'])
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
            cur.execute("UPDATE Clients SET region_id = %s, name = %s, address = %s, phone = %s, email = %s WHERE client_id = %s",
                        (region_id, name, address, phone, email, client_id))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('clients'))
    else:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Clients WHERE client_id = %s", (client_id,))
        client = cur.fetchone()
        cur.close()
        return render_template('edit_client.j2', client=client)


@app.route('/clients/delete/<int:client_id>', methods=['GET', 'POST'])
def delete_client(client_id):
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM Clients WHERE client_id = %s", (client_id,))
        mysql.connection.commit()
        cur.close()
        return redirect("/clients")
    else:
        # It's a GET request, render the delete confirmation page
        return render_template('delete_client.j2', client_id=client_id)
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

        cur.execute("SELECT region_id FROM Regions")
        regions = cur.fetchall()

        cur.close()
        return render_template('foods.j2', foods=foods, regions=regions)

@app.route('/add_food', methods=['POST'])
def add_food():
    region_id = request.form['region_id']
    food_name = request.form['food_name']
    price = request.form['price']

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO Foods (region_id, food_name, price) VALUES (%s, %s, %s)",
                (region_id, food_name, price))
    mysql.connection.commit()
    cur.close()

    return redirect(url_for('foods'))

@app.route('/edit_food/<int:food_id>', methods=['GET', 'POST'])
def edit_food(food_id):
    if request.method == 'POST':
        # Retrieve the form data
        region_id = request.form['region_id']
        food_name = request.form['name']
        price = request.form['price']

        # Update the food item in the database
        cur = mysql.connection.cursor()
        cur.execute("UPDATE Foods SET region_id = %s, food_name = %s, price = %s WHERE food_id = %s", (region_id, food_name, price, food_id))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('foods'))
    else:
        # Retrieve the food item from the database
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Foods WHERE food_id = %s", (food_id,))
        food = cur.fetchone()
        cur.close()

        return render_template('edit_food.j2', food=food)





@app.route('/foods/delete/<int:food_id>')
def delete_food(food_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM Foods WHERE food_id = %s", (food_id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('foods'))


# Inventory
@app.route('/inventories', methods=['GET', 'POST'])
def inventories():
    if request.method == 'POST':
        if 'food_id' in request.form:
            food_id = request.form['food_id']
            item_count = request.form['item_count']
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO Inventories (food_id, client_id, item_count) VALUES (%s, %s, %s)", (food_id, client_id, item_count))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('inventories'))
    else:
        cur = mysql.connection.cursor()
        cur.execute("SELECT Clients.name, Foods.food_name, Foods.food_id, Inventories.inventory_id, Inventories.item_count FROM Inventories JOIN Foods ON Inventories.food_id = Foods.food_id JOIN Clients ON Inventories.client_id = Clients.client_id")
        inventory_data = cur.fetchall()

        cur.execute("SELECT * FROM Foods")
        foods = cur.fetchall()

        cur.execute("SELECT * FROM Clients")
        clients = cur.fetchall()
        #print(inventory_data)
        cur.close()
        return render_template('inventories.j2', inventory_data=inventory_data, foods=foods, clients=clients)


@app.route('/add_inventory', methods=['POST'])
def add_inventory():
    food_id = request.form['food_id']
    client_id = request.form['client_id']
    item_count = request.form['item_count']

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO Inventories (food_id, client_id, item_count) VALUES (%s, %s, %s)", (food_id, client_id, item_count))
    mysql.connection.commit()
    cur.close()

    return redirect(url_for('inventories'))
@app.route('/inventories/edit/<int:inventory_id>', methods=['GET', 'POST'])
def edit_inventory(inventory_id):
    if request.method == 'POST':
        if 'food_id' in request.form:
            food_id = request.form['food_id']
            item_count = request.form['item_count']
            # Process the data and update the database using MySQL queries
            cur = mysql.connection.cursor()
            cur.execute("UPDATE Inventories SET food_id = %s, item_count = %s WHERE inventory_id = %s",
                        (food_id, item_count, inventory_id))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('inventories'))
    else:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Inventories WHERE inventory_id = %s", (inventory_id,))
        inventory = cur.fetchone()
        cur.close()
        return render_template('edit_inventory.j2', inventory=inventory)

@app.route('/delete_inventory/<int:inventory_id>')
def delete_inventory(inventory_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM Inventories WHERE inventory_id = %s", (inventory_id))
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
            cur.execute("INSERT INTO Regions (region_name) VALUES (%s)", (region_name))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('regions'))  # Replace this line with the desired redirect route
    else:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Regions")
        regions = cur.fetchall()
        cur.close()
        return render_template('regions.j2', regions=regions)



@app.route('/add_region', methods=['GET', 'POST'])
def add_region():
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
        return render_template('add_region.j2')


@app.route('/edit_region/<int:region_id>', methods=['GET', 'POST'])
def edit_region(region_id):
    if request.method == 'POST':
        if 'name' in request.form:
            name = request.form['name']
            # Process the data and update the database using MySQL queries
            cur = mysql.connection.cursor()
            cur.execute("UPDATE Regions SET name = %s WHERE region_id = %s", (name, region_id))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('regions'))
    else:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Regions WHERE region_id = %s", (region_id,))
        region = cur.fetchone()
        cur.close()
        return render_template('edit_region.j2', region=region)


@app.route('/regions/delete/<int:region_id>', methods=['GET', 'POST'])
def delete_region(region_id):
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM Regions WHERE region_id = %s", (region_id,))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('regions'))
    else:
        # It's a GET request, render the delete confirmation page
        return render_template('delete_region.j2', region_id=region_id)


# SALES HISTORY
@app.route('/sales_history', methods=['GET', 'POST'])
def sales_history():
    if request.method == 'POST':
        client_id = request.form['client_id']
        date = request.form['date']
        total_cost = request.form['total_cost']
        refund = request.form['refund']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Sales_history (client_id, date, total_cost, refund) VALUES (%s, %s, %s, %s)",
                    (client_id, date, total_cost, refund))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('sales_history'))
    else:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Sales_history")
        sales_history = cur.fetchall()
        
        cur.execute("SELECT * FROM Foods")
        foods = cur.fetchall()

        cur.execute("SELECT * FROM Clients")
        clients = cur.fetchall()
        #print(sales_history)
        cur.close()

        return render_template('sales_history.j2', sales_history=sales_history, foods = foods, clients = clients)



@app.route('/add_sale', methods=['POST'])
def add_sale():
        client_id = request.form['client_id']
        date = request.form['date']
        total_cost = request.form['total_cost']
        refund = request.form['refund']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Sales_history (client_id, date, total_cost, refund) VALUES (%s, %s, %s, %s)",
                    (client_id, date, total_cost, refund))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('sales_history'))

@app.route('/edit_sale/<int:sales_history_id>', methods=['GET', 'POST'])
def edit_sale(sales_history_id):
    if request.method == 'POST':
        client_id = request.form['client_id']
        date = request.form['date']
        total_cost = request.form['total_cost']
        refund = request.form['refund']
        # Process the data and update the database using MySQL queries
        cur = mysql.connection.cursor()
        cur.execute("UPDATE Sales_history SET client_id = %s, date = %s, total_cost = %s, refund = %s WHERE sales_history_id = %s",
                    (client_id, date, total_cost, refund, sales_history_id))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('sales_history'))
    else:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Sales_history WHERE sales_history_id = %s", (sales_history_id,))
        sale = cur.fetchone()
        cur.close()
        return render_template('edit_sale.j2', sale=sale)


@app.route('/sales_history/delete/<int:sales_history_id>', methods=['GET', 'POST'])
def delete_sale(sales_history_id):
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM Sales_history WHERE sales_history_id = %s", (sales_history_id,))
        mysql.connection.commit()
        cur.close()
        return redirect("/sales_history")
    else:
        # It's a GET request, render the delete confirmation page
        return render_template('delete_sale.j2', sales_history_id=sales_history_id)

@app.route('/sales_history_has_food', methods=['GET', 'POST'])
def sales_history_has_food():
    if request.method == 'POST':
        # Handle the form submission for adding a sale history with food
        food_id = request.form['food_id']
        sales_history_id = request.form['sales_history_id']
        count = request.form['count']
        # Process the data and insert into the Sales_history_has_food table using MySQL queries
        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Sales_history_has_food (food_id, sales_history_id, count) VALUES (%s, %s, %s)",
                    (food_id, sales_history_id, count))
        mysql.connection.commit()
        cur.close()
        
        return redirect(url_for('sales_history_has_food'))
    else:
        cur = mysql.connection.cursor()
        cur.execute("SELECT Clients.name, Foods.food_name, Sales_history_has_food.count, Sales_history_has_food.sales_history_id, Sales_history_has_food.food_id From Sales_history_has_food Inner Join Sales_history on Sales_history.sales_history_id = Sales_history_has_food.sales_history_id Inner Join Clients on Sales_history.client_id = Clients.client_id inner JOIN Foods on Foods.food_id = Sales_history_has_food.food_id;")
        sales_history_has_food = cur.fetchall()
        cur.execute("SELECT * FROM Foods")
        foods = cur.fetchall()
        cur.execute("SELECT * FROM Clients")
        clients = cur.fetchall()
        #print(sales_history_has_food)
        cur.close()
        
        return render_template('sales_history_has_food.j2', sales_history_has_food=sales_history_has_food, clients = clients, foods = foods)

@app.route('/edit_sales_history_has_food/<int:sales_history_id>/<int:food_id>', methods=['GET', 'POST'])
def edit_sales_history_has_food(sales_history_id, food_id):

    if request.method == 'POST':

        count = request.form['count']
        # Process the data and update the database using MySQL queries
        cur = mysql.connection.cursor()
        cur.execute("UPDATE Sales_history_has_food SET count = %s WHERE sales_history_id = %s and food_id = %s",
                    (count,  sales_history_id, food_id))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('sales_history_has_food'))
    else:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Sales_history_has_food WHERE sales_history_id = %s and food_id = %s", (sales_history_id, food_id))
        sale = cur.fetchone()
        cur.close()
        return render_template('edit_sales_history.j2', sale=sale)



@app.route('/sales_history_has_food/delete/<int:sales_history_id>/<int:food_id>', methods=['GET', 'POST'])
def delete_sales_history_has_food(sales_history_id, food_id):
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM Sales_history_has_food WHERE sales_history_id = %s and food_id = %s", (sales_history_id,food_id,))
        mysql.connection.commit()
        cur.close()
        return redirect("/sales_history_has_food")
    else:
        # It's a GET request, render the delete confirmation page
        return render_template('delete_sales_history_has_food.j2', sales_history_id=sales_history_id, food_id = food_id)

# Listener

if __name__ == "__main__":
    port_number = 45656
    app.run(debug=True, port=port_number)
    