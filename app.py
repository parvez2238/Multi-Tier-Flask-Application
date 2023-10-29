#This file will contain Flask server code
from flask import Flask, request, jsonify, render_template, send_from_directory
import mysql.connector

app = Flask(__name__, static_folder='static')
db = mysql.connector.connect(
    host="localhost",  # Write the hostname
    user="root",       # MySQL username.
    password="Parvez@2238",  # MySQL password.
    database="User_Form"  # MySQL database name.
)
cursor = db.cursor()

TABLE_NAME = "User_Data"  # MySQL table name.

@app.route('/')
def index():
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
    
# Route to handle the data fatch request
@app.route('/api/data', methods=['GET'])
def get_data():
    try:
        #Select the data from MYSQL Table
        cursor.execute("SELECT * FROM User_Data")
        data = cursor.fetchall()

        # Fatch and print data from database
        print("Fetched data from database:", data)

        # Get data from colume 1 and 2 cause 0 is the ID.
        response_data = [{"name": row[1], "email": row[2]} for row in data]
        return jsonify(response_data), 200
    
    # Exception Handeller
    except Exception as e:
        print("Error:", str(e))
        response = {"error": "Internal Server Error"}
        return jsonify(response), 500

# Route for showing the data 5000/data
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
    app.run(debug=True, port=5000)







