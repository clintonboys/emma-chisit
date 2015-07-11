## Emma Chisit
### A data-driven model for Australian federal and state elections

See [this](http://www.clintonboys.com/emma-chisit/) page for a timeline of the project's progress. 

### I. Data.

The model combines data from a number of different sources. The data from the model alone is probably an invaluable resource to people analysing Australian elections: I'm unaware of anywhere else all this data is stored in an accessible way. Most of the data for this project is not fully collected and this is still a work in progress. 

- **Federal polling data** was obtained from the Phantom Trend's [github repository](https://github.com/PhantomTrend/ptcode) containing a wealth of federal poll data back to 2000. 

- For **state polling data** I had to spend countless hours mining the web: 

    *Newspoll*. This is the easiest of the lot. Newspoll keeps fantastic online archives of its polls, federal and all six states, [here](http://polling.newspoll.com.au/cgi-bin/polling//display_poll_data.pl?url_caller=trend); the only difficulty is cleaning it all up into csv files. They all go back further than 2000 so I included the pre-2000 polls in other files. 

    *Morgan*. All of Morgan's polls **are** available [here](http://www.roymorgan.com/findings) but finding them is a matter of fishing through their 39 000 findings. This took a while and is probably something I should have scraped, but this would have been a pretty tricky task. 

    *ReachTEL*. The only ReachTEL data I could find is on their website [here](https://www.reachtel.com.au/blog/category/tags/new-south-wales) (and various other tags). ReachTEL has only been polling since around 2013 so it's probable these are all their polls.

Both the federal and state polling data are stored in `/data/polling_data`. 

- **Marginal poll data** was obtained by scraping the Ghost Who Votes twitter feed. This mysterious feed is the most comprehensive source of Australian poll data that I could find online. The scraping and parsing code is stored in `data/ghost_who_votes`.

- **Demographic data** was obtained from the ABS census repository websites and is stored in `data/demographic data`

- **Leader satisfaction data** was scraped from the Newspoll history and is stored, together with the scraper and parser used, in `data/leader_sat_data`.

- **Preference data** and **past election data** were obtained from the fantastic databases of the AEC: these are stored in `data/preference_data` and `data/election_data` respectively.

- **Economic data** are also obtained from the ABS' collection of various economic data points. This data is not as regularly collected as I would like, so I have so far not incorporated it into the model and it is very incomplete. It is stored in `data/economic_data`. 

### II. Model components

The Emma Chisit model is built from a number of pieces. The model is built entirely in Python. The early versions of most of the pieces are stored in the folder `version_1`. The file `SecondModel.py` contains the code I currently use to stitch the pieces together; this is frequently changing as I tinker with the model. 

- `ApplySwings.py` takes a dictionary of swings and applies them to seats. 
- `ClusterSeats.py` uses the *k*-means algorithm to cluster seats according to demographic variables. 
- `MarginalTrendAdjustments.py` makes adjustments to implied swings on certain seats which were polled individually. 
- `PollAggregator.py` takes a weighted aggregate of polls. 
- `Polls.py` contains the classes for polls and elections that the model uses. 
- `PollsterWeights.py` computes the accuracy weights for each pollster to be used in the aggregate. 
- `RunoffElection.py` uses primary vote data and historical preference data to simulate an election in a particular seat using the single transferable vote method with instant runoff voting, which is the electoral system used in most Australian lower houses.  
- `Seats.py` contains the classes for seats and polling places that the model uses.

### III. Coming attractions

I'm working on a number of additional pieces for the model; these are outlined in [this](http://www.clintonboys.com/aus-election-model-9/) post. 





