import requests
import pandas as pd

FHIR_SERVER_URL = "http://localhost:8080/fhir"

def fetch_patient_data(count=1000):
    endpoint = f"{FHIR_SERVER_URL}/Patient"
    params = {"_pretty": "true", "_count": f"{count}"}
    response = requests.get(endpoint, params=params)

    if response.status_code == 200:
        bundle = response.json()
        return extract_patient_data(bundle)
    else:
        print(f"Error: Unable to fetch data, status code {response.status_code}")
        return pd.DataFrame()
    
def extract_patient_data(bundle):
    patients = []
    for entry in bundle.get("entry", []):
        resource = entry.get("resource", {})
        patients.append({
            "id": resource.get("id"),
            "gender": resource.get("gender"),
            "birthDate": resource.get("birthDate"),
            "race": resource.get("race"),
            "ethnicity": resource.get("ethnicity"),
            "deceasedDateTime": resource.get("deceasedDateTime")
        })
    return pd.DataFrame(patients)

def handle_deceased_datetime_add_helper_columns(df):
    """
    assumes df['deceasedDateTime'] exists
    """
    df = df.dropna(subset=['deceasedDateTime']) # doesn't make sense to have death data with no time of death

    df['deceasedDateTime'] = pd.to_datetime(df['deceasedDateTime'], errors='coerce')
    df['deceasedYear'] = (df['deceasedDateTime'].dt.year).astype(int)
    df['deceasedMonth'] = (df['deceasedDateTime'].dt.month).astype(int)
    df['deceasedDay'] = (df['deceasedDateTime'].dt.day).astype(int)

    return df