from py import test
from Modules import dbMgr, rnd
from Modules.DBMgr import Instructor, MeetingTime
import enum

# Class to manage the scheduling process
class Schedule:

    # Constructor for the class
    def __init__(self):
        self._data = dbMgr
        self._classes = []
        self._conflicts = []
        self._fitness = -1
        self._classNumb = 0
        self._isFitnessChanged = True

    # Returns the list of classes(as in lectures) for the schedule
    def get_classes(self):
        self._isFitnessChanged = True
        return self._classes

    # Returns the list of conflicts for the schedule
    def get_conflicts(self):
        return self._conflicts

    # Returns the fitness of the schedule
    def get_fitness(self):
        if self._isFitnessChanged:
            self._fitness = self.calculate_fitness()
            self._isFitnessChanged = False
        return self._fitness

    # Initializes the schedule
    def initialize(self):
        # Create a list of big rooms and small rooms to speed up the room assignment process
        # I'll eventually have to do for lab courses
        # bigRoom = []
        # smallRoom = []
        # for i in range(0, len(dbMgr.get_rooms())):
        #     if dbMgr.get_rooms()[i].get_seatingCapacity() >= 400:
        #         bigRoom.append(dbMgr.get_rooms()[i])
        #     else:
        #         smallRoom.append(dbMgr.get_rooms()[i])

        # Chapel days constraint meeting times
        global course_colleges # Making this global so I can use it in the fitness class

        tuesdayService_meetingTimes = [meetingTime for meetingTime in dbMgr.get_meetingTimes() if meetingTime not in dbMgr.get_meetingTimes()[10:12]]
        thursdayService_meetingTimes = [meetingTime for meetingTime in dbMgr.get_meetingTimes() if meetingTime not in dbMgr.get_meetingTimes()[30:32]]
        course_colleges = {i[0]: i[1] for i in dbMgr.get_courseColleges()}

        depts = self._data.get_depts()
        for dept in depts:
            courses = dept.get_courses()
            for course in courses:
                # my attempt at ensuring that the credit hours constraint is met
                meeting_times = dbMgr.get_meetingTimes()
                if course.get_credit_hours() == 1:
                    newClass = Lecture(self._classNumb, dept, course)
                    self._classNumb += 1
                    # Here I will check for their service days and set a meeting time appropriately
                    college = course_colleges.get(course.get_number())
                    
                    if college == 'CST' or college == 'CMSS':
                        newClass.set_meetingTime(rnd.choice(thursdayService_meetingTimes))
                    else:
                        newClass.set_meetingTime(rnd.choice(tuesdayService_meetingTimes))
                    # # Here I need to check if the number of students in the course is greater than the seating capacity of small rooms
                    # if course.get_maxNumbOfStudents() >= 400:
                    #     newClass.set_room(bigRoom[rnd.randrange(0, len(bigRoom))])
                    # else:
                    #     newClass.set_room(smallRoom[rnd.randrange(0, len(smallRoom))])
                    
                    # New strategy for room assignment: Only assign rooms from rooms that can contain the number of students in the course
                    rooms = [room for room in dbMgr.get_rooms() if room.get_seatingCapacity() >= course.get_maxNumbOfStudents()]
                    choice = rnd.choice(rooms)
                    newClass.set_room(choice)

                    newClass.set_instructor(course.get_instructors())
                    self._classes.append(newClass)
                    course.set_class1(newClass)

                if course.get_credit_hours() == 2 or course.get_credit_hours() == 0:
                    class1 = Lecture(self._classNumb, dept, course)
                    self._classNumb += 1
                    # Here I will check for their service days and set a meeting time appropriately
                    college = course_colleges.get(course.get_number())
                    
                    if college == 'CST' or college == 'CMSS':
                        index = rnd.randrange(0, len(thursdayService_meetingTimes)-1)
                        if thursdayService_meetingTimes[index].get_sub() != thursdayService_meetingTimes[index + 1].get_sub(): index -= 1 # This was to account for consecutive meeting times that would mean last period of a day and first of the next
                        class1.set_meetingTime(thursdayService_meetingTimes[index])
                    else:
                        index = rnd.randrange(0, len(tuesdayService_meetingTimes)-1)
                        if tuesdayService_meetingTimes[index].get_sub() != tuesdayService_meetingTimes[index + 1].get_sub(): index -= 1 # This was to account for consecutive meeting times that would mean last period of a day and first of the next
                        class1.set_meetingTime(tuesdayService_meetingTimes[index])
                    # # Here I need to check if the number of students in the course is greater than the seating capacity of small rooms
                    # if course.get_maxNumbOfStudents() > 300:
                    #     room = bigRoom[rnd.randrange(0, len(bigRoom))]
                    # else:
                    #     room = smallRoom[rnd.randrange(0, len(smallRoom))]
                    # class1.set_room(room)
                    
                    # New strategy for room assignment: Only assign rooms from rooms that can contain the number of students in the course
                    rooms = [room for room in dbMgr.get_rooms() if room.get_seatingCapacity() >= course.get_maxNumbOfStudents()]
                    choice = rnd.choice(rooms)
                    class1.set_room(choice)

                    class1.set_instructor(course.get_instructors())
                    self._classes.append(class1)

                    class2 = Lecture(self._classNumb, dept, course)
                    self._classNumb += 1
                    
                    if college == 'CST' or college == 'CMSS':
                        class2.set_meetingTime(thursdayService_meetingTimes[index+1])
                    else:
                        class2.set_meetingTime(tuesdayService_meetingTimes[index+1])
                    
                    class2.set_room(choice)
                    
                    class2.set_instructor(course.get_instructors())
                    self._classes.append(class2)

                    course.set_class1(class1)
                    course.set_class2(class2)

                if course.get_credit_hours() == 3:
                    
                    class1 = Lecture(self._classNumb, dept, course)
                    self._classNumb += 1
                    # Here I will check for their service days and set a meeting time appropriately
                    college = course_colleges.get(course.get_number())
                    
                    if college == 'CST' or college == 'CMSS':
                        index = rnd.randrange(0, len(thursdayService_meetingTimes)-1)
                        if thursdayService_meetingTimes[index].get_sub() != thursdayService_meetingTimes[index + 1].get_sub(): index -= 1 # This was to account for consecutive meeting times that would mean last period of a day and first of the next
                        class1.set_meetingTime(thursdayService_meetingTimes[index])
                    else:
                        index = rnd.randrange(0, len(tuesdayService_meetingTimes)-1)
                        if tuesdayService_meetingTimes[index].get_sub() != tuesdayService_meetingTimes[index + 1].get_sub(): index -= 1 # This was to account for consecutive meeting times that would mean last period of a day and first of the next
                        class1.set_meetingTime(tuesdayService_meetingTimes[index])
                    # # Here I need to check if the number of students in the course is greater than the seating capacity of small rooms
                    # if course.get_maxNumbOfStudents() >= 400:
                    #     room = bigRoom[rnd.randrange(0, len(bigRoom))]
                    # else:
                    #     room = smallRoom[rnd.randrange(0, len(smallRoom))]
                    # class1.set_room(room)
                    
                    # New strategy for room assignment: Only assign rooms from rooms that can contain the number of students in the course
                    rooms = [room for room in dbMgr.get_rooms() if room.get_seatingCapacity() >= course.get_maxNumbOfStudents()]
                    choice = rnd.choice(rooms)
                    class1.set_room(choice)

                    class1.set_instructor(course.get_instructors())
                    self._classes.append(class1)

                    class2 = Lecture(self._classNumb, dept, course)
                    self._classNumb += 1
                    if college == 'CST' or college == 'CMSS':
                        class2.set_meetingTime(thursdayService_meetingTimes[index+1])
                    else:
                        class2.set_meetingTime(tuesdayService_meetingTimes[index+1])
                    class2.set_room(choice)
                    
                    class2.set_instructor(course.get_instructors())
                    self._classes.append(class2)

                    class3 = Lecture(self._classNumb, dept, course)
                    self._classNumb += 1
                    while True:
                        meeting_times = thursdayService_meetingTimes if college in ['CST', 'CMSS'] else tuesdayService_meetingTimes
                        class3.set_meetingTime(rnd.choice(meeting_times))
                        if class3.get_meetingTime().get_sub() != class1.get_meetingTime().get_sub():
                            break 
                    # # Here I need to check if the number of students in the course is greater than the seating capacity of small rooms
                    # if course.get_maxNumbOfStudents() >= 400:
                    #     room = bigRoom[rnd.randrange(0, len(bigRoom))]
                    # else:
                    #     room = smallRoom[rnd.randrange(0, len(smallRoom))]
                    # class3.set_room(room)

                    # New strategy for room assignment: Only assign rooms from rooms that can contain the number of students in the course
                    rooms = [room for room in dbMgr.get_rooms() if room.get_seatingCapacity() >= course.get_maxNumbOfStudents()]
                    choice = rnd.choice(rooms)
                    class3.set_room(choice)
                    
                    class3.set_instructor(course.get_instructors())
                    self._classes.append(class3)
                    
                    course.set_class1(class1)
                    course.set_class2(class2)
                    course.set_class3(class3)
        return self

    # Calculates the fitness of the schedule
    def calculate_fitness(self):
        self._conflicts = []
        global test_list
        test_list = []
        cc_list = []
        cc_list2 = []
        classes = self.get_classes()
        global masterSchedule, masterSchedule2
        masterSchedule = []
        masterSchedule2 = []
        courses = dbMgr.get_courses()
        checked = []
        for i in courses:
            unit = int(i.get_credit_hours())
            if unit == 1:
                masterSchedule2.append(i.get_class1())
            elif unit == 0 or unit == 2:
                masterSchedule2.append(i.get_class1())
                masterSchedule2.append(i.get_class2())
            else:
                masterSchedule2.append(i.get_class1())
                masterSchedule2.append(i.get_class2())
                masterSchedule2.append(i.get_class3())


        for i in range(0, len(classes)):
            checked.append(classes[i])
            theId = 0
            theDept = classes[i].get_dept()
            theCourse = classes[i].get_course()
        
            newLecture = Lecture(theId, theDept, theCourse)
            theId += 1
        
            if classes[i].get_course().get_credit_hours() == 1:
                theRoom = classes[i].get_course().get_class1().get_room()
                theMT = classes[i].get_course().get_class1().get_meetingTime()
                theinstructor = classes[i].get_course().get_instructors()
                newLecture.set_room(theRoom)
                newLecture.set_meetingTime(theMT)
                newLecture.set_instructor(theinstructor)
        
            if classes[i].get_course().get_credit_hours() == 3 or classes[i].get_course().get_credit_hours() == 2 or classes[i].get_course().get_credit_hours() == 0:
                if len(checked) >= 3 and checked[-3].get_course() == classes[i].get_course():
                    theRoom = classes[i].get_course().get_class3().get_room()
                    theMT = classes[i].get_course().get_class3().get_meetingTime()
                    theinstructor = classes[i].get_course().get_instructors()
                    newLecture.set_room(theRoom)
                    newLecture.set_meetingTime(theMT)
                    newLecture.set_instructor(theinstructor)
                elif len(checked) >= 2 and checked[-2].get_course() == classes[i].get_course():
                    theRoom = classes[i].get_course().get_class2().get_room()
                    theMT = classes[i].get_course().get_class2().get_meetingTime()
                    theinstructor = classes[i].get_course().get_instructors()
                    newLecture.set_room(theRoom)
                    newLecture.set_meetingTime(theMT)
                    newLecture.set_instructor(theinstructor)
                else:
                    theRoom = classes[i].get_course().get_class1().get_room()
                    theMT = classes[i].get_course().get_class1().get_meetingTime()
                    theinstructor = classes[i].get_course().get_instructors()
                    newLecture.set_room(theRoom)
                    newLecture.set_meetingTime(theMT)
                    newLecture.set_instructor(theinstructor)
            

            # I need to create a constraint for consecutive instructor and room booking for two unit and three unit courses (maybe should be a soft constraint)
            # Seating Capacity Constraint
            seatingCapacityConflict = list()
            seatingCapacityConflict.append(classes[i])
            if (classes[i].get_room().get_seatingCapacity() < classes[i].get_course().get_maxNumbOfStudents()):
                self._conflicts.append(Conflict(ConflictType.NUMB_OF_STUDENTS, seatingCapacityConflict))
                test_list.append(1)

            # Credit Hour Constraint
            # Isn't actually working. Come back to it.
            creditHourConflict = []
            course = classes[i].get_course()
            unit = course.get_credit_hours()
            if unit > 1:
                crs = course.get_number()
                period1 = int(course.get_class1().get_meetingTime().get_id()[2:])
                period2 = int(course.get_class2().get_meetingTime().get_id()[2:])
                period3 = None
                if unit == 3:
                    period3 = int(course.get_class3().get_meetingTime().get_id()[2:])
                if newLecture.get_meetingTime().get_id()[2:] == period1:
                    stuff = True
                else : stuff = False
                cc_list.append([crs, period1, period2, stuff])
                # print(period1 + period2)
                if period2 != (period1 + 1):
                    self._conflicts.append(Conflict(ConflictType.CREDIT_HOURS, creditHourConflict))
                    test_list.append(2)
                    
            # Here I removed the instructor availability since all lectures are available through the week except for chapel days (Tue / Thur)
            # I need to create a new table for dept-instructor so that you can assign instructors to specific departments to make the availability work
            # I need to fully understand how (look down for 'this') works
            college = course_colleges.get(classes[i].get_course().get_number())
            conflictBetweenClasses = list()
            conflictBetweenClasses.append(classes[i]) # this   
            if (college in ['CST', 'CMSS']) and (classes[i].get_meetingTime() in dbMgr.get_meetingTimes()[30:32]):
                self._conflicts.append(Conflict(ConflictType.INSTRUCTOR_AVAILABILITY, conflictBetweenClasses))
                test_list.append(3)
            elif (college not in ['CST', 'CMSS']) and (classes[i].get_meetingTime() in dbMgr.get_meetingTimes()[10:12]):
                self._conflicts.append(Conflict(ConflictType.INSTRUCTOR_AVAILABILITY, conflictBetweenClasses))
                test_list.append(4)

            # Consecutive Room Booking Constraint
            consecutiveRoomConflict = list()
            consecutiveRoomConflict.append(classes[i])
            course = classes[i].get_course()
            if course.get_credit_hours() > 1:
                lc1 = str(course.get_class1().get_room().get_number())
                lc2 = str(course.get_class2().get_room().get_number())
                lc3 = None
                if course.get_credit_hours() == 3:
                    lc3 = str(course.get_class3().get_room().get_number())
                cc_list2.append([lc1, lc2, lc3])
                if course.get_class1().get_room().get_number() != course.get_class2().get_room().get_number():
                    self._conflicts.append(Conflict(ConflictType.CONSECUTIVE_ROOM_BOOKING, consecutiveRoomConflict))
                    test_list.append(5)
                        

            for j in range(0, len(classes)):
                if (classes[j].get_course().get_number() != classes[i].get_course().get_number()):
                    if (classes[i].get_meetingTime() == classes[j].get_meetingTime() and
                    classes[i].get_id() != classes[j].get_id()):
                        if (classes[i].get_room() == classes[j].get_room()):
                            roomBookingConflict = list()
                            roomBookingConflict.append(classes[i])
                            roomBookingConflict.append(classes[j])
                            self._conflicts.append(Conflict(ConflictType.ROOM_BOOKING, roomBookingConflict))
                            test_list.append(6)
                        # This line checks if there are any common instructors between two classes.
                        # It does this by creating sets of instructors for each class and finding the intersection of these sets.
                        # If the intersection is not empty (i.e., there are common instructors), the condition is True.
                        # This could indicate a scheduling conflict, as an instructor cannot teach two classes at the same time.
                        if set(classes[i].get_instructor()) & set(classes[j].get_instructor()):
                            instructorBookingConflict = list()
                            instructorBookingConflict.append(classes[i])
                            instructorBookingConflict.append(classes[j])
                            self._conflicts.append(Conflict(ConflictType.INSTRUCTOR_BOOKING, instructorBookingConflict))
                            test_list.append(7)


        # I need to work on the fitness function so it assigns weights to the conflicts.
        # The weights would be the multiplicative factor
        # For multiple weights add them in the denominator
        # The plus one makes it such that when the number of conflicts is zero the total fitness would be one
            masterSchedule.append(newLecture)
            

        # print(test_list, cc_list, cc_list2)
        # print(len(classes),len(masterSchedule))
        return 1 / ((1.0 * len(self._conflicts) + 1))
    
    # String representation of the schedule
    def __str__(self):
        returnValue = ""
        for i in range(0, len(self._classes) - 1):
            returnValue += str(self._classes[i]) + ", "
        returnValue += str(self._classes[len(self._classes)-1])
        return returnValue
 

