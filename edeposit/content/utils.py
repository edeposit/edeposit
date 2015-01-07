from edeposit.amqp import aleph
from functools import partial

def loadFromAlephByISBN(isbn):
    print "load from Aleph by ISBN"
    isbn = '978-80-243-4116-3'
    result = aleph.reactToAMQPMessage(aleph.SearchRequest(aleph.ISBNQuery(isbn, base='nkc')),'UUID')
    return result.records


def is_valid_isbn(isbn):
    valid = aleph.isbn.is_valid_isbn(isbn)
    return valid


def getISBNCount(isbn,base='nkc'):
    appearedAtAleph = aleph.aleph.getISBNCount(isbn, base='nkc')
    return

