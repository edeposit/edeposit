# -*- coding: utf-8 -*-
PLONE_URL=        "http://edeposit-test.nkp.cz"

from edeposit.amqp.aleph.datastructures import epublication

import os,binascii

TEST_SEED=binascii.b2a_hex(os.urandom(15))[:5]

QUEUE_PREFIX='acceptation-tests-queue'
QUEUE_NAME=             "-".join([QUEUE_PREFIX,TEST_SEED,'01'])

VALID_ISBN=                  "978-80-260-7000-9"
VALID_ENGLISH_ISBN=          "978-0-306-40615-7"
VALID_BUT_DUPLICIT_ISBN=     "80-85432-66-8"
VALID_WITH_2_RECORDS=        "80-85892-15-4"
WRONG_ISBN=                  "80-12312-3241-324124"

VALID_ISBN_01=               "978-80-260-7001-6"
VALID_ISBN_02=               "978-80-260-7002-3"
VALID_ISBN_03=               "978-80-260-7003-0"

FILENAME=                    "inzlin-01-2013-s-nasi-tabinkou"
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

UNIQUE_USER_NAME=       "-".join(['test-user',TEST_SEED,'01'])
UNIQUE_USER_PASSWORD=   ""

NEW_UNIQ_USER_NAME="-".join([USER_NAME,TEST_SEED,binascii.b2a_hex(os.urandom(15))[:5]])
    
ISBN_AGENCY_USER="isbn-agency-user"
ISBN_AGENCY_PASSWORD=""

EDITOR1_NAME=       "editor1"
EDITOR1_PASSWORD=   ""
    
EDITOR2_NAME=       "editor2"
EDITOR2_PASSWORD=   ""
    
EDITOR3_NAME=       "editor3"
EDITOR3_PASSWORD=   ""

AKVIZITOR_NAME=     "akvizitor"
AKVIZITOR_PASSWORD= ""

RIV_NAME=     "riv-user"
RIV_PASSWORD= ""

SYSTEM_USER_PASSWORD = ""
SYSTEM_USER_NAME = "system"

ADMINISTRATOR_NAME="admin"
ADMINISTRATOR_PASSWORD = ""

DESCRIPTIVE_CATALOGUING_ADMINISTRATOR="jp-admin"
DESCRIPTIVE_CATALOGUING_ADMINISTRATOR_PASSWORD=""

DESCRIPTIVE_CATALOGUING_REVIWER="jp-revizor"
DESCRIPTIVE_CATALOGUING_REVIWER_PASSWORD=""

DESCRIPTIVE_CATALOGUER="jp-katalogizator"
DESCRIPTIVE_CATALOGUER_PASSWORD=""

DESCRIPTIVE_CATALOGUER_01="jp-katalogizator-01"
DESCRIPTIVE_CATALOGUER_01_PASSWORD=""

SUBJECT_CATALOGUING_ADMINISTRATOR="vp-admin"
SUBJECT_CATALOGUING_ADMINISTRATOR_PASSWORD=""

SUBJECT_CATALOGUING_REVIWER="vp-revizor"
SUBJECT_CATALOGUING_REVIWER_PASSWORD=""

SUBJECT_CATALOGUING_REVIWER_01="vp-revizor"
SUBJECT_CATALOGUING_REVIWER_01_PASSWORD=""

SUBJECT_CATALOGUER="vp-katalogizator"
SUBJECT_CATALOGUER_PASSWORD=""


from my_variables import *
