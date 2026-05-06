FROM python:3.11-slim

WORKDIR /app

COPY Flask-React-ToDo-app/ ./

RUN apt-get update && apt-get install -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir \
    flask==2.3.3 \
    flask-sqlalchemy==3.1.1 \
    flask-migrate==4.0.5 \
    flask-bcrypt==1.0.1 \
    flask-script==2.0.6 \
    pyjwt==2.8.0 \
    gunicorn==21.2.0 \
    requests==2.31.0 \
    pytest==7.4.0

RUN python -c "from index import app, db; app.app_context().push(); db.create_all(); print('DB initialized')"

RUN git config --global user.email "dev@example.com" && git config --global user.name "dev" && git add -A && git commit -m "init" || true

EXPOSE 5000

CMD ["python", "-c", "from application.app import app; app.run(host='0.0.0.0', port=5000)"]
