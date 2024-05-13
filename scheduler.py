# Importing necessary libraries
import sqlite3 as sqlite
import prettytable as prettytable
import random as rnd
from enum import Enum

# Initial declaations some global variables
POPULATION_SIZE = 1000
NUMB_OF_ELITE_SCHEDULES = 1
TOURNAMENT_SELECTION_SIZE = 3
MUTATION_RATE = 0.1
VERBOSE_FLAG = False

# CLASS DEFINITIONS

# Class to manage the database and all the data retrieval
class DBMgr:

    # Constructor for the class
    # need to add more the new tables
    def __init__(self):
        self._conn = sqlite.connect('class_schedule-01.db')
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
            # Seating Capacity Constraint
            seatingCapacityConflict = list()
            seatingCapacityConflict.append(classes[i])
            if (classes[i].get_room().get_seatingCapacity() < classes[i].get_course().get_maxNumbOfStudents()):
                self._conflicts.append(Conflict(Conflict.ConflictType.NUMB_OF_STUDENTS, seatingCapacityConflict))

            # Credit Hour Constraint
            creditHourConflict = list()
            creditHourConflict.append(classes[i])
            course = classes[i].get_course()
            unit = course.get_credit_hours()
            if unit > 1:
                period1 = int(course.get_class1().get_meetingTime().get_id()[2:])
                period2 = int(course.get_class2().get_meetingTime().get_id()[2:])
                if period2 != (period1 + 1):
                    self._conflicts.append(Conflict(Conflict.ConflictType.CREDIT_HOURS, creditHourConflict))

            # Here I removed the instructor availability since all lectures are available through the week except for chapel days (Tue / Thur)
            # I need to create a new table for dept-instructor so that you can assign instructors to specific departments to make the availability work
            # if (classes[i].get_meetingTime() not in classes[i].get_instructor().get_availability()):
            #     conflictBetweenClasses = list()
            #     conflictBetweenClasses.append(classes[i])
            #     self._conflicts.append(Conflict(Conflict.ConflictType.INSTRUCTOR_AVAILABILITY, conflictBetweenClasses))
        

        # Here lies the code for the other conflicts. sort them out later

        #     for index_j, j in enumerate(classes):
        #         if (index_j >= index_i):  # corrected line
        #             if (i.get_meetingTime() == j.get_meetingTime() and i.get_id() != j.get_id()):
        #                 if (i.get_room() == j.get_room()):
        #                     roomBookingConflict = list()
        #                     roomBookingConflict.append(i)
        #                     roomBookingConflict.append(j)
        #                     self._conflicts.append(Conflict(Conflict.ConflictType.ROOM_BOOKING, roomBookingConflict))
        #                 if (i.get_instructor() == j.get_instructor()):
        #                     instructorBookingConflict = list()
        #                     instructorBookingConflict.append(i)
        #                     instructorBookingConflict.append(j)
        #                     self._conflicts.append(Conflict(Conflict.ConflictType.INSTRUCTOR_BOOKING, instructorBookingConflict))


        # I need to work on the fitness function so it assigns weights to the conflicts.
        # The weights would be the multiplicative factor, i'll figure out what the plus one does later.
        # For multiple weights add them in the denominator
        return 1 / ((1.0 * len(self._conflicts) + 1))
    
    def __str__(self):
        returnValue = ""
        for i in range(0, len(self._classes) - 1):
            returnValue += str(self._classes[i]) + ", "
        returnValue += str(self._classes[len(self._classes)-1])
        return returnValue
    
class Population:
    def __init__(self, size):
        self._size = size
        self._data = dbMgr
        self._schedules = []
        for i in range(0, size): self._schedules.append(Schedule().initialize())
    def get_schedules(self): return self._schedules

