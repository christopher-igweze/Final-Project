from Db_Manager import dbMgr
from Schedule import Schedule

# A class that represents a population of schedules
class Population:
    def __init__(self, size):
        self._size = size
        self._data = dbMgr
        self._schedules = []
        for i in range(0, size): self._schedules.append(Schedule().initialize())
    def get_schedules(self): return self._schedules

