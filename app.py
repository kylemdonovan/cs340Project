from flask import Flask, render_template, request, json, redirect
from flask_mysqldb import MySQL
import os

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'classmysql.engr.oregonstate.edu'
app.config['MYSQL_USER'] = 'cs340_donovaky'
app.config['MYSQL_PASSWORD'] = '5175' #last 4 of onid
app.config['MYSQL_DB'] = 'cs340_donovaky'
app.config['MYSQL_CURSORCLASS'] = "DictCursor"

mysql = MySQL(app)

# Read (Retrieve) - Display all foods
@app.route('/foods', methods=['GET'])
def foods():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM foods")
    foods = cur.fetchall()
    cur.close()
    return render_template('foods.html', foods=foods)

# Create - Add a new food
@app.route('/foods/add', methods=['POST'])
def add_food():
    name = request.form['name']
    price = request.form['price']
    
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO foods (name, price) VALUES (%s, %s)", (name, price))
    mysql.connection.commit()
    cur.close()
    
    return redirect('/foods')

# Update - Edit an existing food
@app.route('/foods/edit/<int:food_id>', methods=['GET', 'POST'])
def edit_food(food_id):
    cur = mysql.connection.cursor()
    
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        
        cur.execute("UPDATE foods SET name = %s, price = %s WHERE id = %s", (name, price, food_id))
        mysql.connection.commit()
        cur.close()
        
        return redirect('/foods')
    
    cur.execute("SELECT * FROM foods WHERE id = %s", (food_id,))
    food = cur.fetchone()
    cur.close()
    
    return render_template('edit_food.html', food=food)

# Delete - Remove an existing food
@app.route('/foods/delete/<int:food_id>', methods=['POST'])
def delete_food(food_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM foods WHERE id = %s", (food_id,))
    mysql.connection.commit()
    cur.close()
    
    return redirect('/foods')

# Listener
if __name__ == "__main__":

    #Start the app on port 3000, it will be different once hosted
    app.run(port=58610, debug=True)