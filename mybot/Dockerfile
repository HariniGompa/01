FROM rasa/rasa:3.6.20-full

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir rasa-sdk==3.6.2 && \
    if [ -f requirements.txt ]; then pip install -r requirements.txt; fi

COPY supervisord.config /etc/supervisor/conf.d/supervisord.conf

CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
