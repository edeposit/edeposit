*** Settings ***
Library    Selenium2Library    5    run_on_failure=Capture Page Screenshot
Library    Dialogs
Library    String
Test Setup      Open Browser      ${PLONE_URL}
Test Teardown   Close Browser
Variables       it_variables.py
Resource       it-keywords.robot

*** Variables ***
${PLONE_URL}        http://edeposit-test.nkp.cz
    
*** Test Cases ***

Problem s roli akvizitora
    Go to   http://edeposit-aplikace.nkp.cz/producents/zizala/epublications/patobiomechanika-srdecnecevniho-systemu
    Log in As acquisitor
    nema opravneni na zobrazeni original souboru
    nema opravneni na zobrazeni historie
    nevidi ani stav
    nevidi producenty cekajici ke schvaleni