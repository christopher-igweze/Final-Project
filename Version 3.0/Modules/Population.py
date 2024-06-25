# Importing the Schedule class from the Modules package
from Modules.Schedule import Schedule
# Importing the dbMgr module from the Modules package
from Modules import dbMgr

# Defining the Population class
class Population:
    # Constructor for the Population class
    def __init__(self, size):
        # Setting the size of the population
        self._size = size
        # Storing a reference to the dbMgr module
        self._data = dbMgr
        # Initializing an empty list to hold the schedules
        self._schedules = []
        # For each number in the range from 0 to size
        for i in range(0, size):
            # Append a new, initialized Schedule to the list of schedules
            self._schedules.append(Schedule().initialize())
    # Method to get the list of schedules
    def get_schedules(self): 
        return self._schedules
    
    def add_schedules(self, a_schedule : Schedule):
        self._schedules.append(a_schedule)
        self._size += 1