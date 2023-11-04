#This file will contain your Flask server code
from flask import Flask, request, jsonify, render_template
import mysql.connector
import os

app = Flask(__name__, static_folder='static')

MYSQL_HOST = os.getenv('MYSQL_HOST', 'mysql') # Get MySQL host from environment variable (default to 'mysql' if not set)

db = mysql.connector.connect(
    host= MYSQL_HOST,  # Use "localhost" if your database is on the same machine. If not, replace with the actual host address.
    user="root",       # Replace with your MySQL username.
    password="Parvez@2238",  # Replace with your MySQL password.
    database="User_Form"  # Replace with your MySQL database name.
)
cursor = db.cursor()

TABLE_NAME = "User_Data"  # Replace with your MySQL table name.

@app.route('/')
def index():
    print("Request received!")  # Add this line for debugging
    return render_template('index.html')

# Route to handle form submissions
@app.route('/api/save', methods=['POST'])
def save_data():
    try:
        # Get form data from the request
        name = request.form['name']
        email = request.form['email']

        # Insert data into the database
        cursor.execute(f"INSERT INTO {TABLE_NAME} (name, email) VALUES (%s, %s)", (name, email))
        db.commit()

        # Return success message
        response = {"message": "Data saved successfully!"}
        return jsonify(response), 200

    except Exception as e:
        # Handle errors and return error response
        print(str(e))
        response = {"error": "Internal Server Error"}
        return jsonify(response), 500

@app.route('/api/data', methods=['GET'])
def get_data():
    try:
        cursor.execute("SELECT * FROM User_Data")
        data = cursor.fetchall()
        print("Fetched data from database:", data)
        response_data = [{"name": row[1], "email": row[2]} for row in data]
        return jsonify(response_data), 200
    except Exception as e:
        print("Error:", str(e))
        response = {"error": "Internal Server Error"}
        return jsonify(response), 500

@app.route('/data')
def data_page():
    try:
        cursor.execute("SELECT * FROM User_Data")
        data = cursor.fetchall()
        response_data = [{"name": row[1], "email": row[2]} for row in data]
        return render_template('data.html', data=response_data)
    except Exception as e:
        print("Error:", str(e))


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=5000)