class GeneticAlgorithm:
    def evolve(self, population): return self._mutate_population(self._crossover_population(population))
    def _crossover_population(self, pop: Population):
        crossover_pop = Population(0)
        for i in range(NUMB_OF_ELITE_SCHEDULES):
            # a = pop.get_schedules()
            # for j in range(len(a)):
            #     print(j, a[j], '\n\n')
            crossover_pop.get_schedules().append(pop.get_schedules()[i])
        i = NUMB_OF_ELITE_SCHEDULES
        while i < POPULATION_SIZE:
            schedule1 = self._select_tournament_population(pop).get_schedules()[0]
            schedule2 = self._select_tournament_population(pop).get_schedules()[1]
            crossover_pop.get_schedules().append(self._crossover_schedule(schedule1, schedule2))
            i += 1
        return crossover_pop
    def _mutate_population(self, population):
        for i in range(NUMB_OF_ELITE_SCHEDULES, POPULATION_SIZE):
            self._mutate_schedule(population.get_schedules()[i])
        return population
    
    def _crossover_schedule(self, schedule1, schedule2):
        crossoverSchedule = Schedule().initialize()
        for i in range(0, len(crossoverSchedule.get_classes())):
            if rnd.random() > 0.5:
                crossoverSchedule.get_classes()[i] = schedule1.get_classes()[i]
            else:
                crossoverSchedule.get_classes()[i] = schedule2.get_classes()[i]
    
        # # Ensure the crossover schedule adheres to the credit hours constraint
        # total_credit_hours = sum(class_.get_course().get_credit_hours() for class_ in crossoverSchedule.get_classes())
        # while total_credit_hours != crossoverSchedule._data.get_numberOfClasses():
        #     crossoverSchedule = Schedule().initialize()
        #     total_credit_hours = sum(class_.get_course().get_credit_hours() for class_ in crossoverSchedule.get_classes())

        stopper = True
        block = []
        while stopper:
            for i in crossoverSchedule.get_classes():
                if i.get_course().get_credit_hours() == 2 or i.get_course().get_credit_hours() == 3:
                    if int(i.get_course().get_class1().get_meetingTime().get_id[2:]) != (int(i.get_course().get_class2().get_meetingTime().get_id[2:]) + 1):
                        block.append(False)
                        crossoverSchedule = Schedule().initialize()
                        break
                    else:
                        block.append(True)
            if False not in block:
                stopper = False

        return crossoverSchedule

    def _mutate_schedule(self, mutateSchedule):
        stopper = True
        block = []
        while stopper:
            schedule = Schedule().initialize()
            for i in range(0, len(mutateSchedule.get_classes())):
                if MUTATION_RATE > rnd.random():
                    mutated_class = schedule.get_classes()[i]
                    if mutated_class.get_course().get_credit_hours() == 2 or mutated_class.get_course().get_credit_hours() == 3:
                        if int(mutated_class.get_course().get_class1().get_meetingTime().get_id[2:]) != (int(mutated_class.get_course().get_class2().get_meetingTime().get_id[2:]) + 1):
                            block.append(False)
                            mutateSchedule = Schedule().initialize()
                            break
                        else:
                            block.append(True)
            if False not in block:
                stopper = False
        return mutateSchedule

    def _select_tournament_population(self, pop):
        tournament_pop = Population(0)
        i = 0
        while i < TOURNAMENT_SELECTION_SIZE:
            tournament_pop.get_schedules().append(pop.get_schedules()[rnd.randrange(0, POPULATION_SIZE)])
            i += 1
        tournament_pop.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)
        return tournament_pop
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
class DisplayMgr:
    @staticmethod
    def display_input_data():
        print("> All Available Data")
        DisplayMgr.display_dept()
        DisplayMgr.display_course()
        DisplayMgr.display_room()
        DisplayMgr.display_instructor()
        DisplayMgr.display_meeting_times()
    @staticmethod
    def display_dept():
        depts = dbMgr.get_depts()
        availableDeptsTable = prettytable.PrettyTable(['dept', 'courses'])
        for i in range(0, len(depts)):
            courses = depts.__getitem__(i).get_courses()
            tempStr = "["
            for j in range(0, len(courses) - 1):
                tempStr += courses[j].__str__() + ", "
            tempStr += courses[len(courses) - 1].__str__() + "]"
            availableDeptsTable.add_row([depts.__getitem__(i).get_name(), tempStr])
        print(availableDeptsTable)
    @staticmethod
    def display_course():
        availableCoursesTable = prettytable.PrettyTable(['id', 'course #', 'max # of students', 'instructors'])
        courses = dbMgr.get_courses()
        for i in range(0, len(courses)):
            instructors = courses[i].get_instructors()
            tempStr = ""
            for j in range(0, len(instructors) - 1):
                tempStr += instructors[j].__str__() + ", "
            tempStr += instructors[len(instructors) - 1].__str__()
            availableCoursesTable.add_row(
                [courses[i].get_number(), courses[i].get_name(), str(courses[i].get_maxNumbOfStudents()), tempStr])
        print(availableCoursesTable)
    @staticmethod
    def display_instructor():
        availableInstructorsTable = prettytable.PrettyTable(['id', 'instructor', 'availability'])
        instructors = dbMgr.get_instructors()
        for i in range(0, len(instructors)):
            availability = []
            for j in range(0, len(instructors[i].get_availability())):
                availability.append(instructors[i].get_availability()[j].get_id())
            availableInstructorsTable.add_row([instructors[i].get_id(),instructors[i].get_name(), availability])
        print(availableInstructorsTable)
    @staticmethod
    def display_room():
        availableRoomsTable = prettytable.PrettyTable(['room #', 'max seating capacity'])
        rooms = dbMgr.get_rooms()
        for i in range(0, len(rooms)):
            availableRoomsTable.add_row([str(rooms[i].get_number()), str(rooms[i].get_seatingCapacity())])
        print(availableRoomsTable)
    @staticmethod
    def display_meeting_times():
        availableMeetingTimeTable = prettytable.PrettyTable(['id', 'Meeting Time'])
        meetingTimes = dbMgr.get_meetingTimes()
        for i in range(0, len(meetingTimes)):
            availableMeetingTimeTable.add_row([meetingTimes[i].get_id(), meetingTimes[i].get_time()])
        print(availableMeetingTimeTable)
    @staticmethod
    def display_generation(population):
        table1 = prettytable.PrettyTable(['schedule #', 'fitness', '# of conflicts', 'classes [dept,class,room,instructor,meeting-time]'])
        schedules = population.get_schedules()
        for i in range(0, len(schedules)):
            table1.add_row([str(i+1), round(schedules[i].get_fitness(),3), len(schedules[i].get_conflicts()), schedules[i].__str__()])
        print(table1)
    @staticmethod
    def display_schedule_as_table(schedule):
        classes = schedule.get_classes()
        table = prettytable.PrettyTable(['Class #', 'Dept', 'Course (number, max # of students)', 'Room (Capacity)', 'Instructor (Id)',  'Meeting Time (Id)'])
        for i in range(0, len(classes)):
            table.add_row([str(i+1), classes[i].get_dept().get_name(), classes[i].get_course().get_name() + " (" +
                           classes[i].get_course().get_number() + ", " +
                           str(classes[i].get_course().get_maxNumbOfStudents()) +")",
                           classes[i].get_room().get_number() + " (" + str(classes[i].get_room().get_seatingCapacity()) + ")",
                           classes[i].get_instructor().get_name() +" (" + str(classes[i].get_instructor().get_id()) +")",
                           classes[i].get_meetingTime().get_time() +" (" + str(classes[i].get_meetingTime().get_id()) +")"])
        print(table)
    @staticmethod
    def display_schedule_meetingTimes(schedule):
        print("> from 'meeting time' perspective")
        meetingTimesTable = prettytable.PrettyTable(['id', 'meeting time', 'classes [dept,class,room,instructor,meeting-time] '])
        meetingTimes = dbMgr.get_meetingTimes()
        for i in range(0, len(meetingTimes)):
            classes = list()
            for j in range(0, len(schedule.get_classes())):
                if schedule.get_classes()[j].get_meetingTime() == meetingTimes[i]:
                    classes.append(str(schedule.get_classes()[j]))
            meetingTimesTable.add_row([meetingTimes[i].get_id(), meetingTimes[i].get_time(), str(classes)])
        print(meetingTimesTable)
    @staticmethod
    def display_schedule_rooms(schedule):
        print("> from 'room' perspective")
        scheduleRoomsTable = prettytable.PrettyTable(['room','classes [dept,class,room,instructor,meeting-time] '])
        rooms = dbMgr.get_rooms()
        for i in range(0, len(rooms)):
            roomSchedule = list()
            for j in range(0, len(schedule.get_classes())):
                if schedule.get_classes()[j].get_room() == rooms[i]:
                    roomSchedule.append(str(schedule.get_classes()[j]))
            scheduleRoomsTable.add_row([str(rooms[i].get_number()), str(roomSchedule)])
        print(scheduleRoomsTable)
    @staticmethod
    def display_schedule_instructors(schedule):
        print("> from 'instructor' perspective")
        instructorsTable = prettytable.PrettyTable(['id', 'instructor', "classes [dept,class,room,instructor,meeting-time]",'availability'])
        instructors = dbMgr.get_instructors()
        for i in range(0, len(instructors)):
            availability = []
            for j in range(0, len(instructors[i].get_availability())):
                availability.append(instructors[i].get_availability()[j].get_id())
            classSchedule = list()
            for j in range(0, len(schedule.get_classes())):
                if schedule.get_classes()[j].get_instructor() == instructors[i]:
                    classSchedule.append(str(schedule.get_classes()[j]))
            instructorsTable.add_row([instructors[i].get_id(), instructors[i].get_name(), str(classSchedule), availability])
        print(instructorsTable)
    @staticmethod
    def display_schedule_conflicts(schedule):
        conflictsTable = prettytable.PrettyTable(['conflict type', 'conflict between classes'])
        conflicts = schedule.get_conflicts()
        for i in range(0, len(conflicts)):
            conflictsTable.add_row([str(conflicts[i].get_conflictType()),
                                    str("  and  ".join(map(str, conflicts[i].get_conflictBetweenClasses())))])
        if (len(conflicts) > 0): print(conflictsTable)
