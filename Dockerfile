FROM python:3.8.0
USER root
RUN useradd -ms /bin/bash app
WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY src ./
RUN ./scripts/generate-data.sh

USER app
EXPOSE 8050
CMD ["/bin/bash", "./scripts/prod-start.sh"]