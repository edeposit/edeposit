# -*- coding: utf-8 -*-
PLONE_URL=        "http://edeposit-test.nkp.cz"

from edeposit.amqp.aleph.datastructures import epublication

import os,binascii
TEST_SEED=binascii.b2a_hex(os.urandom(15))[:5]

QUEUE_NAME=             "-".join(['acceptation-tests-queue',TEST_SEED,'01'])

VALID_ISBN=                  "978-0-306-40615-7"
VALID_ENGLISH_ISBN=          "978-0-306-40615-7"
VALID_BUT_DUPLICIT_ISBN=     "80-85432-66-8"
WRONG_ISBN=                  "80-12312-3241-324124"

EPUBLICATION_ID = "dervis"

ePublication_IN_ALEPH = epublication.EPublication(
    ISBN = VALID_BUT_DUPLICIT_ISBN,
    nazev = u'Derviš :',
    podnazev =  u'[1. román z cyklu Třemi díly světa] /',
    vazba = u'pevná',
    cena = '59',
    castDil = '',
    nazevCasti = '',
    nakladatelVydavatel = u"Návrat",
    datumVydani = "1993",
    poradiVydani = u'1. vyd.',
    zpracovatelZaznamu = 'A',
    format = '',
    url = '',
    mistoVydani = u'Brno',
    ISBNSouboruPublikaci = '',
    autori    = [epublication.Author(firstName="Karel", lastName="May", title="")],
    originaly = [] ,
    internal_url = ""
)

PRODUCENT_ID=           "zlinsky-vydavatel"
PRODUCENT_TITLE=        u"Zlínsky vydavatel"

USER_NAME=       "jans"
USER_PASSWORD=   ""
    
EDITOR1_NAME=       "editor1"
EDITOR1_PASSWORD=   ""
    
EDITOR2_NAME=       "editor2"
EDITOR2_PASSWORD=   ""
    
EDITOR3_NAME=       "editor3"
EDITOR3_PASSWORD=   ""

AKVIZITOR_NAME=     "akvizitor"
AKVIZITOR_PASSWORD= ""

RIV_NAME=     "akvizitor"
RIV_PASSWORD= ""

SYSTEM_USER_PASSWORD = ""
SYSTEM_USER_NAME = "system"

from my_variables import *
