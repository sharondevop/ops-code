# Use an official Python runtime as a parent image
FROM python:3.6-slim

LABEL maintainer="Sharon Mafgaoker <sharon.mafgaoker@xxx.com>"

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Define environment variable
ENV API_KEY xxx

# Run app.py when the container launches
CMD ["python", "app.py"]
