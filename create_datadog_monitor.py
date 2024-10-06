# create_datadog_monitor.py
import os
import requests
import json
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_monitor(api_key, app_key, monitor_config):
    url = "https://api.datadoghq.com/api/v1/monitor"
    headers = {
        "Content-Type": "application/json",
        "DD-API-KEY": api_key,
        "DD-APPLICATION-KEY": app_key
    }

    response = requests.post(url, headers=headers, data=json.dumps(monitor_config))

    if response.status_code == 200 or response.status_code == 201:
        logging.info("Monitor created successfully.")
        monitor_id = response.json().get("id")
        logging.info(f"Monitor ID: {monitor_id}")
        return monitor_id
    else:
        logging.error(f"Failed to create monitor: {response.status_code} - {response.text}")
        response.raise_for_status()

def main():
    # Retrieve API and APP keys from environment variables
    api_key = os.getenv('DATADOG_API_KEY')
    app_key = os.getenv('DATADOG_APP_KEY')

    if not api_key or not app_key:
        logging.error("DATADOG_API_KEY and DATADOG_APP_KEY must be set as environment variables.")
        sys.exit(1)

    # Define the monitor configuration
    monitor_config = {
        "name": "GitHub Actions Workflow Failure Monitor",
        "type": "metric alert",
        "query": "sum(last_5m):sum:github_actions.workflow_status{status:failure} > 0",
        "message": "🚨 *GitHub Actions Workflow Failure Alert*\nWorkflow *{{workflow}}* has failed in run ID *{{run_id}}*.\nPlease check the details here: {{run_url}}",
        "tags": ["environment:production", "team:devops"],
        "options": {
            "notify_audit": False,
            "locked": False,
            "timeout_h": 0,
            "silenced": {},
            "include_tags": True,
            "thresholds": {
                "critical": 0.0
            }
        }
    }

    try:
        create_monitor(api_key, app_key, monitor_config)
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
