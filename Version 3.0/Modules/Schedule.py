from Modules import dbMgr, rnd
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
        depts = self._data.get_depts()
        for dept in depts:
            courses = dept.get_courses()
            for course in courses:
                # my attempt at ensuring that the credit hours constraint is met
                meeting_times = dbMgr.get_meetingTimes()
                if course.get_credit_hours() == 1:
                    newClass = Class(self._classNumb, dept, course)
                    self._classNumb += 1
                    newClass.set_meetingTime(dbMgr.get_meetingTimes()[rnd.randrange(0, len(dbMgr.get_meetingTimes()))])
                    newClass.set_room(dbMgr.get_rooms()[rnd.randrange(0, len(dbMgr.get_rooms()))])
                    instructors = course.get_instructors()
                    newClass.set_instructor(instructors[rnd.randrange(0, len(instructors))])
                    self._classes.append(newClass)
                    course.set_class1(newClass)

                if course.get_credit_hours() == 2:
                    class1 = Class(self._classNumb, dept, course)
                    self._classNumb += 1
                    index = rnd.randrange(0, len(dbMgr.get_meetingTimes())-1)
                    if meeting_times[index].get_sub() != meeting_times[index + 1].get_sub(): index -= 1 # This was to account for consecutive meeting times that would mean last period of a day and first of the next
                    class1.set_meetingTime(dbMgr.get_meetingTimes()[index])
                    room = rnd.randrange(0, len(dbMgr.get_rooms()))
                    class1.set_room(dbMgr.get_rooms()[room])
                    instructors = course.get_instructors()
                    class1.set_instructor(instructors[rnd.randrange(0, len(instructors))])
                    self._classes.append(class1)

                    class2 = Class(self._classNumb, dept, course)
                    self._classNumb += 1
                    class2.set_meetingTime(dbMgr.get_meetingTimes()[index + 1])
                    class2.set_room(dbMgr.get_rooms()[room])
                    instructors = course.get_instructors()
                    class2.set_instructor(instructors[rnd.randrange(0, len(instructors))])
                    self._classes.append(class2)

                    course.set_class1(class1)
                    course.set_class2(class2)

                if course.get_credit_hours() == 3:
                    
                    class1 = Class(self._classNumb, dept, course)
                    self._classNumb += 1
                    index = rnd.randrange(0, len(dbMgr.get_meetingTimes())-1)
                    if meeting_times[index].get_sub() != meeting_times[index + 1].get_sub(): index -= 1
                    class1.set_meetingTime(dbMgr.get_meetingTimes()[index])
                    room = rnd.randrange(0, len(dbMgr.get_rooms()))
                    class1.set_room(dbMgr.get_rooms()[room])
                    instructors = course.get_instructors()
                    class1.set_instructor(instructors[rnd.randrange(0, len(instructors))])
                    self._classes.append(class1)

                    class2 = Class(self._classNumb, dept, course)
                    self._classNumb += 1
                    class2.set_meetingTime(dbMgr.get_meetingTimes()[index + 1])
                    class2.set_room(dbMgr.get_rooms()[room])
                    instructors = course.get_instructors()
                    class2.set_instructor(instructors[rnd.randrange(0, len(instructors))])
                    self._classes.append(class2)

                    class3 = Class(self._classNumb, dept, course)
                    self._classNumb += 1
                    while True:
                        class3.set_meetingTime(rnd.choice(meeting_times))
                        if class3.get_meetingTime().get_sub() != class1.get_meetingTime().get_sub():
                            break
                    class3.set_room(dbMgr.get_rooms()[rnd.randrange(0, len(dbMgr.get_rooms()))])
                    instructors = course.get_instructors()
                    class3.set_instructor(instructors[rnd.randrange(0, len(instructors))])
                    self._classes.append(class3)
                    
                    course.set_class1(class1)
                    course.set_class2(class2)
                    course.set_class3(class3)
        return self

    # Calculates the fitness of the schedule
    def calculate_fitness(self):
        self._conflicts = []
        classes = self.get_classes()
        for i in range(0, len(classes)):

            # I need to create a constraint for consecutive instructor and room booking for two unit and three unit courses (maybe should be a soft constraint)
            # Seating Capacity Constraint
            seatingCapacityConflict = list()
            seatingCapacityConflict.append(classes[i])
            if (classes[i].get_room().get_seatingCapacity() < classes[i].get_course().get_maxNumbOfStudents()):
                self._conflicts.append(Conflict(ConflictType.NUMB_OF_STUDENTS, seatingCapacityConflict))

            # Credit Hour Constraint
            creditHourConflict = list()
            creditHourConflict.append(classes[i])
            course = classes[i].get_course()
            unit = course.get_credit_hours()
            if unit > 1:
                period1 = int(course.get_class1().get_meetingTime().get_id()[2:])
                period2 = int(course.get_class2().get_meetingTime().get_id()[2:])
                if(period2 != period1 + 1):
                    print(f"Period 1: {period1}, type: {type(period1)}")
                    print(f"Period 2: {period2}, type: {type(period2)}")
                # if period2 != (period1 + 1):
                #     self._conflicts.append(Conflict(Conflict.ConflictType.CREDIT_HOURS, creditHourConflict))
                #     print('hhhhhhh')

            # Here I removed the instructor availability since all lectures are available through the week except for chapel days (Tue / Thur)
            # I need to create a new table for dept-instructor so that you can assign instructors to specific departments to make the availability work
            # if (classes[i].get_meetingTime() not in classes[i].get_instructor().get_availability()):
            #     conflictBetweenClasses = list()
            #     conflictBetweenClasses.append(classes[i])
            #     self._conflicts.append(Conflict(Conflict.ConflictType.INSTRUCTOR_AVAILABILITY, conflictBetweenClasses))
        

            for j in range(0, len(classes)):
                if (j >= i):
                    if (classes[i].get_meetingTime() == classes[j].get_meetingTime() and
                    classes[i].get_id() != classes[j].get_id()):
                        if (classes[i].get_room() == classes[j].get_room()):
                            roomBookingConflict = list()
                            roomBookingConflict.append(classes[i])
                            roomBookingConflict.append(classes[j])
                            self._conflicts.append(Conflict(ConflictType.ROOM_BOOKING, roomBookingConflict))
                        if (classes[i].get_instructor() == classes[j].get_instructor()):
                            instructorBookingConflict = list()
                            instructorBookingConflict.append(classes[i])
                            instructorBookingConflict.append(classes[j])
                            self._conflicts.append(Conflict(ConflictType.INSTRUCTOR_BOOKING, instructorBookingConflict))


        # I need to work on the fitness function so it assigns weights to the conflicts.
        # The weights would be the multiplicative factor
        # For multiple weights add them in the denominator
        # The plus one makes it such that when the number of conflicts is zero the total fitness would be one
        return 1 / ((1.0 * len(self._conflicts) + 1))
    
    # String representation of the schedule
    def __str__(self):
        returnValue = ""
        for i in range(0, len(self._classes) - 1):
            returnValue += str(self._classes[i]) + ", "
        returnValue += str(self._classes[len(self._classes)-1])
        return returnValue
 

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

class ConflictType(enum.Enum):
        INSTRUCTOR_BOOKING = 1
        ROOM_BOOKING = 2
        NUMB_OF_STUDENTS = 3
        INSTRUCTOR_AVAILABILITY = 4
        CREDIT_HOURS = 5  # New conflict type for credit hours constraint

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
