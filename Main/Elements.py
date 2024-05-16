from enum import Enum

class Course:
    def __init__(self, number, name, instructors, maxNumbOfStudents, creditHours, class1=None, class2=None, class3=None):
        self._number = number
        self._name = name
        self._maxNumbOfStudents = maxNumbOfStudents
        self._instructors = instructors
        self._creditHours = creditHours
        self._c1 = class1
        self._c2 = class2
        self._c3 = class3
    def get_number(self): return self._number
    def get_name(self): return self._name
    def get_instructors(self): return self._instructors
    def get_maxNumbOfStudents(self): return self._maxNumbOfStudents
    def get_credit_hours(self): return self._creditHours
    def get_class1(self): return self._c1
    def get_class2(self): return self._c2
    def get_class3(self): return self._c3
    def set_class1(self, period): self._c1 = period
    def set_class2(self, period): self._c2 = period
    def set_class3(self, period): self._c3 = period
    def __str__(self): return self._name


class Instructor:
    def __init__(self, id, name, availability):
        self._id = id
        self._name = name
        self._availability = availability
    def get_id(self): return self._id
    def get_name(self): return self._name
    def get_availability(self): return self._availability
    def __str__(self): return self._name


class Room:
    def __init__(self, number, seatingCapacity):
        self._number = number
        self._seatingCapacity = seatingCapacity
    def get_number(self): return self._number
    def get_seatingCapacity(self): return self._seatingCapacity


class MeetingTime:
    def __init__(self, id, time, sub):
        self._id = id
        self._time = time
        self._sub = sub
    def get_id(self): return self._id
    def get_time(self): return self._time
    def get_sub(self): return self._sub

    
class Department:
    def __init__(self, name, courses):
        self._name = name
        self._courses = courses
    def get_name(self): return self._name
    def get_courses(self): return self._courses


class Class:
    def __init__(self, id, dept, course):
        self._id = id
        self._dept = dept
        self._course = course
        self._instructor = None
        self._meetingTime = None
        self._room = None
    def get_id(self): return self._id
    def get_dept(self): return self._dept
    def get_course(self): return self._course
    def get_instructor(self): return self._instructor
    def get_meetingTime(self): return self._meetingTime
    def get_room(self): return self._room
    def set_instructor(self, instructor): self._instructor = instructor
    def set_meetingTime(self, meetingTime): self._meetingTime = meetingTime
    def set_room(self, room): self._room = room
    def __str__(self):
        return str(self._dept.get_name()) + "," + str(self._course.get_number()) + "," + \
               str(self._room.get_number()) + "," + str(self._instructor.get_id()) + "," + str(self._meetingTime.get_id())
    

class Conflict:
    class ConflictType(Enum):
        INSTRUCTOR_BOOKING = 1
        ROOM_BOOKING = 2
        NUMB_OF_STUDENTS = 3
        INSTRUCTOR_AVAILABILITY = 4
        CREDIT_HOURS = 5  # New conflict type for credit hours constraint

    def __init__(self, conflictType, conflictBetweenClasses):
        self._conflictType = conflictType
        self._conflictBetweenClasses = conflictBetweenClasses

    def get_conflictType(self):
        return self._conflictType

    def get_conflictBetweenClasses(self):
        return self._conflictBetweenClasses

    def __str__(self):
        return str(self._conflictType) + " " + str("  and  ".join(map(str, self._conflictBetweenClasses)))
