from jinja2 import Template
import pdfkit
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
    def generateHtml(self):
        with open('output2.html', 'r', encoding='utf-8') as f:
            html = f.read()
        file = Template(html)
        result = file.render(testNum=self.testNumber, tailNum=self.tailNumber, partNum=self.partNumber, flightNum=self.timeSinceOverhaul)
        with open('result.html', 'w') as r:
            r.write(result)
    def htmlTopdf(self): 
        pdfkit.from_file('result.html', 'out.pdf')   

r = Report(0,0,1,5,6,2,8,4,5,6,5,8)
r.generateHtml()
r.htmlTopdf()


