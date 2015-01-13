from edeposit.amqp import aleph
from functools import partial

def loadFromAlephByISBN(isbn):
    result = aleph.reactToAMQPMessage(aleph.SearchRequest(aleph.ISBNQuery(isbn, base='nkc')),'UUID')
    return result.records


def is_valid_isbn(isbn):
    return aleph.isbn.is_valid_isbn(isbn)

def getISBNCount(isbn, base='nkc'):
    return aleph.aleph.getISBNCount(isbn, base='nkc')

