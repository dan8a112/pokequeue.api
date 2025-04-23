FROM python:3.10.0-slim

# Set the working directory
WORKDIR /app

# Instala las herramientas de desarrollo y el controlador ODBC para SQL Server
RUN apt-get update && \
    apt-get install -y curl apt-transport-https gnupg gcc g++ make && \
    curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql17 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

RUN rm .env

# Make port 80 available to the world outside this container
EXPOSE 8000

CMD ["uvicorn", "main:app" , "--host", "0.0.0.0", "--port", "8000"]
