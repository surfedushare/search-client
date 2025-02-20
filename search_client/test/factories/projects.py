PERSONS = {
    "brian": {
        "name": "Brian May",
        "email": "brian@queen.com",
        "external_id": "person:1"
    }
}


PROJECTS = {
    "math": {
        "srn": "edurep:project:1",
        "set": "edurep",
        "provider": "Kennisnet",
        "external_id": "project:1",
        "title": "Een wiskundig project",
        "project_status": "finished",
        "started_at": "1970-01-01",
        "ended_at": "2020-01-01 22:22:00+00:00",
        "coordinates": [],
        "goal": "Mission accomplished",
        "description": "Dit is de beschrijving van een project met wiskundig onderzoek",
        "contacts": [PERSONS["brian"]],
        "owners": [PERSONS["brian"]],
        "persons": [PERSONS["brian"]],
        "keywords": ["nerds"],
        "parties": ["Wikiwijs Maken"],
        "products": [
            "sharekit:edusources:3522b79c-928c-4249-a7f7-d2bcb3077f10"
        ],
        "themes": [],
        "suggest_phrase": "Een wiskundig project",
        "suggest_completion": ["Een", "wiskundig", "project"],
    }
}


def generate_project(topic="math", title=None, description=None, external_id=None, project_status=None):
    copy = PROJECTS[topic].copy()
    if title:
        copy["title"] = title
    if description:
        copy["description"] = description
    if external_id:
        copy["external_id"] = external_id
        copy["srn"] = f"{copy['set']}:{external_id}"
    if project_status:
        copy["project_status"] = project_status
    return copy
