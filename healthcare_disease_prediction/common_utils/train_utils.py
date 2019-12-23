def prep_diabetes_dataset(data):  # we assume a pre-cleaned dataset
    return data[(data.BloodPressure != 0) & (data.BMI != 0) & (data.Glucose != 0)]
