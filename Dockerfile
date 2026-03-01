# 1. Start with a lightweight, official Python image
FROM python:3.9-slim

# 2. Set a working directory inside the container
WORKDIR /app

# 3. Copy only the requirements file first (this is a caching optimization)
COPY requirements.txt .

# 4. Install the dependencies inside the container
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of your application code into the container
COPY app.py .

# 6. Tell Docker that this container will listen on port 5000
EXPOSE 5000

# 7. The command to run when the container starts
CMD ["python", "app.py"]