# same thing as Modules.__init__
from Modules import dbMgr, POPULATION_SIZE
import prettytable
from Modules.Population import Population
from Modules.GA import GeneticAlgorithm


# This class is responsible for displaying the data and the schedules
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
