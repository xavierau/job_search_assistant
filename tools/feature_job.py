import streamlit

feature_job_schema = {
    "type": "function",
    "function": {
        "name": "feature_job",
        "description": "Use this function to save a job to your list of featured jobs.",
        "parameters": {
            "type": "object",
            "properties": {
                "job_name": {
                    "type": "string",
                    "description": """the job title / name""",
                },
                "job_url": {
                    "type": "string",
                    "description": "detail page for the job",
                }
            },
            "required": ["job_name", "job_url"],
        },
    },
}


def feature_job(job_name: str, job_url: str):
    streamlit.session_state.featured_jobs.append({
        "name": job_name,
        "url": job_url
    })
    return {
        "status": "completed",
        "message": job_name + " added to list"
    }
