*** VARIABLES ***

*** Keywords ***

Open browser and create all folders
    Open browser   ${PLONE_URL}   firefox
    Log in as site owner    
    Go To  ${PLONE_URL}/producents    
    Open Workflow Menu
    Click Element             link=Recreate All important Collections
    Wait Until Page Contains  Dokumenty čekající na přidělení ISBN
    Go To     ${PLONE_URL}/@@mail-controlpanel
    Input Text      css=input[id="form.email_from_name"]       E-Deposit
    Input Text      css=input[id="form.email_from_address"]    edeposit@nkp.cz
    Click Element   css=input[id="form.actions.save"]
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

Start Aleph Daemon
    Start Process      /home/jan/lib/edeposit/bin/python /home/jan/lib/edeposit/bin/edeposit_amqp_alephdaemon.py start    shell=yes
    ${output}=        Run   ps ax | grep alephdaemon
    Should Contain    ${output}   edeposit_amqp_alephdaemon.py

Stop Aleph Daemon
    Start Process      pkill -f alephdaemon     shell=yes

Start Aleph Daemon
    Start Process      /home/jan/lib/edeposit/bin/python /home/jan/lib/edeposit/bin/edeposit_amqp_antivirusd.py start    shell=yes
    ${output}=        Run   ps ax | grep antivirusd
    Should Contain    ${output}   edeposit_amqp_antivirusd.py

Stop Antivirus Daemon
    Start Process      pkill -f amqp_antivirusd     shell=yes

Create producents folder
    Add Dexterity Content     ${PLONE_URL}     edeposit-user-producentfolder    producents

User Should Exist
    [arguments]   ${username}
    Go to                   ${PLONE_URL}/@@user-information?userid=${username}
    Page Should Contain     Osobní informace

User Can Log In
    [arguments]   ${username}    ${password}
    Log In        ${username}   ${password}
    Page Should Contain         Přehledová stránka uživatele

Fill inputs about Prihlaseni
    [arguments]   ${username}=${USER_NAME}      ${password}=${USER_PASSWORD}    ${password_ctl}=${USER_PASSWORD}
    Input Text    css=#form-widgets-username   ${username}
    Input Text    css=#form-widgets-password   ${password}
    Input Text    css=#form-widgets-password_ctl   ${password_ctl}
    
Fill inputs about Osobni informace
    [arguments]   ${fullname}=Jan Stavěl   ${email}=stavel.jan@gmail.com   ${phone}=733230772
    Input Text    css=#form-widgets-fullname     ${fullname}
    Input Text    css=#form-widgets-email   ${email}
    Input Text    css=#form-widgets-phone   ${phone}
    
Fill inputs about Obsah
    [arguments]   ${title}    ${description}
    Input Text				css=#form-widgets-IBasic-title        ${title}
    Input Text				css=#form-widgets-IBasic-description  ${description}

Fill inputs about producent
    Input Text				css=#form-widgets-IBasic-title        ${PRODUCENT_TITLE}
    Input Text				css=#form-widgets-IBasic-description  Malý lokální vydavatel zajímavých publikací 
    Input Text				css=#form-widgets-home_page   http://www.e-deposit.cz
    Input Text				css=#form-widgets-location   Praha
    
Fill inputs about address
    Input Text				css=#form-widgets-street  Pašovice 71
    Input Text 				css=#form-widgets-city  Prakšice
    Input Text    			css=#form-widgets-country  Česká republika
    Input Text    			css=#form-widgets-psc     68756

Add one administrator    
    Input Text                          css=#form-widgets-IAdministrator-administrator-widgets-fullname   Jan Stavěl
    Input Text                          css=#form-widgets-IAdministrator-administrator-widgets-email   stavel.jan@gmail.com
    Input Text                          css=#form-widgets-IAdministrator-administrator-widgets-phone   773230772
    Input Text                          css=#form-widgets-IAdministrator-administrator-widgets-username   ${USER_NAME}
    Input Text                          css=#form-widgets-IAdministrator-administrator-widgets-password   ${USER_PASSWORD}
    Input Text                          css=#form-widgets-IAdministrator-administrator-widgets-password_ctl   ${USER_PASSWORD}

