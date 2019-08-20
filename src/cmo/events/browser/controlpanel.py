# -*- coding: utf-8 -*-
from cmo.events import _
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.z3cform import layout
from zope import schema
from zope.interface import Interface


class ICMOControlPanel(Interface):

    birs_api_uri = schema.URI(
        title=_(
            u'label_birs_api_url',
            default=u'BIRS whorkshops API url'),
        description=_(
            u'help_birs_api_url',
            default=u'e.g. https://staging.birs.ca'),
        default=None,
        required=True,
    )

    birs_api_user = schema.TextLine(
        title=_(
            u'label_birs_api_user',
            default=u'BIRS whorkshops API user'),
        description=_(
            u'help_birs_api_user',
            default=u'Username for authentication '
                    u'to the BIRS whorkshops API'),
        default=None,
        required=False,
    )

    birs_api_password = schema.Password(
        title=_(
            u'label_birs_api_pass',
            default=u'BIRS API password'),
        description=_(
            u'help_birs_api_pass',
            default=u'The password for the BIRS whorkshops API '
                    u'user account.'),
        default=None,
        required=False)

    birs_location = schema.TextLine(
        title=_(
            u'label_birs_location',
            default=u'BIRS events location'),
        description=_(
            u'help_birs_location',
            default=u'This is CMO for production server. '
                    u'For stagging server use EO'),
        default=u'CMO',
        required=True,
    )


class CMOControlPanelForm(RegistryEditForm):
    schema = ICMOControlPanel
    schema_prefix = 'cmo'
    label = u'CMO Settings'


CMOControlPanelView = layout.wrap_form(
    CMOControlPanelForm, ControlPanelFormWrapper)
