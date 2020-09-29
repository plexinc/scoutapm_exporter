scoutapm_exporter
=================

Small container to export scoutapm metrics in the prometheus format

# How to test

Create a `.env` file that contains your scoutapm apikey

```
$ cat .env
scoutapm_apikey=xxxxxxxx
```

Use docker-compose

```
docker-compose build
docker-compose up
```

# Configuration

You can set some env variables to make it work the way you want

|Env variable|Default|Mandatory|Notes|
|------------|-------|---------|-----|
|scoutapm_apikey | N/A | yes | Scoutapm API Key |
|monitored_apps | Evert app | No | comma separated list of apps name you want to monitor |
|time_between_polls | 60 | No | Interval in seconds between each polls |
|metric_name_prefix | scoutapm | No | Prefix name to add to the metric |
|port|8000|No|Port to bind the http server|

# Develop on a local version

```
git clone git@github.com:plexinc/scoutapm_exporter.git
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
export scoutapm_apikey=xxxxxx
python scoutapm_exporter.py
```
