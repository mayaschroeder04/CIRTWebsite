# Stage 1: Base build stage
FROM python AS builder

RUN apt-get update --fix-missing
# Create the app directory
RUN mkdir /app
 
# Set the working directory
WORKDIR /app
 
# Set environment variables to optimize Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 

# Upgrade pip and install dependencies
RUN pip install --upgrade pip 

# Copy the requirements file first (better caching)
COPY requirements.txt /app/
 
# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y netcat-traditional

 
# Stage 2: Production stage
FROM python

RUN echo 'root:Docker!' | chpasswd

RUN apt update && apt install -y sudo && \
   useradd -m -s /bin/bash appuser && \
   mkdir /app && \
   chown -R appuser /app &&\
   echo 'appuser ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers


# Copy the Python dependencies from the builder stage
COPY --from=builder /usr/local/lib/python3.13/site-packages/ /usr/local/lib/python3.13/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/
 
# Set the working directory
WORKDIR /app

# Copy application code
COPY --chown=appuser:appuser . .
 
# Set environment variables to optimize Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 

# Switch to non-root user
# Collect static files for production
RUN python manage.py collectstatic --noinput

# Expose the application port
EXPOSE 8000
EXPOSE 8001
 
# Start the application using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "cirtwebsite.wsgi:application"]
