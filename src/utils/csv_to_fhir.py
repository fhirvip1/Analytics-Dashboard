import csv
from datetime import datetime
import requests

# def convert_date_format(date_str):
#     print(date_str)
#     date_obj = datetime.strptime(date_str, "%m/%d/%Y")
#     return date_obj.strftime("%Y-%m-%d")


def csv_to_dict(filename):
    with open(filename, mode='r', newline='', encoding='utf-8') as file:
        # Create a CSV reader object
        csv_reader = csv.DictReader(file)

        # Convert each row into a dictionary and store in a list
        rows_as_dicts = [row for row in csv_reader]
    
    return rows_as_dicts

# Example usage
filename = 'conneticut_wide_form.csv'  # Replace with your CSV file path
dict_data = csv_to_dict(filename)


## get race extension

import json

def build_race_extension(input_string):
    input_string = input_string.lower()
    race_extensions = {
        'asian indian': {
            "url": "http://hl7.org/fhir/StructureDefinition/patient-race",
            "valueCodeableConcept": {
                "coding": [{
                    "system": "urn:oid:2.16.840.1.113883.6.238",
                    "code": "2028-9",
                    "display": "Asian Indian"
                }]
            }
        },
        'asian, other': {
            "url": "http://hl7.org/fhir/StructureDefinition/patient-race",
            "valueCodeableConcept": {
                "coding": [{
                    "system": "urn:oid:2.16.840.1.113883.6.238",
                    "code": "2076-8",
                    "display": "Asian, Other"
                }]
            }
        },
        'black': {
            "url": "http://hl7.org/fhir/StructureDefinition/patient-race",
            "valueCodeableConcept": {
                "coding": [{
                    "system": "urn:oid:2.16.840.1.113883.6.238",
                    "code": "2054-5",
                    "display": "Black"
                }]
            }
        },
        'native american, other': {
            "url": "http://hl7.org/fhir/StructureDefinition/patient-race",
            "valueCodeableConcept": {
                "coding": [{
                    "system": "urn:oid:2.16.840.1.113883.6.238",
                    "code": "2204-7",
                    "display": "Native American, Other"
                }]
            }
        },
        'other': {
            "url": "http://hl7.org/fhir/StructureDefinition/patient-race",
            "valueCodeableConcept": {
                "coding": [{
                    "system": "urn:oid:2.16.840.1.113883.6.238",
                    "code": "2131-1",
                    "display": "Other"
                }]
            }
        },
        'unknown': {
            "url": "http://hl7.org/fhir/StructureDefinition/patient-race",
            "valueCodeableConcept": {
                "coding": [{
                    "system": "urn:oid:2.16.840.1.113883.6.238",
                    "code": "UNKNOWN",
                    "display": "Unknown"
                }]
            }
        },
        'white': {
            "url": "http://hl7.org/fhir/StructureDefinition/patient-race",
            "valueCodeableConcept": {
                "coding": [{
                    "system": "urn:oid:2.16.840.1.113883.6.238",
                    "code": "2106-3",
                    "display": "White"
                }]
            }
        }
    }
    race_extension = race_extensions.get(input_string)

    if race_extension:
        return race_extension
    else:
        return None

## get ethnicity extention

def build_ethnicity_extension(input_string):

    input_string = input_string.lower()
    ethnicity_extension = None

    # Check for 'Hispanic', 'Latin', 'Cuban', or 'Unknown' with exclusion for 'No' or 'Not'
    if ('hispanic' in input_string or 'latin' in input_string) and ('not' not in input_string):
        # Generate the Hispanic or Latino ethnicity extension
        ethnicity_extension = {
            "url": "http://hl7.org/fhir/StructureDefinition/patient-ethnicity",
            "valueCodeableConcept": {
                "coding": [{
                    "system": "urn:oid:2.16.840.1.113883.6.238",
                    "code": "2186-5",
                    "display": "Hispanic or Latino"
                }]
            }
        }
    elif 'cuban' in input_string and ('no' not in input_string and 'not' not in input_string):
        # Generate the Cuban ethnicity extension
        ethnicity_extension = {
            "url": "http://hl7.org/fhir/StructureDefinition/patient-ethnicity",
            "valueCodeableConcept": {
                "coding": [{
                    "system": "urn:oid:2.16.840.1.113883.6.238",
                    "code": "2192-5",  # Example code for Cuban in SNOMED CT (you may need to confirm or create your own code)
                    "display": "Cuban"
                }]
            }
        }
    elif 'other' in input_string:
        # Generate the Other or Unknown ethnicity extension
        ethnicity_extension = {
            "url": "http://hl7.org/fhir/StructureDefinition/patient-ethnicity",
            "valueCodeableConcept": {
                "coding": [{
                    "system": "urn:oid:2.16.840.1.113883.6.238",
                    "code": "2131-1",  # Other ethnicity
                    "display": "Other ethnicity"
                }]
            }
        }

    return ethnicity_extension



