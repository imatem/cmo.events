# -*- coding: utf-8 -*-

from zope.interface import provider
# from Products.CMFCore.utils import getToolByName
# from zope.component.hooks import getSite
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary


@provider(IVocabularyFactory)
def CertificatesTemplates(context):

    templates = []

    for item in ['Latex Template', ]:
        templates.append(SimpleVocabulary.createTerm(
            item.replace(' ', '-').lower(), item.replace(' ', '-').lower(), item))

    return SimpleVocabulary(templates)
