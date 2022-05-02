class Report:
    def __init__(self, squadron, hangar, sampleDate,timeSinceOverhaul, 
                iron, titanum, otherMetals, scale, testNumber, tailNumber,
                partNumber, flightNumber,conclusion):
        self.testNumber = testNumber
        self.tailNumber = tailNumber
        self.partNumber = partNumber
        self.flightNumber = flightNumber
        self.conclusion = conclusion
        self.squadron = squadron
        self.hangar = hangar
        self.sampleDate = sampleDate
        self.timeSinceOverhaul = timeSinceOverhaul
        self.iron = iron
        self.titanum = titanum 
        self.otherMetals = otherMetals
        self.scale = scale
        
