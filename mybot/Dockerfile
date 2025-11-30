# Use official Rasa full image
FROM rasa/rasa:3.6.20-full

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

# Install Python dependencies for actions
RUN pip install --no-cache-dir -r actions/requirements.txt

# Expose ports (optional, Render uses $PORT dynamically)
EXPOSE 5005 5055

# Start Rasa server with dynamic port
CMD rasa run --enable-api --cors "*" --endpoints endpoints.yml --port $PORT
