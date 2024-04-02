# -*- coding: utf-8 -*-

from zope.interface import provider
# from Products.CMFCore.utils import getToolByName
from zope.component.hooks import getSite
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary


@provider(IVocabularyFactory)
def CertificatesTemplates(context):
    """Get all certificates templates in home site"""

    templates = []
    alltemplates = []

    folder_templates = [item for item in getSite().values() if item.id == 'templates-for-certificates' and item.portal_type == 'Folder']
    if folder_templates:
        alltemplates = folder_templates[0].values()

    for template in alltemplates:
        templates.append(SimpleVocabulary.createTerm(
            template.UID(), template.id, template.title))
    return SimpleVocabulary(templates)


@provider(IVocabularyFactory)
def hotels(context):
    values=[u'Los Laureles', u'Angel Inn', u'Suites Xadani', u'Sin Hotel', 'Self-funded']
    try:
        if context.hotel != u'Suites Xadani':
            values.remove(u'Suites Xadani')
    except:
        pass
    return SimpleVocabulary.fromItems([[i, i] for i in values])
