import os
from dotenv import load_dotenv

import requests

load_dotenv()

ask_database_schema = {
    "type": "function",
    "function": {
        "name": "ask_database",
        "description": "Use this function to answer user questions about finding jobs. Input should be a fully formed SQL query.",
        "parameters": {
            "type": "object",
            "properties": {
                "what": {
                    "type": "string",
                    "description": "The keyword the job such as job title, job description or job nature etc."
                },
                "where": {
                    "type": "string",
                    "description": "The location of the job. This can be a town, city or region."
                },
                "salary_min": {
                    "type": "string",
                    "description": "The min annual salary"
                },
                "salary_max": {
                    "type": "string",
                    "description": "The max annual salary"
                },
                "job_type": {
                    "type": "string",
                    "description": "The job type",
                    "enum": ["full_time", "part_time", "contract", "permanent"]
                },
            },
            "required": ["what"],
        },
    },
}


def ask_database(what: str, where: str = None, salary_min: str = None, salary_max: str = None, job_type: str = None):
    app_id = os.getenv("ADZUNA_APP_ID")
    app_key = os.getenv("ADZUNA_APP_KEY")

    base_url = "https://api.adzuna.com/v1/api/jobs/gb/search/1?"

    queries = {
        "app_id": app_id,
        "app_key": app_key,
        "what": what,
        "results_per_page": 10,
        "where": where,
        "sort_by": "date",
        "salary_min": salary_min,
        "salary_max": salary_max,
        "full_time": job_type == "full_time",
        "part_time": job_type == "part_time",
        "contract": job_type == "contract",
        "permanent": job_type == "permanent",
    }

    valid_queries = {}

    for key, value in queries.items():
        if value is not None:
            if isinstance(value, bool):
                if value is True:
                    valid_queries[key] = 1
            else:
                valid_queries[key] = value

    query_string = "&".join([f"{key}={value}" for key, value in valid_queries.items()])

    print("query_string:", query_string)

    response = requests.get(base_url + query_string, headers={"Content-Type": "application/json"})

    jobs = [_parse_json(job) for job in response.json()["results"]]

    print("jobs:", jobs)

    return {
        "status": "completed",
        "jobs": jobs
    }


def _parse_json(data):
    return {
        "job_title": data["title"],
        "category": data["category"]["label"],
        "location": data["location"]["display_name"],
        "published_date": data["created"],
        "job_duties": data["description"],
        "company": data["company"]["display_name"],
        "url": data["redirect_url"],
        "salary_is_predicted": data["salary_is_predicted"],
    }
