# -*- coding: utf-8 -*-
from plone.autoform.view import WidgetsView
from plone.dexterity.browser.edit import DefaultEditForm
from plone.dexterity.interfaces import IDexterityFTI
from plone.dexterity.utils import getAdditionalSchemata
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class ParticipantEditView(DefaultEditForm):
    # template = ViewPageTemplateFile('templates/participant_edit.pt')

    def nextURL(self):
        view_url = self.context.aq_parent.absolute_url()
        portal_type = getattr(self, 'portal_type', None)
        if portal_type is not None:
            registry = getUtility(IRegistry)
            use_view_action = registry.get(
                'plone.types_use_view_action_in_listings', [])
            if portal_type in use_view_action:
                view_url = view_url + '/view'
        return view_url


class ParticipantView(WidgetsView):
    """This class is the same in plone.dexterity.browser.view.DefaultView
    The default view for Dexterity content. This uses a WidgetsView and
    renders all widgets in display mode.
    """

    @property
    def schema(self):
        fti = getUtility(IDexterityFTI, name=self.context.portal_type)
        return fti.lookupSchema()

    @property
    def additionalSchemata(self):
        return getAdditionalSchemata(context=self.context)
