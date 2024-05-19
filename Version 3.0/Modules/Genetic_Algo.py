from Modules import POPULATION_SIZE, rnd
from Modules.Population import Population
from Modules.Schedule import Schedule

NUMB_OF_ELITE_SCHEDULES = 1
TOURNAMENT_SELECTION_SIZE = 3
MUTATION_RATE = 0.1


class GeneticAlgorithm:
    # Evolve a population by performing crossover and mutation
    def evolve(self, population): return self._mutate_population(self._crossover_population(population))
    
    # Perform crossover on population
    def _crossover_population(self, pop: Population):
        crossover_pop = Population(0)
        # Keep the elite schedules as they are
        for i in range(NUMB_OF_ELITE_SCHEDULES):
            crossover_pop.get_schedules().append(pop.get_schedules()[i])
        # Perform crossover on the rest of the population
        i = NUMB_OF_ELITE_SCHEDULES
        while i < POPULATION_SIZE:
            # Select two schedules from the population
            schedule1 = self._select_tournament_population(pop).get_schedules()[0]
            schedule2 = self._select_tournament_population(pop).get_schedules()[1]
            # Perform crossover on the selected schedules and add the result to the new population
            crossover_pop.get_schedules().append(self._crossover_schedule(schedule1, schedule2))
            i += 1
        return crossover_pop
    

    # Perform mutation on population
    def _mutate_population(self, population):
        # Only mutate non-elite schedules
        for i in range(NUMB_OF_ELITE_SCHEDULES, POPULATION_SIZE):
            self._mutate_schedule(population.get_schedules()[i])
        return population
    
    # Perform crossover on two schedules
    def _crossover_schedule(self, schedule1, schedule2):
        crossoverSchedule = Schedule().initialize()
        # For each class, randomly choose whether to take it from schedule1 or schedule2
        for i in range(0, len(crossoverSchedule.get_classes())):
            if rnd.random() > 0.5:
                crossoverSchedule.get_classes()[i] = schedule1.get_classes()[i]
            else:
                crossoverSchedule.get_classes()[i] = schedule2.get_classes()[i]
        return crossoverSchedule

    # Perform mutation on a schedule
    def _mutate_schedule(self, mutateSchedule):
        # Initialize a new schedule
        schedule = Schedule().initialize()
        # For each class, with a certain probability, replace it with a class from the new schedule
        for i in range(0, len(mutateSchedule.get_classes())):
            if(MUTATION_RATE > rnd.random()): mutateSchedule.get_classes()[i] = schedule.get_classes()[i]
        return mutateSchedule

    # Select a sub-population for tournament selection
    def _select_tournament_population(self, pop):
        tournament_pop = Population(0)
        # Randomly select schedules and add them to the tournament population
        i = 0
        while i < TOURNAMENT_SELECTION_SIZE:
            tournament_pop.get_schedules().append(pop.get_schedules()[rnd.randrange(0, POPULATION_SIZE)])
            i += 1
        # Sort the tournament population by fitness
        tournament_pop.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)
        return tournament_pop
