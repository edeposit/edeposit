import os.path
import pickle

def loadFromAlephByISBN(isbn,num_of_records=0):
    print "load from Aleph by ISBN - mock with one record"
    # isbn = "80-85601-24-9" # Karel May : Ahriman Mirza # one record
    #isbn = '978-80-243-4116-3'
    fname = os.path.join(os.path.dirname(__file__),'browser','records-from-aleph-%d.pickle' %(num_of_records,))
    records = os.path.exists(fname) and pickle.loads(open(fname,"rb").read()) or []
    return records

def is_valid_isbn(isbn, result=True):
    return result

def getISBNCount(isbn,base='nkc',result=0):
    return result

def getAlephRecord():
    print "mock - get one aleph record - mock with one record"
    # isbn = "80-85601-24-9" # Karel May : Ahriman Mirza # one record
    #isbn = '978-80-243-4116-3'
    return loadFromAlephByISBN("",1)[0]
    
