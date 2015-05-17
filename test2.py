import LoadData

VIC_polls = LoadData.LoadPolls('VIC')
VIC_polls[0]._results = LoadData.JoinCoalition(VIC_polls[0])
print VIC_polls[0]._results
print LoadData.JoinOthers(VIC_polls[0])