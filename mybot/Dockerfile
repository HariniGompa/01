# Dockerfile
FROM rasa/rasa:3.6.20-full

# Copy project files
WORKDIR /app
COPY . /app

# Install Python dependencies for actions
RUN pip install --no-cache-dir -r actions/requirements.txt

# Expose ports
EXPOSE 5005 5055

# Start Rasa server + actions server
CMD ["rasa", "run", "--enable-api", "--cors", "*", "--endpoints", "endpoints.yml"]
