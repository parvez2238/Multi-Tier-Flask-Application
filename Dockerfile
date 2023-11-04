# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the required dependencies
RUN pip install --trusted-host pypi.python.org flask mysql-connector-python

# Expose the port the app runs on
EXPOSE 5000

# Define environment variable for MySQL connection
ENV MYSQL_HOST=MYSQL_HOST \
    MYSQL_USER=root \
    MYSQL_PASSWORD=Parvez@2238 \
    MYSQL_DATABASE=User_Form

# Command to run the application
CMD ["python", "app.py"]
