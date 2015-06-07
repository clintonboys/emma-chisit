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

    def __init__(self, name, state):
        self._name = name
        self._state = state
        self._pollingplaces = {}
        self._results = {}
        self._swings = {}
        self._cluster_no = -1

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