Add one editor
    Input Text                          css=#form-widgets-IEditor-fullname   Jan Stavěl
    Input Text                          css=#form-widgets-IEditor-email   stavel.jan@gmail.com
    Input Text                          css=#form-widgets-IEditor-phone   773230772
    Input Text                          css=#form-widgets-IEditor-username   ${EDITOR1_NAME}
    Input Text                          css=#form-widgets-IEditor-password   ${EDITOR1_PASSWORD}
    Input Text                          css=#form-widgets-IEditor-password_ctl   ${EDITOR1_PASSWORD}

Add one administrator with wrong passwords
    #Click Button                        Přidat
    Input Text                          css=#form-widgets-IAdministrator-administrator-widgets-fullname   Jan Stavěl
    Input Text                          css=#form-widgets-IAdministrator-administrator-widgets-email   stavel.jan@gmail.com
    Input Text                          css=#form-widgets-IAdministrator-administrator-widgets-phone   773230772
    Input Text                          css=#form-widgets-IAdministrator-administrator-widgets-username   ${USER_NAME}
    Input Text                          css=#form-widgets-IAdministrator-administrator-widgets-password   ${USER_PASSWORD}
    Input Text                          css=#form-widgets-IAdministrator-administrator-widgets-password_ctl   wrongpassword

Local role is available
    [arguments]   ${rolename}
    Click Link      Sdílení
    Page Should Contain   ${rolename}    

Sharing tab is available
    Page Should Contain Link    Sdílení

Sharing tab is not available
    Page Should Not Contain Link    Sdílení

User Can edit
    Page Should Contain Link    Úpravy

User Can Not Edit
    Page Should Not Contain Link    Úpravy

User Can Not Add Any Content
    Page Should Not Contain        Přidat novou položku

Registrace producenta
    Go To                  ${PLONE_URL}/producents/register-with-producent
    Page Should Contain   		Registrace producenta
    Page Should Contain                 Producent
    Page Should Contain                 Název producenta 
    Page Should Contain Button   	Registrovat
    Fill inputs about producent
    Click Link				Adresa
    Fill inputs about address
    Click Link                          Producent
    Add one administrator    
    Click Button			Registrovat
    Wait Until Page Contains            Vítejte!

Registrace producenta s editorem
    Click link        Registrovat
    Fill inputs about producent
    Click Link				Adresa
    Fill inputs about address
    Click Link                          Producent
    Add one administrator    
    Click Link                          Editor producenta
    Add one editor
    Click Button			Registrovat

Group Should Be Assigned
    [arguments]   ${GROUPNAME}    
    Page Should Contain Element    xpath=//input[@value="${GROUPNAME}" and @name="delete:list"]

Group Should Not Be Assigned
    [arguments]   ${GROUPNAME}    
    Page Should Not Contain Element    xpath=//input[@value="${GROUPNAME}" and @name="delete:list"]

Local Role is Assigned
    [arguments]   ${username}   ${rolename}
    Page Should Contain Element     xpath=//tr[.//input[@value='${username}']]//input[@name='entries.role_${ROLENAME}:records' and @checked='checked']    

Local Role is Not Assigned
    [arguments]   ${username}   ${rolename}
    Page Should Contain Element    xpath=//tr[.//input[@value='${username}']]//input[@name='entries.role_${ROLENAME}:records' and not(@checked)]

Fill inputs about ePublication
    [arguments]    ${title}=Lesní školky ve Zlíně   ${podnazev}=Individualni vzdělávání
    Input Text				css=#form-widgets-IBasic-title     ${title}
    Input Text				css=#form-widgets-podnazev     ${podnazev}
    Page Should Not Contain             Obsah
    Page Should Contain                 ePublikace
    Page Should Contain                 Název
    Input Text                          css=#form-widgets-cena      0

