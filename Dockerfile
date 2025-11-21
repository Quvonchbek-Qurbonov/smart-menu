FROM python:3.11-slim

WORKDIR /app

# Copy app folder into container
COPY ./app ./app

# Install dependencies
RUN pip install --no-cache-dir -r ./app/requirements.txt

EXPOSE 8000

# Run uvicorn pointing to correct module path
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
