# -*- coding: utf-8 -*-
from cmo.events import valid_token
from plone import api
from plone.autoform.view import WidgetsView
from plone.dexterity.browser.edit import DefaultEditForm
from plone.dexterity.events import EditFinishedEvent
from plone.dexterity.i18n import MessageFactory as _
from plone.dexterity.interfaces import IDexterityFTI
from plone.dexterity.utils import getAdditionalSchemata
from plone.registry.interfaces import IRegistry
from Products.statusmessages.interfaces import IStatusMessage
from requests.exceptions import ConnectionError
from requests.exceptions import HTTPError
from z3c.form import button
from zope.component import getUtility
from zope.event import notify

import logging
import requests
import time


logger = logging.getLogger('Plone')


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

        # api user test password

    @button.buttonAndHandler(_(u'Save'), name='save')
    def handleApply(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        self.applyChanges(data)
        IStatusMessage(self.request).addStatusMessage(
            self.success_message, "info"
        )
        self.request.response.redirect(self.nextURL())

        birs_uri = api.portal.get_registry_record('cmo.birs_api_uri')
        email_autho = api.portal.get_registry_record('cmo.birs_api_user')
        passwd_autho = api.portal.get_registry_record('cmo.birs_api_password')

        try:
            token = requests.post(
                birs_uri + '/api/login.json',
                headers={
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                },
                json={'api_user': {'email': email_autho, 'password': passwd_autho}},
            )

            jwt = 'Bearer ' + token.json()['jwt']
            workshop_number = self.context.aq_parent.id

            birs_url_membership = '%s/events/%s/memberships/%s.json' % (birs_uri, workshop_number, data['IMembership.birs_membership_id'])

            req = requests.patch(
                birs_url_membership,
                headers={'Accept': 'application/json', 'Content-Type': 'application/json', 'Authorization': jwt},
                json={
                    'membership': {
                        'staff_notes': data['IMembership.event_notes'],
                        'person_attributes': {
                            'title': data['IPerson.birs_title']
                        }
                    }
                },
            )
            req.raise_for_status()
        except (ConnectionError, HTTPError) as err:
            api.portal.show_message(err, self.request, type=u'error')
        # else:

            # self.update_participants(req.json())

        notify(EditFinishedEvent(self.context))


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
