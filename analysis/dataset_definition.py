from datetime import date

from ehrql import Dataset
from ehrql.codes import SNOMEDCTCode
from ehrql.tables.beta.tpp import patients, clinical_events


dataset = Dataset()

dataset.age = patients.age_on("2023-01-01")

dataset.has_matching_event = clinical_events.where(
    clinical_events.snomedct_code == SNOMEDCTCode("11111111")
).exists_for_patient()

dataset.define_population(patients.date_of_birth.is_on_or_after("2000-01-01"))

patient_data = {
    # Correctly expected in population
    1: {
        "patients": [{"date_of_birth": date(2003, 1, 1)}],
        "clinical_events": [{"date": date(2020, 1, 1), "snomedct_code": "11111111"}],
        "expected_in_population": True,
        "expected_columns": {
            "has_matching_event": True,
            "age": 20
        },
    },
    # Correctly not expected in population
    2: {
        "patients": [{"date_of_birth": date(1999, 1, 1)}],
        "clinical_events": [{"date": date(2020, 1, 1), "snomedct_code": "11111111"}],
        "expected_in_population": False,
    },
}
