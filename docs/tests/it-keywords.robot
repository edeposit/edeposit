*** Keywords ***
Input text and validate
    [Documentation]  Locate input element by ${locator} and enter the given
    ...              ${text}. Validate that the text has been entered.
    [Arguments]  ${locator}  ${text}
    Focus  ${locator}
    Input text  ${locator}  ${text}
    ${value} =  Get value  ${locator}
    Should be equal  ${text}  ${value}

Input text for sure
    [Documentation]  Locate input element by ${locator} and enter the given
    ...              ${text}. Validate that the text has been entered.
    ...              Retry until the set Selenium timeout. (The purpose of
    ...              this keyword is to fix random input issues on slow test
    ...              machines.)
    [Arguments]  ${locator}  ${text}
    ${TIMEOUT} =  Get Selenium timeout
    ${IMPLICIT_WAIT} =  Get Selenium implicit wait
    Wait until keyword succeeds  ${TIMEOUT}  ${IMPLICIT_WAIT}
    ...                          Input text and validate  ${locator}  ${text}

Log in
    [Documentation]  Log in to the site as ${userid} using ${password}. There
    ...              is no guarantee of where in the site you are once this is
    ...              done. (You are responsible for knowing where you are and
    ...              where you want to be)
    [Arguments]  ${userid}  ${password}
    Go to  ${PLONE_URL}/login_form
    Page should contain element  __ac_name
    Page should contain element  __ac_password
    Page should contain element  css=#login-form .formControls input[name=submit]
    Input text for sure  __ac_name  ${userid}
    Input text for sure  __ac_password  ${password}
    Click Button  css=#login-form .formControls input[name=submit]

Log In as Admin
    Log in    admin    ${ADMIN_PASSWORD}

Log out
    Go to  ${PLONE_URL}/logout
    Page Should Contain Element  css=#login-form

Pause
    Pause Execution


Declare test amqp queue
        