import xml.sax

class GleifContentHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.current_element = None
        xml.sax.ContentHandler.__init__(self)
        
    def startElement(self, name, attrs):
        self.current_element = name[1]
        print 'element: ' + name
        
    def startElementNS(self, name, qname, attrs):
        self.current_element = name[1]
        # print 'elementNS: ' + str(name)
        print 'elementNS: ' + name[1]
        # print 'elementNS: ' + str(qname) 
    def endElement(self, name):
        self.current_element = None
        
    def endElementNS(self, name, qname):
        self.current_element = None
        
    def ignorableWhitespace(self, whitespace):
        print "in ignorable"
        
    def characters(self, content):
        if self.current_element:
            if content.strip(): 
                print '\t' + self.current_element + ': ' + content
            else:
                print self.current_element + ': CONTAINER'
                
class GleifElementHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.current_element = []
        xml.sax.ContentHandler.__init__(self)
        
    def startElementNS(self, name, qname, attrs):
        self.current_element.append(name[1])
        print self.current_element
        
    def endElementNS(self, name, qname):
        self.current_element.pop()
        
if __name__ == "__main__":
    source = open("/home/ubuntu/workspace/leiquery/gleif_downloads/20151027-GLEIF-concatenated.xml")
    xml_parser = xml.sax.make_parser()
    handler = GleifElementHandler()
    xml_parser.setContentHandler(handler)
    xml_parser.setFeature(xml.sax.handler.feature_namespaces, True)
    xml_parser.parse(source)