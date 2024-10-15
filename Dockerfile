FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install poetry

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

COPY . /app/

ENV PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=core.settings

CMD ["poetry", "run", "python", "manage.py", "migrate", "--noinput"] && \
    ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
