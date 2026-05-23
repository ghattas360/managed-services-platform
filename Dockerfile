FROM python:3.12-slim AS builder
WORKDIR /build
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/deps -r requirements.txt

FROM python:3.12-slim
COPY --from=builder /deps /usr/local
RUN useradd --no-create-home --shell /bin/false appuser
WORKDIR /app
COPY app/ app/
USER appuser
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
