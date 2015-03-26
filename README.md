## Emma Chisit
### A data-driven model for Australian federal and state elections

26/3/15: This model is still in very early stages of development. I'm currently spending a lot of time building a poll database for state polls. 

1. **Polling data**

Federal polling data was obtained from the Phantom Trend's [github repository](https://github.com/PhantomTrend/ptcode) containing a wealth of federal poll data back to 2000. 

For state polling data I had to spend countless hours mining the web. 

*Newspoll*. This is the easiest of the lot. Newspoll keeps fantastic online archives of its polls, federal and all six states, [here](http://polling.newspoll.com.au/cgi-bin/polling//display_poll_data.pl?url_caller=trend); the only difficulty is cleaning it all up into csv files. They all go back further than 2000 so I included the pre-2000 polls in other files. 

*Morgan*. All of Morgan's polls **are** available [here](http://www.roymorgan.com/findings) but finding them is a matter of fishing through their 39 000 findings. This took a while and is probably something I should have scraped, but this would have been a pretty tricky task. 
