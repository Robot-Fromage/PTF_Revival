from html.parser import HTMLParser

with open('Raw/CLEAN_PTF_ARCHIVE_KAAOS1.html', 'r') as file:
    data = file.read().replace('\n', '')
   
    
class Parser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag == "span":
            dico = dict( attrs )
            if "class" in dico:
                if dico['class'] == "3D\"postbody\"":
                    print( "Encountered a start tag:", tag, dico['class'] )
                    print( "details:", tag, attrs )
                    self.count = self.count + 1
                    self.readpostbodystate = True
                else:
                    self.readpostbodystate = False
        if tag == "a":
            print( "Encountered a start tag:", tag, attrs )

    def handle_endtag(self, tag):
        dummy=0

    def handle_data(self, data):
        print( "Encountered a data:", data )


parser = Parser()
parser.count = 0
parser.feed( data )
print( parser.count )