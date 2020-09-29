import requests
import json
import sys
import os
from time import sleep
from datetime import datetime, timedelta, timezone
from prometheus_client import start_http_server, Gauge

base_url = "https://scoutapp.com"
apikey = os.environ.get('scoutapm_apikey')
monitored_apps = os.environ.get('monitored_apps','').split(',')
time_between_polls = os.environ.get("time_between_polls", 60)
prefix = os.environ.get("metric_name_prefix", "scoutapm")
port = os.environ.get("port", 8000)

headers = {
    "X-SCOUT-API": apikey
}

data = []
metrics = {}

def scoutapm_call(endpoint, params=None):
    result = requests.get('%s/%s' % (base_url, endpoint), headers=headers, params=params)
    if result.json()['header']['status']['code'] != 200:
        print("Error calling %s" % endpoint)
        print(json.dumps(result.json(), indent=2))
        sys.exit(1)
    return result.json()['results']



def extract_metrics(metric_info):
    app_name, app_id, metric_name = metric_info

    print("Extracting %s_%s metric for app %s" % (prefix, metric_name, app_name))
    
    # Get the time series dataset for this metric
    end = datetime.now(tz=timezone.utc)
    start = end - timedelta(minutes=5) 

    params = {
        "from": start.isoformat(),
        "to":   end.isoformat()
    }
     
    dataset = scoutapm_call('/api/v0/apps/%d/metrics/%s' % (app_id, metric_name), params=params)
    return dataset["summaries"][metric_name]

if __name__ == '__main__':
    print("Extracting apps")
    apps = scoutapm_call('/api/v0/apps')

    print("Extracting available metrics")
    for app in apps['apps']:
        if app['name'] not in monitored_apps:
            # We don't need to extract these metrics"
            continue
        # result: {'name': 'MyPlex', 'id': 119}
        available_metrics = scoutapm_call('/api/v0/apps/%d/metrics' % app['id'])
        for metric in available_metrics['availableMetrics']:
            data.append((app['name'], app['id'], metric))
            if not metrics.get(metric):
                metrics[metric] = Gauge("%s_%s" % (prefix,metric), metric, ['app_name'])

    print("Starting HTTP Server on port %s" % port)
    # Start up the server to expose the metrics.
    start_http_server(int(port))

    while True:
        for metric_info in data:
            app_name, app_id, metric_name = metric_info
            metrics[metric_name].labels(app_name=app_name).set(extract_metrics(metric_info))
        # We don't get data updated every seconds, so let's wait 1 minute between polls
        print("Waiting %d seconds" % time_between_polls)
        sleep(time_between_polls)
