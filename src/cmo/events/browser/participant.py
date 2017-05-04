# -*- coding: utf-8 -*-
from plone.dexterity.browser.edit import DefaultEditForm
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getUtility
from plone.registry.interfaces import IRegistry


class ParticipantEditView(DefaultEditForm):
    # template = ViewPageTemplateFile('templates/participant_edit.pt')


    def nextURL(self):
        # import pdb; pdb.set_trace()
        # view_url = self.context.absolute_url()
        view_url = self.context.aq_parent.absolute_url()
        portal_type = getattr(self, 'portal_type', None)
        if portal_type is not None:
            registry = getUtility(IRegistry)
            use_view_action = registry.get(
                'plone.types_use_view_action_in_listings', [])
            if portal_type in use_view_action:
                view_url = view_url + '/view'


        return view_url