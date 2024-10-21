# Use the official Python image from the Docker Hub
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt /app/

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire Django project into the container
COPY . /app/

# Expose port 8000 to the outside world
EXPOSE 8000
# Run Django migrations and start the development server
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