Fill inputs about Vydani
    Input Text                          css=#form-widgets-nakladatel_vydavatel        In Zlín
    Input Text                          css=#form-widgets-misto_vydani                Zlín
    Input Text                          css=#form-widgets-rok_vydani                  2013
    Input Text                          css=#form-widgets-poradi_vydani               první
    Input Text                          css=#form-widgets-zpracovatel_zaznamu         Jan Stavěl

Fill nakladatel
    [arguments]                         ${NAKLADATEL}
    Input Text                          css=#form-widgets-nakladatel_vydavatel        ${NAKLADATEL}

Fill cena
    [arguments]                         ${PRICE}
    Input Text                          css=#form-widgets-cena      ${PRICE}

Fill misto vydani
    [arguments]                         ${VALUE}
    Input Text                          css=#form-widgets-misto_vydani      ${VALUE}

Fill zpracovatel
    [arguments]                         ${VALUE}
    Input Text                          css=#form-widgets-zpracovatel_zaznamu      ${VALUE}

Fill poradi vydani
    [arguments]                         ${VALUE}
    Input Text                          css=#form-widgets-poradi_vydani      ${VALUE}

Fill rok vydani
    [arguments]                         ${YEAR}
    Input Text                          css=#form-widgets-rok_vydani     ${YEAR}

Add authors for ePublication
    [arguments]                         ${AUTHOR}
    Input Text                          css=#form-widgets-IAuthors-authors-0-widgets-fullname    ${AUTHOR}

Add Original Files for ePublication
    [Arguments]                         ${ISBN}    ${filename}=inzlin-01-2013-s-nasi-Tabinkou.pdf
    Input Text                          css=#form-widgets-IOriginalFile-url  http://www.grada.cz/book/1000
    Input Text                          css=#form-widgets-IOriginalFile-isbn  ${ISBN}
    Choose File                         css=#form-widgets-IOriginalFile-file-input  /opt/edeposit/docs/tests/resources/${filename}

Add Original Files for ePublication with ISBN generated
    [Arguments]                         ${filename}=inzlin-01-2013-s-nasi-Tabinkou.pdf
    Input Text                          css=#form-widgets-IOriginalFile-url  http://www.grada.cz/book/1000
    Choose File                         css=#form-widgets-IOriginalFile-file-input  /opt/edeposit/docs/tests/resources/${filename}
    Select Checkbox                     css=#form-widgets-IOriginalFile-generated_isbn-0

Fill inputs about RIV
    Select Checkbox                     css=#form-widgets-offer_to_riv-0
    Select From List By Label           css=#form-widgets-category_for_riv           1. společenské, humanitní a umělecké vědy (SHVa)

RIV category should be selected
    Page Should Contain                 společenské, humanitní a umělecké vědy (SHVa)

Ohlášení se soubory
    [arguments]   ${isbn}=${VALID_ISBN}
    Go To                                 ${PLONE_URL}/dashboard
    Click Link                            Ohlášení ePublikací
    Wait Until Page Contains Element      css=input[value="Ohlásit"]
    Fill inputs about ePublication    
    Add authors for ePublication          Jan Stavěl
    Add Original Files for ePublication   ${isbn}
    Fill inputs about Vydani
    Click Button                          form.buttons.save    


Ohlášení se soubory a anglickym ISBN
    Click Link                            Ohlášení ePublikací
    Wait Until Page Contains Element      css=input[value="Ohlásit"]
    Fill inputs about ePublication    
    Add authors for ePublication          Jan Stavěl
    Add Original Files for ePublication   ${VALID_ENGLISH_ISBN}
    Fill inputs about Vydani
    Click Button                          form.buttons.save    

