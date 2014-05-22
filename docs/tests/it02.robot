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
${PLONE_URL}        http://localhost:8080/Plone
${USER_PASSWORD}    fafs08ja
        
# ${TEST_SEED} ... nahodny string
    
*** Test Cases ***

# UC00 Instalace produktu
#     # update security
#     # reguild catalog
    
# UC01 Registrace producenta
#     ${USER_NAME}=     Catenate     SEPARATOR=-  test-user   ${TEST_SEED}
#     Registrace producenta
#     Page Should Contain            Vítejte!
#     Log in                         ${USER_NAME}   ${USER_PASSWORD}
#     Page Should Contain            Přehledová stránka uživatele
    
UC02 Ohlášení ePublikace
    ${USER_NAME}=                    Catenate     SEPARATOR=-  test-user   ${TEST_SEED}
    Registrace producenta
    Log in                           ${USER_NAME}   ${USER_PASSWORD}
    Click Link                            Ohlášení ePublikací
    Wait Until Page Contains Element      css=input[value="Ohlásit"]
    Pause
    Fill inputs about ePublication    
    Pause
    Add authors for ePublication
    Pause
    Add Original Files for ePublication   ${VALID_ISBN}
    Fill inputs about Vydani
    Click Button                          form.buttons.save    
    Sleep     10s
    Zobrazit historii
    Sleep     1s
    Historie obsahuje zprávu         K akvizici
    Historie obsahuje zprávu         Poslal jsem jeden záznam k exportu do Alephu
    Historie obsahuje zprávu         Export jednoho záznamu do Alephu
    Historie obsahuje zprávu         Všechny exporty do Alephu proběhly úspěšně
    Click Link                       Zobrazení
    Wait Until Page Contains         Čekání na Aleph


# UC02 Ohlášení ePublikace - Diazo Theme - kontrola online validace ISBN
#     ${USER_NAME}=                    Catenate     SEPARATOR=-  test-user   ${TEST_SEED}
#     Registrace producenta
#     Log in                           ${USER_NAME}   ${USER_PASSWORD}
#     Click Link                            Ohlášení ePublikací
#     Wait Until Page Contains Element      css=input[value="Ohlásit"]
#     Fill inputs about ePublication        
#     Fill inputs about Vydani
#     Add authors for ePublication
#     Add Original Files for ePublication   ${WRONG_ISBN}
#     Wait Until Page Contains              chyba v isbn
#     Click Button                          form.buttons.cancel
#     Page Should Contain                   Ohlášení bylo přerušeno.
#     Go to                                 ${PLONE_URL}
#     Click Link                            Ohlášení ePublikací
#     Wait Until Page Contains Element      css=input[value="Ohlásit"]
#     Fill inputs about ePublication        
#     Fill inputs about Vydani
#     Add authors for ePublication
#     Add Original Files for ePublication   ${VALID_BUT_DUPLICIT_ISBN}
#     Wait Until Page Contains              isbn je už použito. Použijte jíné, nebo nahlašte opravu.
    
*** Keywords ***
