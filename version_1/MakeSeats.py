'''
MakeSeats.py
------------

Contains the classes for seats and polling places
used by the model. Importantly, results for seats
and polling places are handled the same, but are not
considered as polls, as they give vote numbers rather
than percentages. Hence we need separate helper functions
for these objects. 

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
        self._swings = {}
        self._cluster_no = None

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
                return 0
        else:
            try:
                return self._results[year]
            except KeyError:
                return 'No results for seat ' + str(self._name) + ' in ' + str(year) + '...'

    def swing(self,year):
        try:
            return self._swings[year]
        except KeyError:
            return 'No swing recorded for seat ' + str(self._name) + ' in ' +str(year) + '...'

    def cluster_no(self):
        return self._cluster_no


def PPinSeat(pollingplace, seat):
    return pollingplace in seat.pollingplaces()

def SeatJoinCoalition(seat, year):

    ## Helper function to standardise all polls
    ## into having only a single column for COA and no
    ## columns for constituent parties of the Coalition. 

    liberal = 0
    national = 0
    liberal_party = None
    national_party = None
    for party in ['LIB', 'LP']:
        if seat.results(year,party) > 0:
            liberal = liberal + seat.results(year,party)
            liberal_party = party

    for party in ['NAT', 'NP']:
        if seat.results(year,party) > 0:
            national = national + seat.results(year,party)
            national_party = party

    results_dict = {'COA': liberal + national}

    for party in seat._results[year]:
        if party not in [liberal_party, national_party]:
            results_dict[party] = seat.results(year,party)

    return results_dict


def SeatJoinOthers(seat,year):

    ## Helper function to join all parties which are not
    ## in 'ALP', 'COA', 'GRN' into an 'OTH' field. 

    major_parties = ['ALP', 'LIB', 'NAT', 'LP', 'NP', 'COA', 'GRN']

    others_vote = 0

    for party in seat._results[year]:
        if party not in major_parties:
            others_vote = others_vote + seat.results(year,party)

    results_dict = {'OTH': others_vote}

    for party in major_parties:
        if seat.results(year,party) > 0:
            results_dict[party] = seat.results(year,party)

    return results_dict