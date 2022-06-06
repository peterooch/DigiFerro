import os
import sys
from jinja2 import Template
import pdfkit

from util import resource_path

# DigiFerro
# Programmers:
# Baruch Rutman
# Roi Amzallag

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
    # use method chaining for more compact syntax
    def generateHtml(self):
        os.makedirs('.cache', exist_ok=True)
        with open(resource_path('report_template.htm'), 'r', encoding='utf-8') as f:
            html = f.read()
        file = Template(html)
        result = file.render(testNum=self.testNumber, tailNum=self.tailNumber, partNum=self.partNumber, flightNum=self.timeSinceOverhaul)
        with open('.cache/report.html', 'w', encoding='utf-8') as f:
            f.write(result)
        return self
    def htmlTopdf(self): 
        pdfkit.from_file('.cache/report.html', 'report.pdf')   
        return self
    def show_pdf(self):
        if sys.platform == "win32":
            os.startfile('report.pdf')

if __name__ == "__main__":
    r = Report(0,0,1,5,6,2,8,4,5,6,5,8)
    r.generateHtml().htmlTopdf()
