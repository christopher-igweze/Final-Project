# Importing necessary libraries
import sqlite3 as sqlite
from Modules.Elements import Room, MeetingTime, Instructor, Course, Department

# Class to manage the database and all the data retrieval
class DBMgr:

    # Constructor for the class
    # need to add more the new tables
    def __init__(self):
        self._conn = sqlite.connect('../database.db')
        self._c = self._conn.cursor()
        self._rooms = self._select_rooms()
        self._meetingTimes = self._select_meeting_times()
        self._instructors = self._select_instructors()
        self._courses = self._select_courses()
        self._depts = self._select_depts()
        self._numberOfClasses = 0
        for i in range(0, len(self._depts)):
            self._numberOfClasses += len(self._depts[i].get_courses())

    # Returns the list of rooms. [room number, room seating capacity]
    def _select_rooms(self):
        self._c.execute("SELECT * FROM room")
        rooms = self._c.fetchall()
        returnRooms = []
        for i in range(0, len(rooms)):
            returnRooms.append(Room(rooms[i][0], rooms[i][1]))
        return returnRooms
    
    # Returns the list of meeting times. [id, meetingtime(day, 1-hour period), subscript(day)]
    def _select_meeting_times(self):
        self._c.execute("SELECT * FROM meeting_time")
        meetingTimes = self._c.fetchall()
        returnMeetingTimes = []
        for i in range(0, len(meetingTimes)):
            returnMeetingTimes.append(MeetingTime(meetingTimes[i][0], meetingTimes[i][1], meetingTimes[i][2]))
        return returnMeetingTimes
    
    # Returns the list of instructors. [id, name]
    # The instructor availability is a list of all meeting IDs the instructor is available (I am going to eventually remove the availability)
    def _select_instructors(self):
        self._c.execute("SELECT * FROM instructor")
        instructors = self._c.fetchall()
        returnInstructors = []
        for i in range(0, len(instructors)):
            returnInstructors.append(Instructor(instructors[i][0], instructors[i][1], self._select_instructor_availability(instructors[i][0])))
        return returnInstructors
    
    # Returns the instructors availability. A list of all meeting IDs the instructor is available (I have to take this function down)
    def _select_instructor_availability(self, instructor):
        self._c.execute("SELECT * from instructor_availability where instructor_id = '" + instructor + "'")
        instructorMTsRS = self._c.fetchall()
        instructorMTs = []
        for i in range(0, len(instructorMTsRS)): instructorMTs.append(instructorMTsRS[i][1])
        instructorAvailability = list()
        for i in range(0, len(self._meetingTimes)):
            if self._meetingTimes[i].get_id() in instructorMTs:
                instructorAvailability.append(self._meetingTimes[i])
        return instructorAvailability
    
    # Returns the list of courses. [id, name, instructors, max number of students, credit hours], 
    # max number of students and the credits hours
    def _select_courses(self):
        self._c.execute("SELECT * FROM course")
        courses = self._c.fetchall()
        returnCourses = []
        for i in range(0, len(courses)):
            returnCourses.append(
                Course(courses[i][0], courses[i][1], self._select_course_instructors(courses[i][0]), 
                        courses[i][2], courses[i][3]))
        return returnCourses

    # Returns the list of departments. [depts, courses]
    def _select_depts(self):
        self._c.execute("SELECT * FROM dept")
        depts = self._c.fetchall()
        returnDepts = []
        for i in range(0, len(depts)):
            returnDepts.append(Department(depts[i][0], self._select_dept_courses(depts[i][0])))
        return returnDepts
    
    # Returns the list of instructors for a course. [course id, instructor id]
    def _select_course_instructors(self, courseNumber):
        self._c.execute("SELECT * FROM course_instructor where course_number == '" + courseNumber + "'")
        dbInstructorNumbers = self._c.fetchall()
        instructorNumbers = []
        for i in range(0, len(dbInstructorNumbers)):
            instructorNumbers.append(dbInstructorNumbers[i][1])
        returnValue = []
        for i in range(0, len(self._instructors)):
           if  self._instructors[i].get_id() in instructorNumbers:
               returnValue.append(self._instructors[i])
        return returnValue
    
    # Returns the list of courses for a department. [dept name, course id]
    def _select_dept_courses(self, deptName):
        self._c.execute("SELECT * FROM dept_course where name == '" + deptName + "'")
        dbCourseNumbers = self._c.fetchall()
        courseNumbers = []
        for i in range(0, len(dbCourseNumbers)):
            courseNumbers.append(dbCourseNumbers[i][1])
        returnValue = []
        for i in range(0, len(self._courses)):
           if self._courses[i].get_number() in courseNumbers:
               returnValue.append(self._courses[i])
        return returnValue
    
    def get_rooms(self): return self._rooms
    def get_instructors(self): return self._instructors
    def get_courses(self): return self._courses
    def get_depts(self): return self._depts
    def get_meetingTimes(self): return self._meetingTimes
    def get_numberOfClasses(self): return self._numberOfClasses