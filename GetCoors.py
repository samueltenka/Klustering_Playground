'''
parses xml file of ocr'd string-location data:
   <String ID="TB.0005.2_0_0" STYLEREFS="TS_10.0" HEIGHT="156.0" WIDTH="448.0" HPOS="540.0" VPOS="1908.0" CONTENT="121st" WC="1.0"/>
and clusters
'''
import Box

p = re.compile('<String ID="(?P<stringid>[^"]*)" ' +
               'STYLEREFS="(?P<stylerefs>[^"]*)" ' +
               'HEIGHT="(?P<height>[^"]*)" ' +
               'WIDTH="(?P<width>[^"]*)" ' +
               'HPOS="(?P<hpos>[^"]*)" ' +
               'VPOS="(?P<vpos>[^"]*)" ' +
               'CONTENT="(?P<content>[^"]*)" ' +
               'WC="(?P<wc>[^"]*)"/>')

class Page:
    def __init__(self, bounding_box):
        self.bb = bounding_box
        self.words = []
    def add_word(self, wordbox):
        self.words.append(wordbox)
        self.bb = self.bb.join(wordbox)
    def read_from(self, filename):
        print('reading [%s]...' % filename)
        with open(filename) as f:
            getnum = lambda match, label: float(match.group(label))
            data = [(getnum(m,'vpos'),getnum(m,'hpos'),
                     getnum(m,'height'),getnum(m,'hpos')) for m in p.finditer(f.read())]
            for (y,x),(h,w) in data:
               self.add_word(Box([y,x],[y+h,x+w]))
        print('found %d ocr points.' % (len(text), len(self.words)))
        print('vpos ranges in [%d,%d]; hpos ranges in [%d,%d]' %
              (self.bb[i][j] for j in range(2) for i in range(2))
