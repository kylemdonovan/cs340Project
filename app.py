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
            cur.execute("INSERT INTO Clients (region_id, name, address, phone, email) VALUES (%s, %s, %s, %s, %s)",
                        (region_id, name, address, phone, email))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('clients'))
    else:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Clients")
        clients = cur.fetchall()
        cur.close()
        return render_template('clients.j2', clients=clients)


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
        return render_template('edit_client.html', client=client)


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
        return render_template('delete_client.html', client_id=client_id)
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
        return render_template('foods.j2', foods=foods)

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
        food_name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        category = request.form['category']

        # Update the food item in the database
        cur = mysql.connection.cursor()
        cur.execute("UPDATE Foods SET name = %s, description = %s, price = %s, category = %s WHERE food_id = %s", (food_name, description, price, category, food_id))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('foods'))
    else:
        # Retrieve the food item from the database
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


@app.route('/inventories')
def inventories():
    cur = mysql.connection.cursor()
    cur.execute("SELECT Inventories.inventory_id, Foods.food_name, Inventories.item_count FROM Inventories JOIN Foods ON Inventories.food_id = Foods.food_id")
    inventories = cur.fetchall()
    cur.close()
    return render_template('inventories.html', inventories=inventories)
@app.route('/inventories/add', methods=['POST'])
def add_inventory():
    food_id = request.form['food_id']
    client_id = request.form['client_id']

    cur = mysql.connection.cursor()

    # Check if the food already exists in the inventory
    cur.execute("SELECT item_count FROM Inventories WHERE food_id = %s AND client_id = %s", (food_id, client_id))
    existing_count = cur.fetchone()

    if existing_count:
        # If the food exists, increment the item_count
        cur.execute("UPDATE Inventories SET item_count = item_count + 1 WHERE food_id = %s AND client_id = %s",
                    (food_id, client_id))
    else:
        # Check if the food exists in the Foods table
        cur.execute("SELECT food_id FROM Foods WHERE food_id = %s", (food_id,))
        existing_food = cur.fetchone()

        if existing_food:
            # If the food exists, insert a new row with item_count = 1
            cur.execute("INSERT INTO Inventories (food_id, client_id, item_count) VALUES (%s, %s, 1)", (food_id, client_id))
        else:
            # If the food doesn't exist, display an error message
            error_message = "The selected food item does not exist. Please add it to the Foods table before adding it to a client's inventory."
            return render_template('error.html', message=error_message)

    mysql.connection.commit()
    cur.close()

    return redirect(url_for('inventories'))








@app.route('/inventories/edit/<int:inventory_id>', methods=['GET', 'POST'])
def edit_inventory(inventory_id):
    if request.method == 'POST':
        if 'food_id' in request.form:
            food_id = request.form['food_id']
            quantity = request.form['quantity']
            # Process the data and update the database using MySQL queries
            cur = mysql.connection.cursor()
            cur.execute("UPDATE Inventories SET food_id = %s, quantity = %s WHERE inventory_id = %s",
                        (food_id, quantity, inventory_id))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('inventories'))
    else:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Inventories WHERE inventory_id = %s", (inventory_id,))
        inventory = cur.fetchone()
        cur.close()
        return render_template('edit_inventory.html', inventory=inventory)

@app.route('/inventories/delete/<int:inventory_id>', methods=['GET', 'POST'])
def delete_inventory(inventory_id):
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM Inventories WHERE inventory_id = %s", (inventory_id,))
        mysql.connection.commit()
        cur.close()
        return redirect("/inventories")
    else:
        # It's a GET request, render the delete confirmation page
        return render_template('delete_inventory.html', inventory_id=inventory_id)



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
            return redirect(url_for('regions'))  # Replace this line with the desired redirect route
    else:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Regions")
        regions = cur.fetchall()
        cur.close()
        return render_template('regions.html', regions=regions)

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
        return render_template('add_region.html')


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
        return render_template('edit_region.html', region=region)




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
        return render_template('delete_region.html', region_id=region_id)


# Sales History
@app.route('/sales_history', methods=['GET', 'POST'])
def sales_history():
    if request.method == 'POST':
        product_name = request.form['product_name']
        client_id = request.form['client_id']
        quantity = request.form['quantity']
        price = request.form['price']
        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Sales_history (product_name, client_id, quantity, price) VALUES (%s, %s, %s, %s)",
                    (product_name, client_id, quantity, price))
        mysql.connection.commit()
        cur.close()
        
        return redirect(url_for('sales_history'))
    else:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Sales_history")
        sales_history = cur.fetchall()
        cur.close()
        
        return render_template('sales_history.html', sales_history=sales_history)



@app.route('/add_sale', methods=['POST'])
def add_sale():
    product_name = request.form['product_name']
    client_id = request.form['client_id']
    quantity = request.form['quantity']
    price = request.form['price']

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO Sales_history (product_name, client_id, quantity, price) VALUES (%s, %s, %s, %s)",
                (product_name, client_id, quantity, price))
    mysql.connection.commit()
    cur.close()

    return redirect(url_for('sales_history'))

@app.route('/edit_sales_history/<int:sales_history_id>', methods=['GET', 'POST'])
def edit_sales_history(sales_history_id):
    if request.method == 'POST':
        if 'product_name' in request.form:
            product_name = request.form['product_name']
            client_id = request.form['client_id']
            quantity = request.form['quantity']
            price = request.form['price']
            # Process the data and update the database using MySQL queries
            cur = mysql.connection.cursor()
            cur.execute("UPDATE Sales_history SET product_name = %s, client_id = %s, quantity = %s, price = %s WHERE sales_history_id = %s",
                        (product_name, client_id, quantity, price, sales_history_id))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('sales_history'))
    else:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Sales_history WHERE sales_history_id = %s", (sales_history_id,))
        sale = cur.fetchone()
        cur.close()
        return render_template('edit_sale.html', sale=sale)



@app.route('/sales_history/delete/<int:sale_id>', methods=['GET', 'POST'])
def delete_sale(sale_id):
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM Sales_history WHERE sales_history_id = %s", (sale_id,))
        mysql.connection.commit()
        cur.close()
        return redirect("/sales_history")
    else:
        # It's a GET request, render the delete confirmation page
        return render_template('delete_sale.html', sale_id=sale_id)

@app.route('/sales_history_has_food', methods=['GET', 'POST'])
def sales_history_has_food():
    if request.method == 'POST':
        # Handle the form submission for adding a sale history with food
        food_id = request.form['food_id']
        sales_history_id = request.form['sales_history_id']
        # Process the data and insert into the Sales_history_has_food table using MySQL queries
        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Sales_history_has_food (food_id, sales_history_id) VALUES (%s, %s)",
                    (food_id, sales_history_id))
        mysql.connection.commit()
        cur.close()
        
        return redirect(url_for('sales_history_has_food'))
    else:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Sales_history_has_food")
        sales_history_has_food = cur.fetchall()
        cur.close()
        
        return render_template('sales_history_has_food.html', sales_history_has_food=sales_history_has_food)


# Listener

if __name__ == "__main__":
    port_number = 45652
    app.run(debug=True, port=port_number)