def add_extra_rows(df):
    rows = [
        {
            'age': 46, 
            'fnlwgt': 257473, 
            'education': 'Bachelors', 
            'education-num': 8,
            'marital-status': 'Married-civ-spouse', 
            'occupation': 'Plumber', 
            'relationship': 'Husband', 
            'race': 'Other', 
            'sex': 'Male',
            'capital-gain': 1000, 
            'capital-loss': 0, 
            'hours-per-week': 41, 
            'native-country': 'Australia',
            'label': '>50K'
        },
        {
            'age': 0, 
            'workclass': 'Private', 
            'fnlwgt': 257473, 
            'education': 'Masters', 
            'education-num': 8,
            'marital-status': 'Married-civ-spouse', 
            'occupation': 'Adm-clerical', 
            'relationship': 'Wife', 
            'race': 'Asian', 
            'sex': 'Female',
            'capital-gain': 0, 
            'capital-loss': 0, 
            'hours-per-week': 40, 
            'native-country': 'Pakistan',
            'label': '>50K'
        },
        {
            'age': 1000, 
            'workclass': 'Private', 
            'fnlwgt': 257473, 
            'education': 'Masters', 
            'education-num': 8,
            'marital-status': 'Married-civ-spouse', 
            'occupation': 'Prof-specialty', 
            'relationship': 'Husband', 
            'race': 'Black', 
            'sex': 'Male',
            'capital-gain': 0, 
            'capital-loss': 0, 
            'hours-per-week': 20, 
            'native-country': 'Cameroon',
            'label': '<=50K'
        },
        {
            'age': 25, 
            'workclass': '?', 
            'fnlwgt': 257473, 
            'education': 'Masters', 
            'education-num': 8,
            'marital-status': 'Married-civ-spouse', 
            'occupation': 'gamer', 
            'relationship': 'Husband', 
            'race': 'Asian', 
            'sex': 'Female',
            'capital-gain': 0, 
            'capital-loss': 0, 
            'hours-per-week': 50, 
            'native-country': 'Mongolia',
            'label': '<=50K'
        }
    ]
    
    df = df.append(rows, ignore_index=True)
    
    return df