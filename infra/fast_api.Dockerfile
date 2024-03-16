FROM python:3.10-slim

WORKDIR /src

RUN pip install --upgrade pip && \
    pip install poetry

COPY poetry.lock pyproject.toml ./

COPY src ./src

RUN poetry install

CMD ["poetry", "run", "uvicorn", "app.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8000"]
