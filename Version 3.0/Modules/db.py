import glob
import openpyxl
import sqlite3

master_folder = r'C:\Users\USER\Documents\Important Files\Final Project\Version 3.0\extracted_folder\master'
db_file = r'C:\Users\USER\Documents\Important Files\Final Project\Version 3.0\class_schedule-02.db'

alpha = False

# Create a connection with the db
conn = sqlite3.connect(db_file)
cursor = conn.cursor()
# Clear the 'course' table
cursor.execute("DELETE FROM course")
cursor.execute("DELETE FROM course_student")
cursor.execute("DELETE FROM course_instructor")
print("I've deleted the tables data")
counter = 1
Scounter = 1

# Fetch the data from the 'instructor' table
cursor.execute("SELECT * FROM instructor")
data = cursor.fetchall()

# Create a dictionary to store the data
instructor_dict = {}
for row in data:
    instructor_dict[row[1]] = row[0]

course_dict = {}
students = {}
student_idList = []
# Loop through the files in the master folder
for file_path in glob.glob(master_folder + '/*.xlsx'):
    # Loop through the sheets of each workbook
    workbook = openpyxl.load_workbook(file_path)
    if alpha == False:
        actual = [_ for _ in workbook.sheetnames if _ != '300' or _ != '500']
        for sheet_name in actual:
            sheet = workbook[sheet_name]      
            # Populate the table
            for i in range(2, sheet.max_row + 1):
                print(sheet.max_row)
                course_code = f"C{counter}"
                counter += 1
                name = sheet.cell(row=i, column=1).value
                name = str(name)
                numberOfStudents = sheet.cell(row=i, column=2).value
                units = sheet.cell(row=i, column=3).value
                instructors = sheet.cell(row=i, column=4).value
                instructors = str(instructors)
                i_list = instructors.split(',')
                elective = sheet.cell(row=i, column=6).value
                course_dict[name] = course_code
                cursor.execute("SELECT * FROM dept")
                thisData = cursor.fetchall()
                cursor.execute("INSERT INTO course (number, name, max_numb_of_students, credit_hours, Elective) VALUES (?, ?, ?, ?, ?)", (course_code, name, numberOfStudents, units, elective))
                for _ in thisData:
                    if _[2] == sheet.cell(row=i, column=5).value:
                        value = _[0]
                cursor.execute("INSERT INTO dept_course (name, course_numb) VALUES (?, ?)", (value, course_code)) # type: ignore
                for instructor in i_list:
                    cursor.execute("INSERT INTO course_instructor (course_number, instructor_number) VALUES (?, ?)", (course_code, instructor_dict.get(instructor)))

            
            # Get the number of electives required for the semester
            noOfElectives = sheet.cell(row=2, column=7).value
            compulsory_list = [i for i in range(2, sheet.max_row + 1) if sheet[2][6] == "NO"]
            elective_list = [i for i in range(2, sheet.max_row + 1) if sheet[2][6] == "YES"]
            
            if noOfElectives == 0:
                student_list = []
                student_code = f"S{Scounter}"
                Scounter+=1
                for _ in compulsory_list:
                    student_list.append(_)
                for course in student_list:
                    student_idList.append(course_dict.get(course))
                students[student_code] = student_idList    
            elif noOfElectives == 1:
                for x in elective_list:
                    student_code = f"S{Scounter}"
                    Scounter+=1
                    student_list = []
                    for y in compulsory_list:
                        student_list.append(y)
                    student_list.append(x)
                    for course in student_list:
                        student_idList.append(course_dict.get(course))
                    students[student_code] = student_idList
            elif noOfElectives == 2:
                for x in elective_list:
                    new_list = [_ for _ in elective_list if _ != x]
                    for y in new_list:
                        student_code = f"S{Scounter}"
                        Scounter+=1
                        student_list = []
                        for z in compulsory_list:
                            student_list.append(z)
                        student_list.append(y)
                        student_list.append(x)
                        for course in student_list:
                            student_idList.append(course_dict.get(course))
                        students[student_code] = student_idList

            for id in students:
                theList = id[1]
                for _ in theList:
                    cursor.execute("INSERT INTO course_student (course_id, student_id) VALUES (?, ?)", (_, id[0]))
          
conn.commit()
cursor.close()
# Close the connection
conn.close()