Zobrazit historii
    Click link       Historie
    
Historie obsahuje zprávu
    [arguments]      ${message}
    Page Should Contain    ${message}

User can add ePublication
    Click Link         Ohlášení ePublikací
    Wait Until Page Contains   Ohlášení ePublikací
    Open add new menu
    Click Element          css=#edeposit-content-epublication
    Page Should Contain    Přidat E-Deposit - ePublikace

Go to user page
    Pause

Vytvoření RIV posuzovatele
    Log in as site owner
    Go To                             ${PLONE_URL}/@@usergroup-userprefs
    Click Overlay Button        Přidat nového uživatele
    Input Text       //input[@id='form.fullname']   Jan Stavel
    Input Text       //input[@id='form.username']   riv
    Input Text       //input[@id='form.email']      riv@nkp.cz
    Input Text       //input[@id='form.password']   afado3
    Input Text       //input[@id='form.password_ctl']   afado3
    Select Checkbox  //input[@id='form.groups.8']
    Click Button     Registrovat
    Log out


Vytvoření akvizitora
    Log in as site owner
    Go To                             ${PLONE_URL}/@@usergroup-userprefs
    Click Overlay Button        Přidat nového uživatele
    Input Text       //input[@id='form.fullname']   Jan Stavel
    Input Text       //input[@id='form.username']   ${AKVIZITOR_NAME}
    Input Text       //input[@id='form.email']      ${AKVIZITOR_NAME}@nkp.cz
    Input Text       //input[@id='form.password']   ${AKVIZITOR_PASSWORD}
    Input Text       //input[@id='form.password_ctl']   ${AKVIZITOR_PASSWORD}
    #Select Checkbox  //input[@id='form.groups.1']
    Select Checkbox  //input[@id='form.groups.2']
    Click Button     Registrovat
    Page Should Contain    Přehled uživatelů

Vytvoření administrátora katalogizace
    [arguments]   ${name}=${LIBRARY_ADMINISTRATOR}   ${password}=${LIBRARY_ADMINISTRATOR_PASSWORD}
    Log in as site owner
    Go To                             ${PLONE_URL}/@@usergroup-userprefs
    Click Overlay Button        Přidat nového uživatele
    Input Text       //input[@id='form.fullname']   Testovací správce knihovníků
    Input Text       //input[@id='form.username']   ${name}
    Input Text       //input[@id='form.email']      ${name}@nkp.cz
    Input Text       //input[@id='form.password']   ${password}
    Input Text       //input[@id='form.password_ctl']   ${password}
    Select Checkbox  //input[@id='form.groups.3']
    Click Button     Registrovat
    Page Should Contain    Přehled uživatelů

Vytvoření pracovníka katalogizace
    [arguments]   ${name}=${LIBRARIAN_USER}   ${password}=${LIBRARIAN_PASSWORD}
    Log in as site owner
    Go To                             ${PLONE_URL}/@@usergroup-userprefs
    Click Overlay Button        Přidat nového uživatele
    Input Text       //input[@id='form.fullname']   Testovací knihovník
    Input Text       //input[@id='form.username']   ${name}
    Input Text       //input[@id='form.email']      ${name}@nkp.cz
    Input Text       //input[@id='form.password']   ${password}
    Input Text       //input[@id='form.password_ctl']   ${password}
    Select Checkbox  //input[@id='form.groups.4']
    Click Button     Registrovat
    Page Should Contain    Přehled uživatelů

Vytvoření pracovníka ISBN Agentury
    [arguments]   ${name}=${ISBN_AGENCY_USER}   ${password}=${ISBN_AGENCY_PASSWORD}
    Log in as site owner
    Go To                             ${PLONE_URL}/@@usergroup-userprefs
    Click Overlay Button        Přidat nového uživatele
    Input Text       //input[@id='form.fullname']   Testovací pracovnik ISBN agentury
    Input Text       //input[@id='form.username']   ${name}
    Input Text       //input[@id='form.email']      ${name}@nkp.cz
    Input Text       //input[@id='form.password']   ${password}
    Input Text       //input[@id='form.password_ctl']   ${password}
    Select Checkbox  //input[@id='form.groups.5']
    Click Button     Registrovat
    Page Should Contain    Přehled uživatelů

