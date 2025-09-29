import pandas as pd

# Reconstruct survey and choices data based on previous interactions
# In a real scenario, you would load these from your uploaded files.
survey_data = {
    'type': [
        'start', 'end', 'text', 'geopoint',
        'select_one governorate_list', 'select_one district_list',
        'select_one interview_status_list', 'select_one yes_no',
        'begin_group', 'integer', 'begin_repeat household_members',
        'integer', 'select_one sex', 'end_repeat',
        'select_one boolean', 'select_multiple disability_types', 'text',
        'select_one legal_status', 'select_one edu_lvl', 'text',
        'select_one emp_lvl', 'text', 'note', 'integer', 'end_group'
    ],
    'name': [
        'start_time', 'end_time', 'enumerator_id', 'household_location',
        'governorate', 'district', 'interview_status', 'consent_obtained',
        '', 'household_size', 'household_members', # begin_repeat name
        'member_age', 'member_sex', '', # end_repeat has no name
        'disabilities', 'disab', 'disab_other',
        'head_household_legal_status', 'education_level', 'education_level_other',
        'employment_status', 'employment_status_other', 'note_food_security', 'no_members_per_day', '' # end_group has no name
    ],
    'label': [
        'Start Time of Interview', 'End Time of Interview', 'What is the Enumerator\'s ID?',
        'Please record the GPS coordinates of the household',
        'In Which Governorate is this household located?', 'In which District is this household located?',
        'What is the status of this interview?', 'Has informed consent been obtained from the respondent?',
        '', 'How many individuals living in the household?', 'Provide the age and gender of each household member',
        'Age of household member (in years).', 'Gender of household member.', '',
        'Are there any individuals with disabilities in your household?',
        'Please specify the type(s) of disability(ies) (Select all that apply)', 'Please specify:',
        'What is the legal status of the head of the household?',
        'What is the highest level of education attained by head of household?', 'Please specify:',
        'What is the current employment status of head of household?', 'Please specify:',
        'Food Security:', 'How many meals does the household typically consume?'
    ],
    'required': [
        '', '', '', '', '', '', '', '',
        '', 'yes', '',
        'yes', 'yes', '',
        'yes', '', '',
        'yes', 'yes', '',
        'yes', '', '', 'yes', ''
    ],
    'relevant': [
        '', '', '', '', '', '', '', '',
        '', '', '${household_size} > 0', # relevant for begin_repeat
        '', '', '',
        '', '${disabilities} = \'yes\'', 'selected(${disab}, \'other\')',
        '', '', '${education_level} = \'other\'',
        '', '${employment_status} = \'other\'', '', '', ''
    ]
}
survey_df = pd.DataFrame(survey_data)

choices_data = {
    'list_name': [
        'sex', 'sex', 'legal_status', 'legal_status', 'legal_status',
        'boolean', 'boolean',
        'shelter_type', 'shelter_type', 'shelter_type',
        'governorate_list', 'governorate_list', 'governorate_list', 'governorate_list', 'governorate_list',
        'district_list', 'district_list', 'district_list', 'district_list', 'district_list', 'district_list',
        'interview_status_list', 'interview_status_list', 'interview_status_list',
        'yes_no', 'yes_no',
        'disability_types', 'disability_types', 'disability_types', 'disability_types', 'disability_types', 'disability_types',
        'edu_lvl', 'edu_lvl', 'edu_lvl', 'edu_lvl', 'edu_lvl', 'edu_lvl',
        'emp_lvl', 'emp_lvl', 'emp_lvl', 'emp_lvl', 'emp_lvl', 'emp_lvl'
    ],
    'name': [
        'male', 'female', 'Lebanese citizen', 'registered refugee', 'undocumented migrant',
        'yes', 'no',
        'house', 'apartment', 'tent',
        'beirut', 'mount_lebanon', 'north', 'south', 'bekaa',
        'beirut_dist1', 'beirut_dist2', 'chouf', 'matn', 'tripoli', 'saida', # Added 'saida' to fill out district for south
        'complete', 'incomplete', 'refused',
        'yes', 'no',
        'physical', 'sensory', 'intellectual', 'mental', 'multiple', 'other',
        'none', 'primary', 'secondary', 'vocational', 'university', 'other',
        'employed', 'unemployed', 'self_employed', 'retired', 'student', 'other'
    ],
    'label': [
        'Male', 'Female', 'Lebanese citizen', 'registered refugee', 'undocumented migrant',
        'Yes', 'No',
        'House', 'Apartment', 'Tent',
        'Beirut', 'Mount Lebanon', 'North', 'South', 'Bekaa',
        'Beirut Dist 1 (Beirut)', 'Beirut Dist 2 (Beirut)', 'Chouf (Mount Lebanon)', 'Matn (Mount Lebanon)', 'Tripoli (North)', 'Saida (South)',
        'Complete', 'Incomplete', 'Refused',
        'Yes', 'No',
        'Physical Disability', 'Sensory Disability', 'Intellectual Disability', 'Mental Health Condition', 'Multiple Disabilities', 'Other (Please specify)',
        'No formal education', 'Primary education', 'Secondary education', 'Vocational training', 'University degree', 'Other (Please specify)',
        'Employed', 'Unemployed', 'Self-employed', 'Retired', 'Student', 'Other (Please specify)'
    ]
}
choices_df = pd.DataFrame(choices_data)

# Helper function to get choices for a given list_name
def get_choices_for_list(list_name):
    return choices_df[choices_df['list_name'] == list_name]['name'].tolist()

print("--- Form Entry Suggestions (for Cleaning & Analysis) ---")
print("This output suggests how to fill in each question, considering your form's logic.")
print("Each suggestion is a 'good' example for data quality and testing analysis scenarios.")
print("-" * 60)

