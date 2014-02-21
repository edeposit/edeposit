*** Keywords ***

Open browser and create all folders
    Open browser   ${PLONE_URL}   firefox
    Log in as site owner    
    Create producents folder
    Log Out    
    
Page Should Not Contain Error
    Page Should Not Contain        Litujeme, ale tato stránka neexistuje...

Page Does Not Exist
    Page Should Contain        Litujeme, ale tato stránka neexistuje...

Page Does Exist
    Page Should Not Contain        Litujeme, ale tato stránka neexistuje...

Workflow State Is
    [arguments]     ${state_id}
    Page Should Contain Element    css=span.state-${state_id}
    
Add Dexterity Content
    [arguments]  ${url}   ${content_type}   ${title}    
    Go to             ${url}
    Open add new menu

    ${status} =  Run Keyword And Return Status  Click Link
    ...  css=#plone-contentmenu-factories a.contenttype-${content_type}
    Run keyword if  ${status} != True  Click Link  ${content_type}
    Input Text   form.widgets.IBasic.title  ${title}    
    Click button   name=form.buttons.save
    Page Should Contain  Položka byla vytvořena
    Page should contain  ${title}
    ${location} =  Get Location
    [return]  ${location}

Create producents folder
    Add Dexterity Content     ${PLONE_URL}     edeposit-user-producentfolder    producents

User Should Exist
    [arguments]   ${username}
    Go to                   ${PLONE_URL}/@@user-information?userid=jans
    Page Should Contain     Osobní informace

Fill inputs about producent
    Input Text				css=#form-widgets-IBasic-title        ${PRODUCENT_TITLE}
    Input Text				css=#form-widgets-IBasic-description  Malý lokální vydavatel zajímavých publikací 
    Input Text				css=#form-widgets-home_page   http://www.e-deposit.cz
    Input Text				css=#form-widgets-location   Praha
    Input Text				css=#form-widgets-contact   Jan Stavěl
    
Fill inputs about address
    Input Text				css=#form-widgets-street  Pašovice 71
    Input Text 				css=#form-widgets-city  Prakšice
    Input Text    			css=#form-widgets-country  Česká republika
    Input Text    			css=#form-widgets-psc     68756

Add one administrator    
    Click Button                        Přidat
    Input Text                          css=#form-widgets-IProducentAdministrators-administrators-0-widgets-fullname   Jan Stavěl
    Input Text                          css=#form-widgets-IProducentAdministrators-administrators-0-widgets-email   stavel.jan@gmail.com
    Input Text                          css=#form-widgets-IProducentAdministrators-administrators-0-widgets-home_page   www.nkp.cz

    Input Text                          css=#form-widgets-IProducentAdministrators-administrators-0-widgets-location   Pašovice
    Input Text                          css=#form-widgets-IProducentAdministrators-administrators-0-widgets-phone   773230772
    Input Text                          css=#form-widgets-IProducentAdministrators-administrators-0-widgets-street   Pašovice 71
    Input Text                          css=#form-widgets-IProducentAdministrators-administrators-0-widgets-city   Prakšice
    Input Text                          css=#form-widgets-IProducentAdministrators-administrators-0-widgets-country   Česká republika
    Input Text                          css=#form-widgets-IProducentAdministrators-administrators-0-widgets-username   ${USER_NAME}
    Input Text                          css=#form-widgets-IProducentAdministrators-administrators-0-widgets-password   ${USER_PASSWORD}
    Input Text                          css=#form-widgets-IProducentAdministrators-administrators-0-widgets-password_ctl   ${USER_PASSWORD}

Add one administrator with wrong passwords
    Click Button                        Přidat
    Input Text                          css=#form-widgets-IProducentAdministrators-administrators-0-widgets-fullname   Jan Stavěl
    Input Text                          css=#form-widgets-IProducentAdministrators-administrators-0-widgets-email   stavel.jan
    Input Text                          css=#form-widgets-IProducentAdministrators-administrators-0-widgets-home_page   www.nkp.cz

    Input Text                          css=#form-widgets-IProducentAdministrators-administrators-0-widgets-location   Pašovice
    Input Text                          css=#form-widgets-IProducentAdministrators-administrators-0-widgets-phone   773230772
    Input Text                          css=#form-widgets-IProducentAdministrators-administrators-0-widgets-street   Pašovice 71
    Input Text                          css=#form-widgets-IProducentAdministrators-administrators-0-widgets-city   Prakšice
    Input Text                          css=#form-widgets-IProducentAdministrators-administrators-0-widgets-country   Česká republika
    Input Text                          css=#form-widgets-IProducentAdministrators-administrators-0-widgets-username   ${USER_NAME}
    Input Text                          css=#form-widgets-IProducentAdministrators-administrators-0-widgets-password   ${USER_PASSWORD}
    Input Text                          css=#form-widgets-IProducentAdministrators-administrators-0-widgets-password_ctl   wrongpassword

Local role is available
    [arguments]   ${rolename}
    Click Link      Sdílení
    Page Should Contain   ${rolename}    

Sharing tab is available
    Page Should Contain Link    Sdílení

Registrace producenta
    Click link        Registrovat
    Page Should Contain   		Registrace producenta
    Page Should Contain Button   	Registrovat
    Fill inputs about producent
    Click Link				Adresa
    Fill inputs about address
    Click Link                          Obsah
    Add one administrator    
    Click Button			Registrovat

Group Should Be Assigned
    [arguments]   ${GROUPNAME}    
    Page Should Contain Element    xpath=//input[@value="${GROUPNAME}" and @name="delete:list"]

Local Role is Assigned
    [arguments]   ${rolename}
    Page Should Contain Element    xpath=//input[@name='entries.role_${ROLENAME}:records' and @checked='checked']    

Fill inputs about ePublication
    Input Text				css=#form-widgets-nazev     Lesní školky ve Zlíně
    Input Text				css=#form-widgets-podnazev  Alternativní vzdělávání
    #Page Should Not Contain Element     css=div.fieldErrorBox
    #Input Text				css=#form-widgets-vazba     časopis
    Input Text                          css=#form-widgets-cena      0
    
Add authors for ePublication
    Click Element                       form.widgets.IAuthors.authors.buttons.add
    Input Text                          css=#form-widgets-IAuthors-authors-0-widgets-first_name  Jan
    Input Text                          css=#form-widgets-IAuthors-authors-0-widgets-last_name   Stavěl

Add Original Files for ePublication
    Click Element                       form.widgets.IOriginalFiles.originalFiles.buttons.add
    Input Text                          css=#form-widgets-IOriginalFiles-originalFiles-0-widgets-url  http://www.grada.cz/book/1000
    Input Text                          css=#form-widgets-IOriginalFiles-originalFiles-0-widgets-isbn  80-12312-3241-324124
    Choose File                         css=#form-widgets-IOriginalFiles-originalFiles-0-widgets-file-input  /opt/edeposit/docs/tests/resources/inzlin-01-2013-s-nasi-Tabinkou.pdf


Fill inputs about RIV
    Select Checkbox                     css=#form-widgets-offer_to_riv-0    
    Select From List By Label           css=#form-widgets-category_for_riv           1. společenské, humanitní a umělecké vědy (SHVa)

RIV category should be selected
    Page Should Contain                 1. společenské, humanitní a umělecké vědy (SHVa)