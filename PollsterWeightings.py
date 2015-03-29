import pandas as pd
import numpy as np
import LoadData

vic_polls = LoadData.LoadPolls('VIC')
nsw_polls = LoadData.LoadPolls('NSW')
sa_polls = LoadData.LoadPolls('SA')
wa_polls = LoadData.LoadPolls('WA')
qld_polls = LoadData.LoadPolls('QLD')
tas_polls = LoadData.LoadPolls('TAS')

elections_from_2000 = LoadData.LoadElections()

print elections_from_2000[1]