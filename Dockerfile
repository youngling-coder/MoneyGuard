FROM python:3.11

WORKDIR /backend

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir poetry

COPY backend/pyproject.toml backend/poetry.lock /backend/

RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-root

COPY backend /backend

RUN mkdir /profile_pictures
RUN poetry run alembic upgrade head

# Открываем порт
EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
