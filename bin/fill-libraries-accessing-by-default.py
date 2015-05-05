
#./bin/instance80 -Oedeposit run fill-libraries-accessing-by-default.py
from AccessControl.SecurityManagement import newSecurityManager
from edeposit.content.epublication import librariesAccessingChoices
default_value = librariesAccessingChoices[0][0]

def main(app):
    # Use Zope application server user database (not plone site)
    newSecurityManager(None, app.acl_users.getUserById("admin"))

    edeposit = app['edeposit']
    pcat = edeposit.portal_catalog
    epubs = pcat(portal_type="edeposit.content.epublication", sort_on="created")

    for epub in epubs:
        obj = epub.getObject()
        print " | ".join([epub.id, epub.Title, str(epub.created)])
        print "... ", obj.libraries_accessing
        if obj.libraries_accessing is None:
            print "... nastavuji default hodnotu"
            obj.libraries_accessing = default_value

    import transaction; transaction.commit()
    print "hotovo"

if 'app' in locals():
    main(app)
