from fhir_utils import fetch_patient_data
import pandas as pd
# import dash_bootstrap_components as dbc

# Incorporate data
# df = fetch_patient_data() # assumes the server url is http://localhost:8080/fhir

# df['deceasedDateTime'] = pd.to_datetime(df['deceasedDateTime'])
# df['deceasedYear'] = df['deceasedDateTime'].dt.year
# df['deceasedMonth'] = df['deceasedDateTime'].dt.month
# df['deceasedDay'] = df['deceasedDateTime'].dt.day

df = pd.read_csv('conneticut_wide_form.csv')

print(df[df['death_year'].isnull()])