FROM python:3.8.0 as base

ARG endpoint
ARG masterKey
ARG databaseId
ARG containerId

ENV endpoint=$endpoint
ENV masterKey=$masterKey
ENV databaseId=$databaseId
ENV containerId=$containerId

USER root
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY src ./
RUN python datageneration/events_28d.py
RUN python datageneration/events_180d.py


FROM python:3.8.0
RUN useradd -ms /bin/bash app
WORKDIR /app
COPY --from=base /usr/local/lib/python3.8/site-packages /usr/local/lib/python3.8/site-packages
COPY --from=base /app ./ 
COPY src ./

USER app
EXPOSE 8050
CMD ["/bin/bash", "./scripts/start.sh"]