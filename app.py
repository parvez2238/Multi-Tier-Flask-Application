#This file will contain Flask server code
from flask import Flask, request, jsonify, render_template, redirect, url_for 
import mysql.connector 
import os

app = Flask(__name__, static_folder='static')

MYSQL_HOST = os.getenv('MYSQL_HOST', 'mysql') # Get MySQL host from environment variable (default to 'mysql' if not set)

db = mysql.connector.connect(
    host= MYSQL_HOST,  # MYSQL is running on container default host is MYSQL_HOST(if it is local mechine use localhost)
    user="root",       # MySQL username.(default root)
    password="Parvez@2238",  # MySQL password.
    database="User_Form"  # MySQL database name. (Create database)
)
cursor = db.cursor()

TABLE_NAME = "User_Data"  # MySQL table name.(Create the table in database)

@app.route('/')
def index():
    print("Request received!")  #debugging
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
        
        # Redirect to the /data page after successful save
        #return render_template('data.html')
        #return redirect(url_for('data_page'))

    except Exception as e:
        # Handle errors and return error response
        print(str(e))
        response = {"error": "Internal Server Error"}
        return jsonify(response), 500
    
# Route for getting data from database
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
    
#Display the data in the port 5000/data
@app.route('/data')
def data_page():
    try:
        cursor.execute("SELECT * FROM User_Data")
        data = cursor.fetchall()
        response_data = [{"name": row[1], "email": row[2]} for row in data] #row 0 is my PK| row 1 is name| row 2 is email)
        return render_template('data.html', data=response_data)
    except Exception as e:
        print("Error:", str(e))

#initialize the port, debug is on for troubleshooting
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=5000)