class Lecture:
    def __init__(self, id, dept, course):
        # ignore type errors because these are initialised later

        self._id = id
        self._dept = dept
        self._course = course
        self._instructor: list[Instructor] = None # type: ignore
        self._meetingTime: MeetingTime = None # type: ignore
        self._room: Room = None # type: ignore
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
        instructors = [i.get_id() for i in self._instructor]
        instructors_str = ', '.join(instructors)
        return str(self._dept.get_name()) + "," + str(self._course.get_number()) + "," + \
               str(self._room.get_number()) + "," + instructors_str + "," + str(self._meetingTime.get_id())

class ConflictType(enum.Enum):
        INSTRUCTOR_BOOKING = 1
        ROOM_BOOKING = 2
        NUMB_OF_STUDENTS = 3
        INSTRUCTOR_AVAILABILITY = 4
        CREDIT_HOURS = 5
        CONSECUTIVE_ROOM_BOOKING = 6

class Conflict:

    def __init__(self, conflictType, conflictBetweenClasses):
        self._conflictType = conflictType
        self._conflictBetweenClasses = conflictBetweenClasses

    def get_conflictType(self):
        return self._conflictType

    def get_conflictBetweenClasses(self):
        return self._conflictBetweenClasses

    def __str__(self):
        return str(self._conflictType) + " " + str("  and  ".join(map(str, self._conflictBetweenClasses)))

class updatedSchedule:
    def __init__(self, solution) -> None:
        self._solution: list[Lecture] = solution
    def get_solution(self): return self._solution

def finalSchedule():
    TT = updatedSchedule(masterSchedule)
    mainTimetable = TT.get_solution()
    return mainTimetable, masterSchedule
