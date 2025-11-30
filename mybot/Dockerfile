FROM rasa/rasa:3.6.20-full

WORKDIR /app
COPY . /app

# Install actions dependencies
RUN pip install --no-cache-dir -r actions/requirements.txt

# Optional ports
EXPOSE 5005 5055

# Shell form CMD (Render will inject $PORT)
CMD rasa run --enable-api --cors "*" --endpoints endpoints.yml --port $PORT
