import os
import requests
from datetime import datetime

def send_metric(api_key, metric_name, value, tags=None):
    url = "https://api.datadoghq.com/api/v1/series"
    headers = {
        "Content-Type": "application/json",
        "DD-API-KEY": api_key
    }
    payload = {
        "series": [
            {
                "metric": metric_name,
                "points": [
                    [int(datetime.utcnow().timestamp()), value]
                ],
                "type": "count",
                "tags": tags or []
            }
        ]
    }
    
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()

def main():
    api_key = os.getenv('DATADOG_API_KEY')
    workflow_name = os.getenv('GITHUB_WORKFLOW')
    workflow_status = os.getenv('WORKFLOW_STATUS')
    run_id = os.getenv('GITHUB_RUN_ID')
    
    metric_name = "github_actions.workflow_status"
    value = 1 if workflow_status == "failure" else 0
    tags = [
        f"workflow:{workflow_name}",
        f"status:{workflow_status}",
        f"run_id:{run_id}"
    ]
    
    send_metric(api_key, metric_name, value, tags)
    print(f"Sent metric {metric_name} with value {value} and tags {tags}")

if __name__ == "__main__":
    main()
