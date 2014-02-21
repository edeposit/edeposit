from five import grok
from zope.component import queryUtility

from zope import schema
from zope.schema.interfaces import IVocabularyFactory

from zope.schema.vocabulary import SimpleVocabulary
from plone.registry.interfaces import IRegistry

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
                terms.append(SimpleVocabulary.createTerm(item, item.encode('utf-8'), item))
        return SimpleVocabulary(terms)
grok.global_utility(CurrenciesVocabulary, name=u"edeposit.content.currencies")

class CategoriesForRIVVocabulary(object):
    grok.implements(IVocabularyFactory)

    def __call__(self, context):
        registry = queryUtility(IRegistry)
        terms = []
        if registry is not None:
            for item in registry.get('edeposit.content.categoriesForRIV', ()):
                terms.append(SimpleVocabulary.createTerm(item, item.encode('utf-8'), item))
        return SimpleVocabulary(terms)
grok.global_utility(CategoriesForRIVVocabulary, name=u"edeposit.content.categoriesForRIV")
