#Python base image
FROM python:3.11-alpine

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# 5. Expose the port the Flask dev server runs on
EXPOSE 5000

# 6. Define the command to run your app
CMD ["python", "main.py"]