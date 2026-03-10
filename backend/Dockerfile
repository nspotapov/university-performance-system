ARG PYTHON_VERSION=3.12.3

FROM python:$PYTHON_VERSION-slim-bookworm

WORKDIR /src

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

RUN groupadd -r fastapi \
    && useradd -r -g fastapi fastapi

COPY --chown=fastapi:fastapi ./src/ .

RUN chmod +x entrypoint.sh

ENTRYPOINT ["/src/entrypoint.sh"]

USER fastapi

EXPOSE 8000

ENV PYTHONPATH=/src/app \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
