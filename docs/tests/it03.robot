*** Settings ***
Library    Selenium2Library    5    run_on_failure=Capture Page Screenshot
Library    Dialogs
Library    String
Library    Collections
    
Test Setup      Open Browser      ${PLONE_URL}
Test Teardown   Close Browser
Variables       it_variables.py
Resource        my-keywords.robot
Resource        it-keywords.robot

*** Variables ***
#${PLONE_URL}        http://edeposit-test.nkp.cz
${PLONE_URL}        http://localhost:8080/Plone

*** Test Cases ***

IT03-01 Nastaveni portletu pro skupinu Acquisitors
    Log in as site owner
    Go To                             ${PLONE_URL}/@@usergroup-userprefs
    Click Link                        Skupiny
    Go To                             ${PLONE_URL}/@@usergroup-groupmembership?groupname=Acquisitors
    Click Link                        Přehledová stránka skupiny
    Select From List                  //div[@id='dashboard-portlets1']//select    /++groupdashboard++plone.dashboard1+Acquisitors/+/portlets.Review

IT03-02 Instalace edeposit modulu
    Log In as Admin
    Reinstall E-Deposit modules

IT03-03 View with Worklist for ISBN Agency
    Log In As Admin
    Reinstall E-Deposit modules
    Open Browser      ${PLONE_URL}
    Log In            ${SYSTEM_NAME}    ${SYSTEM_PASSWORD}
    Go To             ${PLONE_URL}/producents/worklist-for-isbn-agency
    Pause

IT03-04 View with Worklist for Acquisition
    Log In As Admin
    Reinstall E-Deposit modules
    Open Browser      ${PLONE_URL}
    Log In            ${SYSTEM_NAME}    ${SYSTEM_PASSWORD}
    Go To             ${PLONE_URL}/producents/worklist-for-acquisition
    Pause

IT03-05 View with Worklist for Catalogization
    Log In As Admin
    Reinstall E-Deposit modules
    Open Browser      ${PLONE_URL}
    Log In            ${SYSTEM_NAME}    ${SYSTEM_PASSWORD}
    Go To             ${PLONE_URL}/producents/worklist-for-catalogization
    Pause

IT03-06 Pracovni list pro akvizitora
    Log In      ${AKVIZITOR_NAME}    ${AKVIZITOR_PASSWORD}
    Go To       ${PLONE_URL}/producents/
    Page Should Contain    Producenti
    Pause

# pybot  -E star:+ -t IT03-07+ it03.robot 
IT03-07 Pracovní prostředí pracovníka ISBN agentury
    Log In      ${ISBN_AGENCY_USER}    ${ISBN_AGENCY_PASSWORD}
    Page Should Contain     Přehledová stránka uživatele
    Existuje portlet Prideleni ISBN
    Existuje portlet Prehled originalu pro prideleni ISBN
    Click Element   css=#portal-logo
    Existuje portlet Prideleni ISBN
    
*** Keywords ***

Nastaveni portletu pro skupinu Akvizitori
    Go To                             ${PLONE_URL}/@@usergroup-userprefs
    Click Link                        Skupiny
    Go To                             ${PLONE_URL}/@@usergroup-groupmembership?groupname=Acquisitors
    Click Link                        Přehledová stránka skupiny
    Select From List                  //div[@id='dashboard-portlets1']//select    /++groupdashboard++plone.dashboard1+Acquisitors/+/portlets.Review
