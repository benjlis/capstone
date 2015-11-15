import xml.sax
import unicode_csv
from models import LegalEntity
from database import session
from sqlalchemy.exc import DataError, IntegrityError

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
    def __init__(self):
        self.in_lei_record = False
        self.current_element = None
        self.address_type = None
        xml.sax.ContentHandler.__init__(self)
        
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
        #self.csv_writer.writerow(self.legal_entity)
        pass
    
class LEIRecordHandlerCsv(LEIRecordHandler):
    def __init__(self, csvfile):
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
        self.csv_writer = unicode_csv.DictUnicodeWriter(dest, fieldnames=fieldnames, extrasaction='ignore')
        LEIRecordHandler.__init__(self)
    
    def addLEIRecord(self):
        self.csv_writer.writerow(self.legal_entity)
        
class LEIRecordHandlerDB(LEIRecordHandler):
    def __init__(self):
        self.db_record_cnt = 0      # running count of LEI records processed
        self.db_error_cnt = 0   # count of db errors
        self.db_interval = 500      # frequency of commits and log message
        
        LEIRecordHandler.__init__(self)
    
    def addLEIRecord(self):
        db_record = LegalEntity()
        db_record.lei = self.legal_entity.get('LEI', None)
        db_record.legal_name = self.legal_entity.get('LegalName', None)  
        db_record.legal_address_line1 = self.legal_entity.get('LegalAddressLine1', None)  
        db_record.legal_address_line2 = self.legal_entity.get('LegalAddressLine2', None)  
        db_record.legal_address_line3 = self.legal_entity.get('LegalAddressLine3', None)  
        db_record.legal_address_line4 = self.legal_entity.get('LegalAddressLine4', None)  
        db_record.legal_address_city = self.legal_entity.get('LegalAddressCity', None)  
        db_record.legal_address_region = self.legal_entity.get('LegalAddressRegion', None)  
        db_record.legal_address_country = self.legal_entity.get('LegalAddressCountry', None)  
        db_record.legal_address_postal_code = self.legal_entity.get('LegalAddressPostalCode', None)  
        db_record.hq_address_line1 = self.legal_entity.get('HeadquartersAddressLine1', None)  
        db_record.hq_address_line2 = self.legal_entity.get('HeadquartersAddressLine2', None)  
        db_record.hq_address_line3 = self.legal_entity.get('HeadquartersAddressLine3', None)  
        db_record.hq_address_line4 = self.legal_entity.get('HeadquartersAddressLine4', None)  
        db_record.hq_address_city = self.legal_entity.get('HeadquartersAddressCity', None)  
        db_record.hq_address_region = self.legal_entity.get('HeadquartersAddressRegion', None)  
        db_record.hq_address_country = self.legal_entity.get('HeadquartersAddressCountry', None)  
        db_record.hq_address_postal_code = self.legal_entity.get('HeadquartersAddressPostalCode', None)  
        db_record.business_registry = self.legal_entity.get('BusinessRegister', None)  
        db_record.business_registry_id = self.legal_entity.get('BusinessRegisterEntityID', None)  
        db_record.legal_jurisdiction = self.legal_entity.get('LegalJurisdiction', None)  
        db_record.legal_form = self.legal_entity.get('LegalForm', None)  
        db_record.entity_status = self.legal_entity.get('EntityStatus', None)  
        db_record.entity_expiration_date = self.legal_entity.get('EntityExpirationDate', None)  
        db_record.entity_expiration_reason = self.legal_entity.get('EntityExpirationReason', None)  
        db_record.successor_lei = self.legal_entity.get('SuccessorLEI', None)
        db_record.initial_registration_date = self.legal_entity.get('InitialRegistrationDate', None)  
        db_record.last_update_date = self.legal_entity.get('LastUpdateDate', None)  
        db_record.registration_status = self.legal_entity.get('RegistrationStatus', None)  
        db_record.next_renewal_date = self.legal_entity.get('NextRenewalDate', None)  
        db_record.managing_lou = self.legal_entity.get('ManagingLOU', None)  
        db_record.validation_status = self.legal_entity.get('ValidationSources', None) 
        self.db_record_cnt += 1
        try:
            session.add(db_record)
            session.commit()
        except (DataError, IntegrityError) as e:
            self.db_error_cnt += 1
            session.rollback()
            print "==========================="
            print "LEI:             " + self.legal_entity.get('LEI', 'No LEI')
            print "DB record count: " + str(self.db_record_cnt)
            print "DB error count:  " + str(self.db_error_cnt)
            print e.orig.message, e.params
        #
        #if self.db_record_cnt % self.db_interval == 0:
        #    #session.commit()
        #    print str(self.db_record_cnt) + "LEI Records Loaded"

        
def run_parser(xmlfile, handler):
    """Creates configures and runs the XML parser"""
    source = open(xmlfile)
    xml_parser = xml.sax.make_parser()
    xml_parser.setContentHandler(handler)
    xml_parser.setFeature(xml.sax.handler.feature_namespaces, True)
    xml_parser.parse(source)


def process_gleif(xmlfile, csvfile):
    """Parse the GLEIF XML file and store important data elements into a csv file"""
    # Create the content handler
    handler = LEIRecordHandlerCsv(csvfile)
    # Run the parser
    run_parser(xmlfile, handler)

def process_gleif(xmlfile):
    """Parse the GLEIF XML file and store important data elements in db"""
    handler = LEIRecordHandlerDB()
    run_parser(xmlfile, handler)
    
if __name__ == "__main__":
    process_gleif("/home/ubuntu/workspace/leiquery/gleif_downloads/20151109-GLEIF-concatenated.xml")
    #       , "/home/ubuntu/workspace/leiquery/gleif_downloads/test.csv")
