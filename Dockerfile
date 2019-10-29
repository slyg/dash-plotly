FROM python:3.8.0
USER root
WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8050
CMD ["python", "app.py"]
