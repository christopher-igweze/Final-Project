import re

# Read the uploaded file
file_path = 'C:/Users/USER/Documents/Important Files/Final Project/Version 3.0/files/LEC_LIST.txt'

with open(file_path, 'r') as file:
    data = file.read()

# Extract lecturers and courses
pattern = r'(\w+):([^\(]+)\(([^)]+)\)([^,]+(?:,[^,]+)*)'
matches = re.findall(pattern, data)

# Create a dictionary of unique lecturers with IDs
lecturer_dict = {}
lecturer_id = 1

# Function to get lecturer ID or create a new one
def get_lecturer_id(lecturer_name):
    global lecturer_id
    if lecturer_name not in lecturer_dict:
        lecturer_dict[lecturer_name] = lecturer_id
        lecturer_id += 1
    return lecturer_dict[lecturer_name]

# Process matches to create course list with lecturer IDs
courses = []

for match in matches:
    course_code = match[0].strip()
    course_name = match[1].strip()
    lecturers = [lect.strip() for lect in match[3].split(',')]
    lecturer_ids = [get_lecturer_id(lect) for lect in lecturers]
    courses.append((course_code, lecturer_ids))

# Convert lecturer dictionary to table format
lecturer_table = [{'Lecturer Name': name, 'Lecturer ID': lid} for name, lid in lecturer_dict.items()]

# Convert courses to table format
course_table = [{'Course Code': code, 'Lecturer IDs': ids} for code, ids in courses]

print(lecturer_table, course_table)
