# -*- coding: utf-8 -*-

from zope.interface import provider
# from Products.CMFCore.utils import getToolByName
# from zope.component.hooks import getSite
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary


@provider(IVocabularyFactory)
def ShowFields(context):

    active_terms = []

    for brain in ['Participant: Firstname', 'Participant: Lastname', 'Workshop: Title', ]:
        active_terms.append(SimpleVocabulary.createTerm(
            brain.replace(': ', '-'), brain.split(':')[1].strip(), brain))

    return SimpleVocabulary(active_terms)

@provider(IVocabularyFactory)
def CertificatesTemplates(context):

    templates = []

    for item in ['Latex Template', ]:
        templates.append(SimpleVocabulary.createTerm(
            item.replace(' ', '-').lower(), item.replace(' ', '-').lower(), item))

    return SimpleVocabulary(templates)
