FROM rasa/rasa:3.6.20-full

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir rasa-sdk==3.6.2 && \
    if [ -f requirements.txt ]; then pip install -r requirements.txt; fi

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

EXPOSE 5005
EXPOSE 5055

CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
