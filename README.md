## Emma Chisit
### A data-driven model for Australian federal and state elections

26/3/15: This model is still in very early stages of development. I'm currently spending a lot of time building a poll database for state polls. 

1. **Polling data**

Federal polling data was obtained from the Phantom Trend's [github repository](https://github.com/PhantomTrend/ptcode) containing a wealth of federal poll data back to 2000. 

For state polling data I had to spend countless hours mining the web. 

*Newspoll*. This is the easiest of the lot. Newspoll keeps fantastic online archives of its polls, federal and all six states, [here](http://polling.newspoll.com.au/cgi-bin/polling//display_poll_data.pl?url_caller=trend); the only difficulty is cleaning it all up into csv files. They all go back further than 2000 so I included the pre-2000 polls in other files. 

*Morgan*. All of Morgan's polls **are** available [here](http://www.roymorgan.com/findings) but finding them is a matter of fishing through their 39 000 findings. This took a while and is probably something I should have scraped, but this would have been a pretty tricky task. 

*ReachTEL*. The only ReachTEL data I could find is on their website [here](https://www.reachtel.com.au/blog/category/tags/new-south-wales) (and various other tags). ReachTEL has only been polling since around 2013 so it's probable these are all their polls.

1.1. **Pollster weightings**

The Python script LoadData.py contains a series of classes to load poll and election data. The script PollsterWeightings.py computes root-mean-square deviation errors for all contests polled, using the final poll released before the election, and averages over all contests. From this we compute the poll weightings we use in the full model. 

2. **Leader satisfaction data**

Newspoll leader satisfaction data goes back to 1985. The file sat.csv contains the raw data cut and pasted from the Newspoll sat; sat_parser.py converts it into the neater file leader_satisfaction.csv which also contains median poll dates. 