Existuje portlet Prideleni ISBN
    Page Should Contain Element   xpath=//dt[contains(@class,"portletHeader")]//span[contains(text(),"Přidělování ISBN")]
    Page Should Contain Element   xpath=//dd[contains(@class,"portletItem")]//a[contains(@href,"/producents/content_status_comment?workflow_action=sendEmailToISBNAgency")]
    Page Should Contain Element   xpath=//dd[contains(@class,"portletItem")]//a[contains(@href,"/producents/originalfiles-for-isbn-agency")]
    Page Should Contain Element   xpath=//dd[contains(@class,"portletItem")]//a[contains(@href,"/producents/worklist-for-isbn-agency")]

Existuje portlet Prehled originalu pro prideleni ISBN
    # portlet Pridelovani isbn - prehled originalu
    Page Should Contain Element   xpath=//dl[contains(@class,"portletCollection")]//dt[contains(@class,"portletHeader")]//span[contains(text(),"Přidělení ISBN - přehled originálů")]

Existuje portlet Cekame na Aleph
    Page Should Contain Element   xpath=//dt[contains(@class,"portletHeader")]//span[contains(text(),"Čekáme na Aleph")]
    Page Should Contain Element   xpath=//dd[contains(@class,"portletItem")]//a[contains(@href,"/producents/content_status_comment?workflow_action=loadSysNumbersFromAleph") and contains(text(),"načíst z Alephu")]
    Page Should Contain Element   xpath=//dd[contains(@class,"portletItem")]//a[contains(@href,"/producents/originalfiles-waiting-for-aleph") and contains(text(),"přehled originálů")]
    Page Should Contain Element   xpath=//dd[contains(@class,"portletItem")]//a[contains(@href,"/producents/worklist-waiting-for-aleph") and contains(text(),"CSV s přehledem")]
    Page Should Contain Element   xpath=//dd[contains(@class,"portletItem")]//a[contains(@href,"/producents/content_status_comment?workflow_action=sendEmailWithOriginalFilesWaitingForAleph") and contains(text(),"odeslat email akvizitorům")]

Existuje portlet Originaly co cekaji na Aleph
    Page Should Contain Element   xpath=//dl[contains(@class,"portletCollection")]//dt[contains(@class,"portletHeader")]//span[contains(text(),"Originály co čekají na Aleph")]


Registrace pracovníků katalogizace
    Vytvoření administrátora katalogizace
    Log Out
    Vytvoření pracovníka katalogizace
    Vytvoření pracovníka katalogizace   ${LIBRARIAN_USER_01}
    Log Out

Nastaveni portletu pro skupinu Akvizitori
    Log in as site owner
    Go To                             ${PLONE_URL}/@@usergroup-userprefs
    Click Link                        Skupiny
    Go To                             ${PLONE_URL}/@@usergroup-groupmembership?groupname=Acquisitors
    Click Link                        Přehledová stránka skupiny
    Select From List                  //div[@id='dashboard-portlets1']//select    /++groupdashboard++plone.dashboard1+Acquisitors/+/portlets.Review

ISBNValidationResult is at RabbitMQ Test Queue
    ${MSG}=                          Get Message From Queue          ${QUEUE_NAME}
    Log Dictionary                   ${MSG}   WARN
    ${MSG_BODY}=                     Get From Dictionary   ${MSG}   body
    ${MSG_HEADERS}=                  Get From Dictionary   ${MSG}   headers
    Dictionary Should Contain Item   ${MSG_BODY}   __nt_name   ISBNValidationResult
    Dictionary Should Contain Item   ${MSG_BODY}   is_valid    True

