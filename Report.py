class Report:
    def __init__(self, squadron, hangar, sampleDate,timeSinceOverhaul, 
                iron, titanium, otherMetals, scale, testNumber, tailNumber,
                partNumber,conclusion):
        self.testNumber = testNumber
        self.tailNumber = tailNumber
        self.partNumber = partNumber
        self.conclusion = conclusion
        self.squadron = squadron
        self.hangar = hangar
        self.sampleDate = sampleDate
        self.timeSinceOverhaul = timeSinceOverhaul
        self.iron = iron
        self.titanium = titanium 
        self.otherMetals = otherMetals
        self.scale = scale
    
