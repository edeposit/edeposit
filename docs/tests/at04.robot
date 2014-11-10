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

AT04-01 Pracovni prostredi administratora katalogizace
    Log In                  ${LIBRARY_ADMINISTRATOR}     ${LIBRARY_ADMINISTRATOR_PASSWORD}
    Click Logo
    Existuje portlet    Práce pro jmenný popis
    Existuje portlet    Práce pro revizi jmenného popisu
    Existuje portlet    Příprava jmenného popisu
    
AT04-02 Příprava jmenné katalogizace
    Otevřít email s přehledem originálů k přípravě jmenné katalogizace
    Klik na jeden original v emailu
    Log In      ${DESCRIPTIVE_CATALOGUING_ADMINISTRATOR}    ${DESCRIPTIVE_CATALOGUING_ADMINISTRATOR_PASSWORD}
    Existuje portlet     Čeká na přidělení
    Vybrat katalogizátora    JP Katalogizator
    

AT04-03 Jmenný popis
    Otevřít email s přehledem originálů k přípravě jmenného popisu
    Klik na jeden original v emailu
    Log In      ${DESCRIPTIVE_CATALOGUER}    ${DESCRIPTIVE_CATALOGUER_PASSWORD}
    V Alephu potvrdit jmennou katalogizaci
    eDeposit načte změny v Alephu
    Originál je ve stavu  Příprava revize jmenného popisu


AT04-04 Příprava revize jmenného popisu
    Otevřít email s přehledem originálů k přípravě revize jmenného popisu
    Klik na jeden original v emailu
    Log In      ${DESCRIPTIVE_CATALOGUING_ADMINISTRATOR}    ${DESCRIPTIVE_CATALOGUING_ADMINISTRATOR_PASSWORD}
    Existuje portlet     Čeká na přidělení
    Vybrat revizoza    JP Revizor
    Originál je ve stavu  Revizor jmenného popisu

AT04-05 Revize jmenného popisu
    Otevřít email s přehledem originálů k revizi jmenného popisu
    Klik na jeden original v emailu
    Log In      ${DESCRIPTIVE_CATALOGUING_REVIWER}    ${DESCRIPTIVE_CATALOGUING_REVIWER_PASSWORD}
    V Alephu potvrdit revizi jmenné katalogizace
    eDeposit načte změny v Alephu
    Originál je ve stavu  Příprava věcného popisu

AT04-06 Příprava věcné katalogizace
    Otevřít email s přehledem originálů k přípravě věcné katalogizace
    Klik na jeden original v emailu
    Log In      ${SUBJECT_CATALOGUING_ADMINISTRATOR}    ${SUBJECT_CATALOGUING_ADMINISTRATOR_PASSWORD}
    Existuje portlet     Čeká na přidělení
    Vybrat katalogizátora    VP Katalogizator
    Originál je ve stavu    Věcný popis

AT04-07 Věcný popis
    Otevřít email s přehledem originálů k věcnému popisu
    Klik na jeden original v emailu
    Log In      ${SUBJECT_CATALOGUER}    ${SUBJECT_CATALOGUER_PASSWORD}
    V Alephu potvrdit věcnou katalogizaci
    eDeposit načte změny v Alephu
    Originál je ve stavu  Příprava revize věcného popisu

AT04-08 Příprava revize věcného popisu
    Otevřít email s přehledem originálů k přípravě revize věcného popisu
    Klik na jeden original v emailu
    Log In      ${SUBJECT_CATALOGUING_ADMINISTRATOR}    ${SUBJECT_CATALOGUING_ADMINISTRATOR_PASSWORD}
    Existuje portlet     Čeká na přidělení
    Vybrat revizora    VP Revizor
    Originál je ve stavu  Revize věcného popisu


AT04-09 Revize jmenného popisu
    Otevřít email s přehledem originálů k revizi věcného popisu
    Klik na jeden original v emailu
    Log In      ${SUBJECT_CATALOGUING_REVIWER}    ${SUBJECT_CATALOGUING_REVIWER_PASSWORD}
    V Alephu potvrdit revizi věcného popisu
    eDeposit načte změny v Alephu
    Originál je ve stavu  Čekáme na LTP
