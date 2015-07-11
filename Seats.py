'''
 _______  _______  _______  _______ 
(  ____ \(       )(       )(  ___  )
| (    \/| () () || () () || (   ) |
| (__    | || || || || || || (___) |
|  __)   | |(_)| || |(_)| ||  ___  |
| (      | |   | || |   | || (   ) |
| (____/\| )   ( || )   ( || )   ( |
(_______/|/     \||/     \||/     \|
                                    
 _______          _________ _______ __________________
(  ____ \|\     /|\__   __/(  ____ \|__   __/\__   __/
| (    \/| )   ( |   ) (   | (    \/   ) (      ) (   
| |      | (___) |   | |   | (_____    | |      | |   
| |      |  ___  |   | |   (_____  )   | |      | |   
| |      | (   ) |   | |         ) |   | |      | |   
| (____/\| )   ( |___) (___/\____) |___) (___   | |   
(_______/|/     \|\_______/\_______)\_______/   )_( 

(c) Clinton Boys 2015

-----------
Seats.py
-----------

v1.0 Contains the classes for seats and polling places
	 used by the model. Importantly, results for seats
	 and polling places are handled the same, but are not
	 considered as polls, as they give vote numbers rather
	 than percentages. Hence we need separate helper functions
	 for these objects. 

v2.0 Polling places now take a backseat, initial modelling
	 showing this data is more useful in computing preference data 
	 and redistributions. Greater functionality for redistrubitions 
	 and comparing results over the years. Defensive coding for 
	 errors. 

'''

class PollingPlace(object):

    ##
    ## Polling place objects should be initialised with
    ## just a name, since the seat to which a polling place
    ## belongs can change: this flexibility is used to 
    ## calculate notional margins when seats are redistributed.
    ##

    def __init__(self,name):
        self._name = name
        self._seat = {}
        self._results = {}


    @property
    def name(self):
        return self._name

    @property
    def state(self):
    	try:
        	return self._seat[self._seat.keys()[0]]._state
        except KeyError:
        	print 'Polling Place Error: Polling Place ' + self._name + ' not assigned to any seats.'
        	return ''

    @property
    def seat(self, year):
    	try:
        	return self._seat[year]   
        except KeyError:
        	print 'Polling Place Error: Polling Place ' + self._name + ' not assigned to any seat in ' + str(year) + '.'

    def SetSeat(self,seat,year):
    	self._seat[year] = seat
    	seat.pollingplaces().append(self)

    def AddResults(self,year,results_dict):
        self._results[year] = results_dict

    def GetResults(self,year,party):
        try:
            return self._results[year][party]
        except KeyError:
            print 'Polling Place Error: Party ' + party + ' did not contest ' + self._name + ' in ' + str(year) + '.'
            return 0.00


class Seat(object):

	##
	## Seats exist only in certain years, and can given in each election
	## year of existence a list of linked polling place objects, a list of
	## primary and two-candidate preferred election results for this year, 
	## and swings where applicable for each candidate. They are initialised
	## with their name and the state to which they belong. 
	##

    def __init__(self, name, state, is_non_traditional_tpp = False):
        self._name = name
        self._state = state
        self._pollingplaces = {}
        self._results = {}
        self._swings = {}
        self._cluster_no = -1
        self._is_non_traditional_tpp = is_non_traditional_tpp

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    def pollingplaces(self,year):
    	try:
        	return self._pollingplaces[year]
        except KeyError:
        	print 'Seat Error: No polling places loaded for ' + self._name + ' in ' + str(year) + '.'

    def AddResults(self,year,results_dict):
        self._results[year] = results_dict

    def AddSwings(self,year,results_dict):
    	self._swings[year] = results_dict

    def results(self, year, party = None):
        if party is not None:
            try:
                return self._results[year][party]
            except KeyError:
                return 0.00
        else:
            try:
                return self._results[year]
            except KeyError:
                print 'Seat Error: No results for seat ' + self._name + ' in ' + str(year) + '.'
                return 0.00

    def swing(self,year,party=None):
    	if party is not None:
    		try:
    			return self._swings[year][party]
    		except KeyError:
    			return 0.00
    	else:
	        try:
	            return self._swings[year]
	        except KeyError:
	            print 'Seat Error: No swing recorded for seat ' + self._name + ' in ' +str(year) + '.'
	            return 0.00

	## By default, the cluster number is set to -1. If clustering is 
	## performed, a non-negative integer will be generated for the seat. 

    def cluster_no(self):
    	if self._cluster_no == -1:
    		print 'Seat Error: Seat ' + self._name + 'not included in any cluster.'
        return self._cluster_no

def join_coalition(results_dict):

	liberal = 0
	national = 0
	liberal_party = None
	national_party = None

	for party in ['LIB', 'LP', 'LNQ']:
		if results_dict.has_key(party):
			liberal = liberal + results_dict[party]
			liberal_party = party
		else:
			pass
	for party in ['NAT', 'NP']:
		if results_dict.has_key(party):
			national = national + results_dict[party]
    		national_party = party
    	else:
    		pass
	new_results_dict = {'COA': liberal + national}
	for party in results_dict:
		if party not in ['LIB', 'LP', 'LNQ', 'NAT', 'NP', 'COA']:
			new_results_dict[party] = results_dict[party]
	return new_results_dict

def join_others(results_dict, others = []):

	major_parties = ['ALP', 'COA', 'LIB', 'LP', 'NP', 'NAT', 'GRN', 'LNQ', 'OTH']
	if len(others) > 0:
		for party in others:
			major_parties.append(party) 
	try:
		others_vote = results_dict['OTH']
	except KeyError:
		others_vote = 0
	for party in results_dict:
		if party not in major_parties:
			others_vote = others_vote + results_dict[party]
	new_results_dict = {'OTH': others_vote}
	for party in major_parties:
		try:
			new_results_dict[party] = results_dict[party]
		except KeyError:
			pass
	return new_results_dict
