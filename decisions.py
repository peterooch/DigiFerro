
# Bin indices
SMALLER_THAN_75 = 0
BETWEEN_75_105  = 1
BETWEEN_105_120 = 2
LARGER_THAN_120 = 3

def fragment_decision(dist):
    if dist[LARGER_THAN_120] > 3:
        return 0
    if dist[LARGER_THAN_120] > 0:
        return 7
    if dist[BETWEEN_105_120] > 3:
        return 10
    if dist[BETWEEN_105_120] > 0:
        return 15
    if dist[BETWEEN_75_105] > 10:
        return 15
    if dist[BETWEEN_75_105] > 0:
        return 27.5
    # default return value (deduced from chart)    
    return 27.5

def spec_decision(iron, titanium, others):
    pass

def rubbing_decision(precent):
    return 27.5
