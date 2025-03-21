PERSONS = {
    "researcher": {
        "srn": "sharekit:person:d5e05c12-0648-4129-9386-408d47b6f8c0",
        "set": "nppo",
        "provider": "sharekit",
        "external_id": "d5e05c12-0648-4129-9386-408d47b6f8c0",
        "name": "Brian May",
        "themes": ["Queen"]
    }
}


def generate_person(person_type="researcher"):
    copy = PERSONS[person_type].copy()
    return copy
