FROM python:3.8
ENV port 8000
EXPOSE ${port}
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN  pip install --no-cache-dir -r requirements.txt
COPY scoutapm_exporter.py .
CMD [ "python", "scoutapm_exporter.py" ]