def find_fittest_schedule(verboseFlag):
    generationNumber = 0
    if (verboseFlag): print("> Generation # "+str(generationNumber))
    population = Population(POPULATION_SIZE)
    population.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)
    if (verboseFlag):
        DisplayMgr.display_generation(population)
        DisplayMgr.display_schedule_as_table(population.get_schedules()[0])
        DisplayMgr.display_schedule_conflicts(population.get_schedules()[0])
    geneticAlgorithm = GeneticAlgorithm()
    while (population.get_schedules()[0].get_fitness() != 1.0):
        generationNumber += 1
        if (verboseFlag): print("\n> Generation # " + str(generationNumber))
        population = geneticAlgorithm.evolve(population)
        population.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)
        if (verboseFlag):
            DisplayMgr.display_generation(population)
            DisplayMgr.display_schedule_as_table(population.get_schedules()[0])
            DisplayMgr.display_schedule_conflicts(population.get_schedules()[0])
    print("> solution found after " + str(generationNumber) + " generations")
    return population.get_schedules()[0]
def handle_command_line(verboseFlag):
    while (True):
        entry = input("> What do you want to do (i:nitial data display, f:ind fittest schedule, d:efault mode, v:erbose mode, e:xit)\n")
        if (entry == "i"): DisplayMgr.display_input_data()
        elif (entry == "f"):
            schedule = find_fittest_schedule(verboseFlag)
            handle_schedule_display(schedule)
        elif (entry == "d"): verboseFlag = False
        elif (entry == "v"): verboseFlag = True
        elif (entry == "e"): break
def handle_schedule_display(schedule):
    while (True):
        entry = input("> What do you want to display (c:lass schedule, t:ime schedule, r:oom schedule, i:nstructor schedule, e:lse)\n")
        if (entry == "c"):
            print("> from 'class' perspective")
            DisplayMgr.display_schedule_as_table(schedule)
        elif (entry == "t"): DisplayMgr.display_schedule_meetingTimes(schedule)
        elif (entry == "r"): DisplayMgr.display_schedule_rooms(schedule);
        elif (entry == "i"): DisplayMgr.display_schedule_instructors(schedule);
        elif (entry == "e"): break
dbMgr = DBMgr()
handle_command_line(VERBOSE_FLAG)

