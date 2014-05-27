# -*- coding: utf-8 -*-

import os,binascii
TEST_SEED=binascii.b2a_hex(os.urandom(15))[:5]

USER_NAME=              "jans"
USER_PASSWORD=          "password"
SYSTEM_NAME=            "system"
SYSTEM_PASSWORD=        "password"
PRODUCENT_ID=           "zlinsky-vydavatel"
PRODUCENT_TITLE=        u"Zlínsky vydavatel"

EDITOR1_NAME=       "editor1"
EDITOR1_PASSWORD=   ""
    
EDITOR2_NAME=       "editor2"
EDITOR2_PASSWORD=   ""
    
EDITOR3_NAME=       "editor3"
EDITOR3_PASSWORD=   ""

SYSTEM_USER_PASSWORD=   "password"
SYSTEM_USER_NAME=       "system"
ADMIN_PASSWORD=         "password"
AKVIZITOR_NAME=         "akvizitor"
AKVIZITOR_PASSWORD=     "password"
RIV_NAME=               "riv"

from my_it_variables import *
