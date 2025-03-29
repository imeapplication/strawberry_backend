FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Ensure manage.py is executable
RUN chmod +x manage.py

# Create startup script directly in the Dockerfile
RUN echo '#!/bin/bash\n\
echo "Waiting for postgres..."\n\
sleep 5\n\
python manage.py makemigrations core\n\
python manage.py migrate\n\
DJANGO_SUPERUSER_USERNAME=admin \\\n\
DJANGO_SUPERUSER_EMAIL=admin@example.com \\\n\
DJANGO_SUPERUSER_PASSWORD=adminpassword \\\n\
python manage.py createsuperuser --noinput || true\n\
python manage.py runserver 0.0.0.0:8000\n'\
> /app/start.sh

# Make sure the script is executable
RUN chmod +x /app/start.sh

# Run the startup script
CMD ["/bin/bash", "/app/start.sh"]