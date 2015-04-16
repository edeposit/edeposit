from five import grok
from zope.component import queryUtility

from zope import schema
from zope.schema.interfaces import IVocabularyFactory

from zope.schema.vocabulary import SimpleVocabulary
from plone.registry.interfaces import IRegistry
import unicodedata

class FileTypesVocabulary(object):
    grok.implements(IVocabularyFactory)

    def __call__(self, context):
        registry = queryUtility(IRegistry)
        terms = []
        if registry is not None:
            for item in registry.get('edeposit.content.fileTypes', ()):
                terms.append(SimpleVocabulary.createTerm(item, item.encode('utf-8'), item))
        return SimpleVocabulary(terms)
grok.global_utility(FileTypesVocabulary, name=u"edeposit.content.fileTypes")

class CurrenciesVocabulary(object):
    grok.implements(IVocabularyFactory)

    def __call__(self, context):
        registry = queryUtility(IRegistry)
        terms = []
        if registry is not None:
            for item in registry.get('edeposit.content.currencies', ()):
                token = unicodedata.normalize('NFKD', item).encode('ascii', 'ignore').lower()
                terms.append(SimpleVocabulary.createTerm(item, token, item))
        return SimpleVocabulary(terms)
grok.global_utility(CurrenciesVocabulary, name=u"edeposit.content.currencies")

class CategoriesForRIVVocabulary(object):
    grok.implements(IVocabularyFactory)

    def __call__(self, context):
        registry = queryUtility(IRegistry)
        terms = []
        if registry is not None:
            for item in registry.get('edeposit.content.categoriesForRIV', ()):
                token = unicodedata.normalize('NFKD', item).encode('ascii', 'ignore').lower()
                terms.append(SimpleVocabulary.createTerm(item, token, item))
        return SimpleVocabulary(terms)
grok.global_utility(CategoriesForRIVVocabulary, name=u"edeposit.content.categoriesForRIV")

class LibrariesAccessingVocabulary(object):
    grok.implements(IVocabularyFactory)

    def __call__(self, context):
        registry = queryUtility(IRegistry)
        terms = []
        if registry is not None:
            for item in registry.get('edeposit.content.librariesAccessingChoices', ()):
                token = unicodedata.normalize('NFKD', item).encode('ascii', 'ignore').lower()
                terms.append(SimpleVocabulary.createTerm(item, token, item))
        return SimpleVocabulary(terms)
grok.global_utility(LibrariesAccessingVocabulary, name=u"edeposit.content.librariesAccessingChoices")