group_stack = []
repeat_stack = []

for index, row in survey_df.iterrows():
    q_type = row['type']
    q_name = row['name']
    q_label = row['label']
    q_required = row['required']
    q_relevant = row['relevant']

    indent = "  " * (len(group_stack) + len(repeat_stack))
    prefix = ""

    if q_type == 'start':
        print(f"{indent}* {q_label} ({q_name}): Automatically captured (e.g., '2025-06-01T15:23:00+03:00')")
    elif q_type == 'end':
        print(f"{indent}* {q_label} ({q_name}): Automatically captured (e.g., '2025-06-01T15:35:00+03:00')")
    elif q_type == 'text':
        if q_relevant:
            prefix = f"[CONDITIONAL: {q_relevant}] "
        print(f"{indent}* {prefix}{q_label} ({q_name}): Free text entry (e.g., 'Respondent\'s name', 'Specific condition', 'Another job type')")
    elif q_type == 'integer':
        if q_relevant:
            prefix = f"[CONDITIONAL: {q_relevant}] "
        print(f"{indent}* {prefix}{q_label} ({q_name}): Whole number (e.g., '5', '30', '1')")
    elif q_type == 'geopoint':
        print(f"{indent}* {q_label} ({q_name}): GPS coordinates (e.g., '33.89389 35.50178 100 5' for Lat Long Alt Accuracy)")
    elif q_type.startswith('select_one'):
        list_name = q_type.split(' ')[1]
        options = get_choices_for_list(list_name)
        if q_relevant:
            prefix = f"[CONDITIONAL: {q_relevant}] "
        print(f"{indent}* {prefix}{q_label} ({q_name}): Select ONE from: {', '.join(options)}")
        if q_name == 'interview_status':
             print(f"{indent}    - GOOD FOR ANALYSIS: Test 'complete', 'incomplete', and 'refused'. If 'refused', expect subsequent questions to be blank.")
        elif q_name == 'consent_obtained':
             print(f"{indent}    - If 'interview_status' is 'refused', this should be 'no'. Otherwise, 'yes'.")
        elif q_name == 'disabilities':
             print(f"{indent}    - Test 'yes' (to enable follow-up) and 'no' (to skip follow-up).")

    elif q_type.startswith('select_multiple'):
        list_name = q_type.split(' ')[1]
        options = get_choices_for_list(list_name)
        if q_relevant:
            prefix = f"[CONDITIONAL: {q_relevant}] "
        print(f"{indent}* {prefix}{q_label} ({q_name}): Select MULTIPLE from: {', '.join(options)} (e.g., 'physical sensory other')")
        if 'other' in options and f'{q_name}_other' in survey_df['name'].values:
            print(f"{indent}    - GOOD FOR ANALYSIS: Include 'other' in selection to test '{q_name}_other' field.")
    elif q_type == 'begin_group':
        group_name = q_name if q_name else "Unnamed Group"
        print(f"{indent}--- BEGIN GROUP: {group_name} ---")
        if q_relevant:
            print(f"{indent}    [CONDITIONAL GROUP: {q_relevant}]")
        group_stack.append(group_name)
    elif q_type == 'end_group':
        if group_stack:
            group_name = group_stack.pop()
            print(f"{indent}--- END GROUP: {group_name} ---")
        else:
            print(f"{indent}--- END GROUP (no matching begin_group) ---") # Should not happen in valid XLSForm
    elif q_type == 'begin_repeat':
        repeat_name = q_name if q_name else "Unnamed Repeat"
        print(f"{indent}### BEGIN REPEAT: {repeat_name} ###")
        if q_relevant:
            print(f"{indent}    [CONDITIONAL REPEAT: {q_relevant}]")
        print(f"{indent}    GOOD FOR ANALYSIS: Test various repeat counts (e.g., 0, 1, 3, 5).")
        repeat_stack.append(repeat_name)
    elif q_type == 'end_repeat':
        if repeat_stack:
            repeat_name = repeat_stack.pop()
            print(f"{indent}### END REPEAT: {repeat_name} ###")
        else:
            print(f"{indent}### END REPEAT (no matching begin_repeat) ###") # Should not happen
    elif q_type == 'note':
        print(f"{indent}* {q_label} ({q_name}): Information note displayed to enumerator (no data entry).")
    else:
        print(f"{indent}* {q_label} ({q_name}): {q_type} (Unspecified type, review manually).")

    if q_required == 'yes' and not q_type.startswith(('start', 'end', 'begin_', 'end_', 'note')):
        print(f"{indent}    - REQUIRED: This question must be answered.")

print("-" * 60)
print("--- Cleaning and Analysis Notes ---")
print("1.  **Missing Data:** Pay attention to questions that are blank due to 'relevant' conditions (e.g., if 'interview_status' is 'refused', or if 'disabilities' is 'no'). These are not errors, but expected missing data.")
print("2.  **'Other' Fields:** Ensure that if a 'select_one' or 'select_multiple' question has an 'other' option, and it's selected, the corresponding 'other' text field is populated.")
print("3.  **Repeat Groups:** Data from repeat groups (like 'household_members') will flatten into multiple columns (e.g., 'member_age[0]', 'member_age[1]', etc.). Be prepared to restructure this for analysis (e.g., long format).")
print("4.  **Consistency:** Look for values that might be out of expected ranges (e.g., 'member_age' too high/low if constraints are not enforced by the form).")
print("5.  **Typographical Errors:** In real data, misspellings or inconsistent capitalization (e.g., 'male' vs 'Male') are common in 'text' fields. Your 'select_one' and 'select_multiple' fields will enforce valid choices.")