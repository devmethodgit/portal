FROM python:3.9
WORKDIR /web
COPY ./poetry.lock /web/poetry.lock
COPY ./pyproject.toml /web/pyproject.toml
EXPOSE 5000
RUN pip install poetry
RUN poetry install --no-root