*** Settings ***

Resource  plone/app/robotframework/selenium.robot

Test Setup  Open browser   ${PLONE_URL}   firefox
Test Teardown  Close all browsers

Library  Remote  ${PLONE_URL}/RobotRemote
Library  Dialogs

*** Test Cases ***

Domovská stránka
    Page Should Contain Link    Registrovat
    Page Should Contain Link    Přihlášení
    Page Should Contain Link    Smlouva s Národní knihovnou
    Page Should Contain Element    css=h1
    Capture Page Screenshot      home-page.png
    Title Should be   E-Deposit - portál pro ohlašování elektronických publikací

Registrace producenta
    Pause Execution
    Click link        Registrovat
    Page Should Contain   		Registrace producenta
    Page Should Contain Button   	Registrovat
    Input Text				css=#form-widgets-home_page   http://www.e-deposit.cz
    Input Text				css=#form-widgets-location   Praha
    Input Text				css=#form-widgets-contact   Jan Stavěl
    Click Link				Adresa
    Input Text				css=#form-widgets-street  Pašovice 71
    Input Text 				css=#form-widgets-city  Prakšice
    Input Text    			css=#form-widgets-country  Česká republika
    Click Element			css=#fieldsetlegend-agreement
    Click Button			Registrovat    