CountResult is at RabbitMQ Test Queue    
    ${MSG}=                          Get Message From Queue          ${QUEUE_NAME}
    Log Dictionary                   ${MSG}   WARN
    ${MSG_BODY}=                     Get From Dictionary   ${MSG}   body
    ${MSG_HEADERS}=                  Get From Dictionary   ${MSG}   headers
    Dictionary Should Contain Item   ${MSG_BODY}   __nt_name   CountResult
    Dictionary Should Contain Item   ${MSG_BODY}   num_of_records    0
    
Open Browser with RabbitMQ
    Open Browser      http://localhost:15672/#/queues
    Input Text        css=input[name="username"]    guest
    Input Text        css=input[name="password"]    guest
    Click Button      Login
    Select From List by Value    css=#show-vhost    aleph

Open Browser with System User
    Open Browser      ${PLONE_URL}
    Log in                                ${SYSTEM_USER_NAME}   ${SYSTEM_USER_PASSWORD}

Open Browser with ISBN Agency User
    Open Browser      ${PLONE_URL}
    Log in                                ${ISBN_AGENCY_USER}   ${ISBN_AGENCY_PASSWORD}

Delete Test Queue
    Delete Queue     ${QUEUE_NAME}

Set Javascript Testing Mode
    Execute Javascript    jQuery().setTestingMode()

Unset Javascript Testing Mode
    Execute Javascript    jQuery().unsetTestingMode()

Fill Aleph Record
    Input Text				css=#form-widgets-IBasic-title     Aleph Record
    Input Text				css=#form-widgets-isbn             ${VALID_ISBN}
    Input Text				css=#form-widgets-rok_vydani       2013
    Input Text				css=#form-widgets-aleph_sys_number       129087
    Input Text				css=#form-widgets-aleph_library       NKC01


Choose an Aleph Record
    Wait Until Page Contains Element      css=a.contenttype-edeposit-content-alephrecord
    Click Element                         css=a.contenttype-edeposit-content-alephrecord
    Wait Until Page Contains Element      css=input.contentTreeAdd
    Execute Javascript                    jQuery('input.contentTreeAdd').click()

Fill Unique Username
    ${random}=       Generate Random String    4
    ${value}=        Catenate    SEPARATOR=-  username   ${TEST_SEED}    ${random}
    Input Text       css=#form-widgets-IAdministrator-administrator-widgets-username   ${value}

Choose a Producent Administrator
    ${content_type}=    Catenate   edeposit-user-producentadministrator    
    ${status} =  Run Keyword And Return Status  Click Link
    ...  css=#plone-contentmenu-factories a.contenttype-${content_type}
    Run keyword if  ${status} != True  Click Link  ${content_type}
    Wait Until Page Contains    Přidat

Choose a Producent Editor
    ${content_type}=    Catenate   edeposit-user-producenteditor
    ${status} =  Run Keyword And Return Status  Click Link
    ...  css=#plone-contentmenu-factories a.contenttype-${content_type}
    Run keyword if  ${status} != True  Click Link  ${content_type}
    Wait Until Page Contains    Přidat

System potvrdi ze
    [arguments]     ${state_label}
    Open Workflow Menu
    Click Element                     link=${state_label}

Submit Acquisition
    Open Workflow Menu
    Click Element                     link=Schválit

Vytvorit systemovou zpravu
    [arguments]      ${link}
    Open add new menu    
    Click Element                         link=${link}
    Input Text                            css=input[id="form-widgets-IBasic-title"]     systemova zprava
    Input Text                            css=input[id="form-widgets-isbn"]             isbn-fadsfjasd
    Click Button                          form.buttons.save  
    Page Should Contain                   Položka byla vytvořena

Systémové zprávy obsahují
    [arguments]   ${text}
    ${current_location}=       Get Location
    Click Link                 Systémové zprávy
    Wait Until Page Contains   ${text}    
    Go To                      ${current_location}

