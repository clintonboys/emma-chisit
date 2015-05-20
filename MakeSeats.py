'''
MakeSeats.py
------------

Contains the classes for seats and polling places
used by the model. 

'''

class PollingPlace(object):

    def __init__(self,name,seat):
        self._name = name
        self._seat = seat
        self._state = seat.state()
        self._results = {}

        seat.pollingplaces().append(self)

    @property
    def name(self):
        return self._name

    def state(self):
        return self._state

    def seat(self):
        return self._seat    

    def AddResults(self,year, results_dict):
        self._results[year] = results_dict

    def GetResults(self,year,party):
        try:
            return self._results[year][party]
        except KeyError:
            return 'Party ' + party + ' did not contest ' + str(self._name) + ' in ' + str(year) + '...'

class Seat(object):

    def __init__(self, name, state):
        self._name = name
        self._state = state
        self._pollingplaces = []
        self._results = {}

    @property
    def name(self):
        return self._name

    def state(self):
        return self._state

    def pollingplaces(self):
        return self._pollingplaces

    def AddResults(self,year,results_dict):
        self._results[year] = results_dict

    def results(self, year, party = None):
        if party is not None:
            try:
                return self._results[year][party]
            except KeyError:
                return 'No results for ' + party + ' in seat ' + str(self._name) + ' in ' + str(year) + '...'
        else:
            try:
                return self._results[year]
            except KeyError:
                return 'No results for seat ' + str(self._name) + ' in ' + str(year) + '...'

def PPinSeat(pollingplace, seat):
    return pollingplace in seat.pollingplaces()