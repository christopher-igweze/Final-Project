from Modules import POPULATION_SIZE
from Modules.Population import Population
from Modules.Display import DisplayMgr
from Modules.Genetic_Algo import GeneticAlgorithm


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


def main():
    VERBOSE_FLAG = False
    handle_command_line(VERBOSE_FLAG)

if __name__ == "__main__":
    main()