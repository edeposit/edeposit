*** Settings ***
Library    Selenium2Library   5
Library    Dialogs
Library    String
Test Setup      Open Browser      ${PLONE_URL}
Test Teardown   Close Browser
Variables       variables.py
            
*** Variables ***
${PLONE_URL}        http://localhost:8080/Plone
${USER_PASSWORD}    fafs08ja
${ADMIN_PASSWORD}   admin

# ${TEST_SEED} ... nahodny string
    
*** Test Cases ***

Nastaveni portletu pro skupinu Akvizitors
    Log in as site owner
    Go To                             ${PLONE_URL}/@@usergroup-userprefs
    Click Link                        Skupiny
    Go To                             ${PLONE_URL}/@@usergroup-groupmembership?groupname=Acquisitors
    Click Link                        Přehledová stránka skupiny
    Select From List                  //div[@id='dashboard-portlets1']//select    /++groupdashboard++plone.dashboard1+Acquisitors/+/portlets.Review

*** Keywords ***

Log in as site owner
    Click Link                 Přihlášení
    Input Text                 css=#__ac_name         admin
    Input Text                 css=#__ac_password     ${ADMIN_PASSWORD}    
    Click Button               Přihlásit se

User Registration
    Click Link                   Registrovat
    Wait Until Page Contains     Přihlásit
    Fill username
    Fill password
    Click Button                 Přihlásit
    Wait Until Page Contains     Osobní údaje
    
Fill password
    Input Text                   css=#pass     ${PASSWORD}    
    
Fill username
    Input Text                   css=#login    ${USERNAME}
    
Pause
    Pause Execution

Nastaveni portletu pro skupinu Akvizitori
    Go To                             ${PLONE_URL}/@@usergroup-userprefs
    Click Link                        Skupiny
    Go To                             ${PLONE_URL}/@@usergroup-groupmembership?groupname=Acquisitors
    Click Link                        Přehledová stránka skupiny
    Select From List                  //div[@id='dashboard-portlets1']//select    /++groupdashboard++plone.dashboard1+Acquisitors/+/portlets.Review
