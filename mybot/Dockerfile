FROM rasa/rasa:3.6.20-full

WORKDIR /app

# Copy project files
COPY . /app

# Install dependencies for action server
RUN pip install --no-cache-dir rasa-sdk==3.6.2 \
    && pip install --no-cache-dir -r requirements.txt || true

# Supervisord runs both Rasa + Actions
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

EXPOSE 5005
EXPOSE 5055

CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
