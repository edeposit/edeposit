*** Settings ***

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Test Setup       Open browser and create all folders
Test Teardown    Close all browsers

Library  Remote  ${PLONE_URL}/RobotRemote
Library  Dialogs
Library  OperatingSystem
Library  String
Library  amqp.RabbitMQ
Library  Collections

Resource    my-keywords.robot
Variables   variables.py
        
*** Variables ***
    
*** Keywords ***

*** Test Cases ***

AT04-01 Uvodni stranka administratora katalogizace
    Registrace pracovníků katalogizace
    Log In                  ${LIBRARY_ADMINISTRATOR}     ${LIBRARY_ADMINISTRATOR_PASSWORD}
    Pause
    Page Should Contain Link     Naplánovat práci knihovníkům
    Pause    
    
AT04-02 Příprava katalogizace
    Prepare AMQP Test Environment
    Registrace producenta
    Registrace pracovníků katalogizace
    Log in                              ${USER_NAME}   ${USER_PASSWORD}
    Ohlášení se soubory    ${VALID_ISBN}
    Send ePublication To Acquisition   ${VALID_ISBN}   ${PLONE_URL}/producents/${PRODUCENT_ID}/epublications/lesni-skolky-ve-zline/inzlin-01-2013-s-nasi-tabinkou.pdf
    Click Link      Zobrazení
    Submit Acquisition
    Switch Browser   1
    Ohlášení se soubory    ${VALID_ISBN_01}
    Send ePublication To Acquisition   ${VALID_ISBN}   ${PLONE_URL}/producents/${PRODUCENT_ID}/epublications/lesni-skolky-ve-zline-1/inzlin-01-2013-s-nasi-tabinkou.pdf
    Click Link      Zobrazení
    Submit Acquisition
    Log Out
    Log In                  ${LIBRARY_ADMINISTRATOR}     ${LIBRARY_ADMINISTRATOR_PASSWORD}
    Pause
    Click Button                        Naplánovat prácí katalogizace
    Page Should Contain list of two ePublications
    Page Should Contain list of persons
    Select one person
