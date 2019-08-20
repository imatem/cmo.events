# -*- coding: utf-8 -*-
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.z3cform import layout
from zope import schema
from zope.interface import Interface


class ICMOControlPanel(Interface):

    birs_api_uri = schema.URI(
        title=u'Birs API url',
        required=True,
    )

    birs_api_user = schema.TextLine(
        title=u'Birs API user',
        required=False,
    )

    birs_api_password = schema.Password(
        title=u'Birs API password',
        required=False,
    )

    birs_location = schema.TextLine(
        title=u'Birs location',
        required=True,
    )


class CMOControlPanelForm(RegistryEditForm):
    schema = ICMOControlPanel
    schema_prefix = 'cmo'
    label = u'CMO Settings'


CMOControlPanelView = layout.wrap_form(
    CMOControlPanelForm, ControlPanelFormWrapper)
