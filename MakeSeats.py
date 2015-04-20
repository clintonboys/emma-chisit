import LoadData
import PollsterWeightings

elections_from_2000 = LoadData.LoadElections()

class PollingPlace(object):

    def __init__(self,name,seat):
        self._name = name
        self._seat = seat
        self._state = seat.state()

        seat.pollingplaces().append(self)

    @property
    def name(self):
        return self._name

    def state(self):
        return self._state

    def seat(self):
        return self._seat    

class Seat(object):

    def __init__(self, name, state):
        self._name = name
        self._state = state
        self._pollingplaces = []
    @property
    def name(self):
        return self._name

    def state(self):
        return self._state

    def pollingplaces(self):
        return self._pollingplaces

def PPinSeat(pollingplace, seat):
    return pollingplace in seat.pollingplaces()

Sydney = Seat('Sydney', 'NSW')
TownHall = PollingPlace('TownHall', Sydney)
OperaHouse = PollingPlace('OperaHouse', Sydney)

year_range = range(2000,2016)

print PPinSeat(OperaHouse, Sydney)