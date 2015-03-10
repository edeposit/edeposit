# -*- coding: utf-8 -*-
from five import grok
from edeposit.content.originalfile import IOriginalFile
from string import Template
from Products.Five.browser import BrowserView
from zope.i18n import translate
from plone import api

# class OriginalFileChangesDisplayForm(form.Form):
#     mode = 'display'
#     fields = field.Fields(IOriginalFile)
    
# formWrapper = wrap_form(OriginalFileChangesDisplayForm, 
#                         index=FiveViewPageTemplateFile("changes_notification_email.pt"))
#                         #index=FiveViewPageTemplateFile("aa.pt"))



class ChangesEmail(BrowserView):
    tmpl = Template(u"""
Dobrý den, 
informujeme Vás o změnách v ohlášené ePublikaci.
Změny provedl někdo z akvizice, nebo katalogizace.

$href

$title
podnázev: \t $podnazev
část: \t $cast
název části: \t $nazev_casti
nakladatel/vydavatel: \t $nakladatel_vydavatel

ISBN: \t $isbn
přidělené ISBN: \t $generated_isbn

zpracovatel záznamu: \t $zpracovatel_zaznamu
url: \t $url

ohlásil: \t $authorTitle
stav: \t $state
Poslední změna: \t $lastModified


Kontakt

Pro následnou opravu údajů kontaktujte, prosím, akvizici na tel.: 221 663 369, pan Martin Žížala.

edeposit.nkp.cz
""")

    def __call__(self):
        obj = self.context
        creators = obj.listCreators()
        state = api.content.get_state(obj=obj)
        stateTitle = translate(obj.portal_workflow.getTitleForStateOnType(state, 
                                                                          obj.portal_type),
                               domain='plone', context = self.request)
        lastModified = obj.toLocalizedTime(obj.ModificationDate(),1)
        self.request.response.setHeader('Content-Type','text/plain')
        return self.tmpl.substitute(href=obj.absolute_url(),
                                    title = obj.getParentTitle(),
                                    podnazev = obj.getPodnazev(),
                                    cast = obj.getCast(),
                                    nazev_casti = obj.getNazevCasti(),
                                    nakladatel_vydavatel = obj.getNakladatelVydavatel(),
                                    isbn = obj.isbn or "",
                                    generated_isbn = obj.generated_isbn and 'Ano' or 'Ne',
                                    zpracovatel_zaznamu = obj.zpracovatel_zaznamu,
                                    url = obj.url or "",
                                    authorTitle = creators and creators[0],
                                    state =  stateTitle,
                                    lastModified = lastModified )
                                    
