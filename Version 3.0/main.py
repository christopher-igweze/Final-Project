# Importing necessary modules and constants
from xml.etree.ElementPath import findall
from Modules import POPULATION_SIZE
from Modules.Population import Population
from Modules.Display import DisplayMgr
from Modules.Genetic_Algo import GeneticAlgorithm
from Modules.Schedule import Schedule, updatedSchedule, finalSchedule
from Modules.Excel import output_schedule
# from Frontend.pages.constraints import returnValues
import time

# Define maximum iterations and time; set to None to disable
MAX_ITERATIONS = None # Maximum iterations
MAX_TIME = 61 # Maximum time in seconds   

# Function to find the fittest schedule
def find_fittest_schedule(verboseFlag):
    start_time = time.time()  # Record the start time
    # Initialize generation number
    generationNumber = 0
    # Print the generation number if verbose flag is True
    if (verboseFlag): print("> Generation # "+str(generationNumber))
    # Create a new population
    population = Population(POPULATION_SIZE)
    # Sort the schedules in the population by fitness
    population.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)
    # If verbose flag is True, display the generation and the fittest schedule
    if (verboseFlag):
        DisplayMgr.display_generation(population)
        DisplayMgr.display_schedule_as_table(population.get_schedules()[0])
        DisplayMgr.display_schedule_conflicts(population.get_schedules()[0])
    # Initialize the genetic algorithm
    geneticAlgorithm = GeneticAlgorithm()
    # Keep evolving the population until a perfect schedule is found
    while (population.get_schedules()[0].get_fitness() != 1.0):
        # Check if maximum iterations is reached
        if MAX_ITERATIONS is not None and generationNumber >= MAX_ITERATIONS:
            print("> Maximum iterations reached without finding a perfect solution.")
            break
        # Check if maximum time is exceeded
        if MAX_TIME is not None and (time.time() - start_time) > MAX_TIME:
            print("> Maximum time exceeded without finding a perfect solution.")
            break
        # Increment the generation number
        generationNumber += 1
        # Print the generation number if verbose flag is True
        if (verboseFlag): print("\n> Generation # " + str(generationNumber))
        # Evolve the population
        population = geneticAlgorithm.evolve(population)
        # Sort the schedules in the population by fitness
        population.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)
        # If verbose flag is True, display the generation and the fittest schedule
        if (verboseFlag):
            DisplayMgr.display_generation(population)
            DisplayMgr.display_schedule_as_table(population.get_schedules()[0])
            DisplayMgr.display_schedule_conflicts(population.get_schedules()[0])
    # Print the number of generations it took to find a solution
    if population.get_schedules()[0].get_fitness() == 1.0:
        print("> Solution found after " + str(generationNumber) + " generations")
    else:
        print("> Ended after " + str(generationNumber) + " generations without a perfect solution")
    # Return the fittest schedule
    final = finalSchedule()[0]
    DisplayMgr.display_schedule_as_tables(final)
    output_schedule()
    return population.get_schedules()[0]

# Function to handle command line inputs
def handle_command_line(verboseFlag):
    # Keep asking for user input until the user decides to exit
    while (True):
        # Ask the user what they want to do
        entry = input("> What do you want to do (i:nitial data display, f:ind fittest schedule, d:efault mode, v:erbose mode, e:xit)\n")
        # If the user wants to display initial data
        if (entry == "i"): DisplayMgr.display_input_data()
        # If the user wants to find the fittest schedule
        elif (entry == "f"):
            schedule = find_fittest_schedule(verboseFlag)
            handle_schedule_display(schedule)
        # If the user wants to switch to default mode
        elif (entry == "d"): verboseFlag = False
        # If the user wants to switch to verbose mode
        elif (entry == "v"): verboseFlag = True
        # If the user wants to exit
        elif (entry == "e"): break

# Function to handle schedule display
def handle_schedule_display(schedule):
    # Keep asking for user input until the user decides to go back
    while (True):
        # Ask the user what they want to display
        entry = input("> What do you want to display (c:lass schedule, t:ime schedule, r:oom schedule, i:nstructor schedule, e:lse)\n")
        # If the user wants to display the class schedule
        if (entry == "c"):
            print("> from 'class' perspective")
            DisplayMgr.display_schedule_as_table(schedule)
        # If the user wants to display the time schedule
        elif (entry == "t"): DisplayMgr.display_schedule_meetingTimes(schedule)
        # If the user wants to display the room schedule
        elif (entry == "r"): DisplayMgr.display_schedule_rooms(schedule);
        # If the user wants to display the instructor schedule
        elif (entry == "i"): DisplayMgr.display_schedule_instructors(schedule);
        # If the user wants to go back
        elif (entry == "e"): break

# Main function
def main():
    # Initialize verbose flag as False
    VERBOSE_FLAG = False
    # Start handling command line inputs
    handle_command_line(VERBOSE_FLAG)

# If this script is run directly, call the main function
if __name__ == "__main__":
    main()