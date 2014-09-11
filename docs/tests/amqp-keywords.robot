*** Keywords ***
Open Browser with RabbitMQ
    Open Browser      http://localhost:15672/#/queues
    Input Text        css=input[name="username"]    guest
    Input Text        css=input[name="password"]    guest
    Click Button      Login
    Select From List by Value    css=#show-vhost    aleph