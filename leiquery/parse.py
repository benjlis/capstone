import xml.sax
import unicode_csv


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
        
class LEIRecordHandler(xml.sax.ContentHandler):
    def __init__(self, csv_writer):
        self.in_lei_record = False
        self.current_element = None
        self.address_type = None
        self.csv_writer = csv_writer
        xml.sax.ContentHandler.__init__(self)
        
    def start_document(self):
        csv_writer.writeheader()
        
    def startElementNS(self, name, qname, attrs):
        if name[1] == 'LEIRecord':
            self.in_lei_record = True
            self.legal_entity = {}
        elif self.in_lei_record:
            if name[1].endswith('Address'):
                self.address_type = name[1]
            else:
                self.current_element = name[1]
        
    def endElementNS(self, name, qname):
        if name[1] == 'LEIRecord':
            self.addLEIRecord()
            self.in_lei_record = False
        elif self.in_lei_record:
            if name[1].endswith('Address'):
                self.address_type = None
            else:
                self.current_element = None
            
    def characters(self, content):
        data = content.strip()
        if self.current_element and data:
           self.legal_entity[self.address_type + self.current_element if self.address_type 
                                    else self.current_element] = data 
            
    def addLEIRecord(self):
        #print 'a new record.....'
        #for key, value in self.legal_entity.items():
        #    print key + ': ' + value
        self.csv_writer.writerow(self.legal_entity)
            
    def endDocument(self):
        pass

def process_gleif(xmlfile, csvfile):
    """Parse the GLEIF XML file and store important data elements into a csv file"""
    # Create and configure the CSV writer
    dest = open(csvfile, 'w')
    fieldnames = ['LEI', 'LegalName', 
        'LegalAddressLine1', 'LegalAddressLine2', 'LegalAddressLine3', 'LegalAddressLine4', 
        'LegalAddressCity', 'LegalAddressRegion', 'LegalAddressCountry', 'LegalAddressPostalCode',  
        'HeadquartersAddressLine1', 'HeadquartersAddressLine2', 'HeadquartersAddressLine3', 
        'HeadquartersAddressLine4', 'HeadquartersAddressCity', 'HeadquartersAddressRegion', 
        'HeadquartersAddressCountry', 'HeadquartersAddressPostalCode', 
        'BusinessRegister','BusinessRegisterEntityID','LegalJurisdiction', 'LegalForm',
        'EntityStatus', 'EntityExpirationDate', 'EntityExpirationReason', 'SuccessorLEI',
        'InitialRegistrationDate', 'LastUpdateDate', 'RegistrationStatus', 'NextRenewalDate',
        'ManagingLOU', 'ValidationSources']
    csv_writer = unicode_csv.DictUnicodeWriter(dest, fieldnames=fieldnames, extrasaction='ignore')
    # Create and configure the XML parser
    source = open(xmlfile)
    xml_parser = xml.sax.make_parser()
    handler = LEIRecordHandler(csv_writer)
    xml_parser.setContentHandler(handler)
    xml_parser.setFeature(xml.sax.handler.feature_namespaces, True)
    xml_parser.parse(source)
    
if __name__ == "__main__":
    process_gleif("/home/ubuntu/workspace/leiquery/gleif_downloads/test.xml",
            "/home/ubuntu/workspace/leiquery/gleif_downloads/test.csv")