Queue is not empty
    [arguments]     ${vhost}    ${queue}
    ${num_of_messages}=    Get Num of Messages at Queue      ${vhost}    ${queue}
    # Log      ${vhost}     WARN
    # Log      ${queue}     WARN
    # Log      ${num_of_messages}     WARN
    Should not be equal as integers    ${num_of_messages}    0

Respond as ISBN Validation Daemon
    [arguments]       ${isbn}   ${is_valid}
    Log   Respond as ISBN Validation Daemon    WARN
    Wait Until Keyword Succeeds           10s   0.5s  Queue is not empty     aleph     ${QUEUE_NAME}
    Sleep   1s
    ${MSG}=                               Get Message From Queue      aleph    ${QUEUE_NAME}
    Write Msg Into File         ${MSG}    aleph-isbn-validation-request.json
    Simulate ISBN Validate Response       ${MSG}   ${isbn}   ${is_valid}


Respond as Aleph Count Daemon
    [arguments]       ${isbn}   ${num_of_records}
    Log   Respond as Aleph Count Daemon    WARN
    Wait Until Keyword Succeeds           10s   0.5s  Queue is not empty     aleph     ${QUEUE_NAME}
    Sleep   1s
    ${MSG}=                               Get Message From Queue      aleph    ${QUEUE_NAME}
    Write Msg Into File         ${MSG}    aleph-count-request.json
    Simulate ISBN Count Response          ${MSG}   ${isbn}   ${num_of_records}

Respond as Antivirus Daemon
    Log   Respond as Antivirus    WARN
    Wait Until Keyword Succeeds           10s   0.5s  Queue is not empty     antivirus     ${QUEUE_NAME}
    Sleep   1s
    ${MSG}=                               Get Message From Queue      antivirus    ${QUEUE_NAME}
    Write Msg Into File         ${MSG}    antivirus-request.json
    Simulate Antivirus Response           ${MSG}   ${FILENAME}

Respond as Calibre Daemon
    Log   Respond as Calibre Convert    WARN
    Wait Until Keyword Succeeds           10s   0.5s  Queue is not empty     calibre     ${QUEUE_NAME}
    Sleep   1s
    ${MSG}=                               Get Message From Queue      calibre    ${QUEUE_NAME}
    Write Msg Into File         ${MSG}    calibre-convert-request.json
    Simulate Calibre Response           ${MSG}

Respond as Aleph Export Daemon
    [arguments]       ${isbn}  
    Log   Respond as Aleph Export Daemon    WARN
    Wait Until Keyword Succeeds           10s   0.5s  Queue is not empty     aleph     ${QUEUE_NAME}
    Sleep   1s
    ${MSG}=                               Get Message From Queue      aleph    ${QUEUE_NAME}
    Write Msg Into File         ${MSG}    aleph-export-request.json
    Simulate Aleph Export Response          ${MSG}   ${isbn}

Respond as Aleph Export Daemon with Exception
    [arguments]       ${isbn}  
    Log   Respond as Aleph Export Daemon with Exception    WARN
    Wait Until Keyword Succeeds           5s   0.5s  Queue is not empty     aleph     ${QUEUE_NAME}
    Sleep   1s
    ${MSG}=                               Get Message From Queue      aleph    ${QUEUE_NAME}
    Write Msg Into File         ${MSG}    aleph-export-request.json
    Simulate Aleph Export Exception          ${MSG}

Insert Comment
    [arguments]   ${text}
    Wait Until Page Contains Element   css=#form-widgets-comment
    Input Text        css=#form-widgets-comment     ${text}    
    
Send Email to ISBN Agency
    [arguments]    ${browser_id}=2
    Switch Browser    ${browser_id}
    Go to    ${PLONE_URL}/producents
    Open Workflow Menu
    Click Element                           link=Send Email to ISBN Agency
    Insert Comment                          Email to isbn agency was sent
    Click Element     css=input[name="form.buttons.save"]
    Wait Until Page Contains    Stav položky změněn
    
