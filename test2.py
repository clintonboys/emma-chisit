import pandas as pd

filename = 'data/polling_data/NSW_state_polls.csv'
pollframe = pd.read_csv(filename)

print pollframe.columns[4]

def GetCoalitionLabels(poll):

    lib_count = 0
    nat_count = 0

    for party in liberal_alias:
        if (poll.results(party) != 0) and (poll.results(party) is not np.nan):
            lib_count += 1
            liberal_party = party
    for party in national_alias:
        if (poll.results(party) != 0) and (poll.results(party) is not np.nan):
            nat_count += 1
            national_party = party

    if lib_count == 1:
        if nat_count == 1:
            coalition_labels = [liberal_party, national_party]
        elif nat_count == 0:
            coalition_labels = [liberal_party, None]
        else:
            return 'Label error: more than one party labelled as Nationals'
    elif lib_count == 0:
        if nat_count == 1:
            coalition_labels = [None, national_party]
        if nat_count > 1:
            return 'Label error: more than one party labelled as Nationals'
        if nat_count == 0:
            coa_count = 0
            for party in coalition_alias:
                if (poll.results(party) != 0) and (poll.results(party) is not np.nan):
                    coa_count += 1
                    coalition_party = party
            if coa_count == 0:
                return 'Label error: no coalition party included in poll'
            elif coa_count == 1:
                coalition_labels = [coalition_party]
            else:
                return 'Label error: more than one party labelled as Coalition'
    else:
        return 'Label error: more than one party labelled as Liberals'

    return coalition_labels
