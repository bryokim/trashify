FROM python:3-alpine AS builder

WORKDIR /api

RUN python3 -m venv venv
ENV VIRTUAL_ENV=/api/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY requirements.txt .
RUN pip install -r requirements.txt

# Stage 2
FROM python:3-alpine AS runner

WORKDIR /api

COPY --from=builder /api/venv venv
COPY app.py app.py

ENV VIRTUAL_ENV=/api/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ENV FLASK_APP=api/__init__.py

EXPOSE 8080

CMD ["gunicorn", "--bind" , ":8080", "--workers", "2", "app:app"]