Submit SysNumber Search at Aleph
    [arguments]    ${epublication_link}=${PLONE_URL}/producents/${PRODUCENT_ID}/epublications/lesni-skolky-ve-zline/inzlin-01-2013-s-nasi-tabinkou.pdf
    Open browser   ${PLONE_URL}   firefox
    Log in                                ${SYSTEM_USER_NAME}   ${SYSTEM_USER_PASSWORD}
    Go To                                 ${epublication_link}
    Open Workflow Menu
    Click Element                         link=Dohledat sysNumber v Alephu
    Page Should Contain                   Čekání na Aleph

Respond as Aleph Search Daemon
    [arguments]       ${isbn}  
    Log   Respond as Aleph Search Daemon    WARN
    Wait Until Keyword Succeeds           5s   0.5s  Queue is not empty     aleph     ${QUEUE_NAME}
    Sleep   1s
    ${MSG}=                               Get Message From Queue      aleph    ${QUEUE_NAME}
    Write Msg Into File         ${MSG}    aleph-sysnumber-search-request.json
    Simulate Aleph Search Response          ${MSG}   ${isbn}

Prepare AMQP Test Environment
    Delete All Test Queues Starting With    ${QUEUE_PREFIX}
    Declare Queue                    aleph  ${QUEUE_NAME}
    Declare Queue Binding            aleph  search     ${QUEUE_NAME}   request
    Declare Queue Binding            aleph  count      ${QUEUE_NAME}   request
    Declare Queue Binding            aleph  validate   ${QUEUE_NAME}   request
    Declare Queue Binding            aleph  export     ${QUEUE_NAME}   request

    # Remove Queue Binding            aleph  search     daemon   request
    # Remove Queue Binding            aleph  count      daemon   request
    # Remove Queue Binding            aleph  validate   daemon   request
    # Remove Queue Binding            aleph  export     daemon   request

    Declare Queue                    antivirus  ${QUEUE_NAME}
    Declare Queue Binding            antivirus  antivirus   ${QUEUE_NAME}  request
#    Remove Queue Binding             antivirus  antivirus   daemon  request
    
    Declare Queue                    calibre  ${QUEUE_NAME}
    Declare Queue Binding            calibre  convert   ${QUEUE_NAME}  request
#    Remove Queue Binding             calibre  convert   daemon  request

Rollback AMQP Test Environmnent
    Delete All Test Queues Starting With    ${QUEUE_PREFIX}
    Declare Queue Binding            aleph  search     daemon   request
    Declare Queue Binding            aleph  count      daemon   request
    Declare Queue Binding            aleph  validate   daemon   request
    Declare Queue Binding            aleph  export     daemon   request
    Declare Queue Binding            antivirus  antivirus   daemon  request
    Declare Queue Binding            calibre  convert   daemon  request

Send ePublication To Acquisition
    [arguments]      ${isbn}=${VALID_ISBN}    ${epublication_link}=${PLONE_URL}/producents/${PRODUCENT_ID}/epublications/lesni-skolky-ve-zline/inzlin-01-2013-s-nasi-tabinkou.pdf
    Respond as ISBN Validation Daemon     ${isbn}  True
    Respond as Aleph Count Daemon         ${isbn}  0
    Respond as Antivirus Daemon
    Respond as Aleph Export Daemon        ${isbn}
    Submit SysNumber Search at Aleph      ${epublication_link}
    Respond as Aleph Search Daemon        ${isbn}


ePublication contains Original File at state 
    [arguments]   ${state}
    Click Link    Zobrazení
    Page Should Contain Element   xpath=//a[contains(@class,"contenttype-edeposit-content-originalfile") and contains(@class,"state-${state}")]
