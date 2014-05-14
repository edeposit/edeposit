*** Settings ***
Library    Selenium2Library   5
Library    Dialogs
Library    String
Test Setup      Open Browser      ${PLONE_URL}
Test Teardown   Close Browser
Variables       variables.py
Resource        my-keywords.robot
Resource        it-variables.robot
Resource        it-keywords.robot

*** Variables ***
${PLONE_URL}        http://edeposit-aplikace.nkp.cz
#${PLONE_URL}        http://localhost:8080/edeposit
${USER_NAME}        alzaltest
${USER_PASSWORD}    mentostest
${ISBN}             978-80-251-2235-8
${TITLE}            Jak vést a motivovat lidi
${AUTHOR}            Bělohlávek František
${NAKLADATEL}       Computer Press a.s.
${PRICE}            230
${MISTO_VYDANI}     Brno
${DATUM_VYDANI_DAY}  23
${DATUM_VYDANI_YEAR}  2008
${PORADI_VYDANI}      páte    
${ZPRACOVATEL_ZAZNAMU}   AZ
        
    
# ${TEST_SEED} ... nahodny string
    
*** Test Cases ***

Ohlašení knihy s jiz pouzitym ISBN
    Log in             ${USER_NAME}    ${USER_PASSWORD}
    Click Link                            Ohlášení ePublikací
    Wait Until Page Contains Element      css=input[value="Ohlásit"]
    Add Original Files for ePublication   ${ISBN}
    Fill inputs about ePublication
    Wait Until Page Contains              isbn je už použito. Použijte jíné, nebo nahlašte opravu.
    Add authors for ePublication          ${AUTHOR}
    Fill nakladatel                       ${NAKLADATEL}
    Fill cena                             ${PRICE}
    Fill misto vydani                     ${MISTO_VYDANI}
    Fill poradi vydani                    ${PORADI_VYDANI}
    Fill zpracovatel                      ${ZPRACOVATEL_ZAZNAMU}
    Fill datum vydani                     ${DATUM_VYDANI_DAY}   ${DATUM_VYDANI_YEAR}
    Click Button                          form.buttons.save    
    Wait Until Page Contains              isbn je už použito. Použijte jíné, nebo nahlašte opravu.

*** Keywords ***