def generate_home_address(city, district, state, street_line=None, postal_code=None):    
    address = {
        "use": "home", 
        "type": "both", 
        "line": [street_line] if street_line else [],  
        "city": city,
        "district": district, 
        "state": 'Connecticut', 
        "postalCode": postal_code if postal_code else None, 
        "country": "US" 
    }
    
    return address


def row_to_patient(row):
    patient = {"resourceType" : "Patient"}
    patient['deceasedDateTime'] = row['date']
    extension = []
    patient['gender'] = row['sex'].lower()
    patient['address'] = generate_home_address(row['residencecity'], row['residencecounty'], row['residencestate'])
    if row['ethnicity']:
        ethnicity = build_ethnicity_extension(row['ethnicity'])
        if ethnicity:
            extension.append(ethnicity)    
    if row['race']:
        race = build_race_extension(row['race'])
        if race:
            extension.append(race)
        
    if len(extension) > 0:
        patient['extension'] = extension  
    
    
    patient_request = {}
    patient_request['resource'] = patient
    patient_request['request'] =  {
                    "method": "POST",
                    "url": "Patient"
                }
    return patient_request  
        

def build_bundle(row):
    bundle  = {
        "resourceType": "Bundle",
        "type": "transaction"
        }

    ## bundle['entry'].append(create_condition_resource(row))
    
    ## injury location
    
    injury_location = create_location_resource("Injury Location", row['injurycity'], row['injurycounty'], row['injurystate'], row['descriptionofinjury'] + row['injuryplace'])
    death_location = create_location_resource("Death Location", row['deathcity'], row['deathcounty'], row['death_state'], row['locationifother'] + row['location'])
    bundle['entry'] = [row_to_patient(row), death_location, injury_location]
    return json.dumps(bundle)
    
    
def create_location_resource(location_type, city, county, state, place_description=None):
    location_resource = {
        "resourceType": "Location",
        "name": location_type,
        "description": place_description if place_description else f"Place where {location_type.lower()} occurred",
        "address": {
            "city": city,
            "county": county,
            "state": state
        }
    }
    
    location_request = {}
    location_request['resource'] = location_resource
    location_request['request'] =  {
                    "method": "POST",
                    "url": "Location"
                }
    return location_request

def create_condition_resource(patient_id, cause_of_death_code, cause_of_death_display, manner_of_death, description_of_injury, onset_date_time):
    condition_resource = {
        "resourceType": "Condition",
        "subject": {
            "reference": f"Patient/{patient_id}"
        },
        "code": {
            "coding": [
                {
                    "system": "http://snomed.info/sct",  # SNOMED CT system for diagnosis codes
                    "code": cause_of_death_code,
                    "display": cause_of_death_display
                }
            ]
        },
        "verificationStatus": {
            "coding": [
                {
                    "system": "http://terminology.hl7.org/CodeSystem/condition-ver-status",
                    "code": "confirmed",
                    "display": "Confirmed"
                }
            ]
        },
        "onsetDateTime": onset_date_time,
        "note": [
            {
                "text": description_of_injury
            }
        ],
        "mannerOfDeath": {
            "coding": [
                {
                    "system": "http://terminology.hl7.org/CodeSystem/manner-of-death",
                    "code": manner_of_death,
                    "display": manner_of_death.capitalize()
                }
            ]
        }
    }
    
    condition_request = {}
    condition_request['resource'] = condition_resource
    condition_request['request'] =  {
                    "method": "POST",
                    "url": "Condition"
                }
    return condition_request

    
    
def send_to_server(body):
    url = 'http://localhost:8080/fhir'

    headers = {
        'Content-Type': 'application/fhir+json',
    }
    # Send the POST request
    response = requests.post(url, headers=headers, data=body)

    # Check if the request was successful
    if response.status_code == 200:
        print("Request was successful!")
        print(response.json())  # Print the response from the server
    else:
        print(f"Request failed with status code {response.status_code}")
        print(response.text)
    

# # Print out the result
for row in dict_data:
    body = build_bundle(row)
    print(body)
    send_to_server(body)