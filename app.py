#This file will contain your Flask server code
from flask import Flask, request, jsonify, render_template, send_file
import mysql.connector

app = Flask(__name__, static_folder='static')
db = mysql.connector.connect(
    host="localhost",  # Use "localhost" if your database is on the same machine. If not, replace with the actual host address.
    user="root",       # Replace with your MySQL username.
    password="Parvez@2238",  # Replace with your MySQL password.
    database="User_Form"  # Replace with your MySQL database name.
)
cursor = db.cursor()

TABLE_NAME = "User_Data"  # Replace with your MySQL table name.

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

@app.route('/api/data', methods=['GET'])
def get_data():
    try:
        cursor.execute("SELECT * FROM User_Data")
        data = cursor.fetchall()
        response_data = [{"name": row[0], "email": row[1]} for row in data]
        return jsonify(response_data), 200
    except Exception as e:
        print("Error:", str(e))
        response = {"error": "Internal Server Error"}
        return jsonify(response), 500


if __name__ == '__main__':
    app.run(debug=True)


from flask import send_from_directory

@app.route('/data')
def data_page():
    return send_from_directory('.', 'data.html')


