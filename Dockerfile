# Use an official Python runtime as a base image
FROM ubuntu:16.04

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
RUN apt-get update -qq && apt-get install -y curl make python2.7 python-pip python-dev build-essential

# Run app.py when the container launches
#CMD ["bash", "run.sh", ]
CMD bash run.sh $version
