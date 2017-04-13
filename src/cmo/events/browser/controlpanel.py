# -*- coding: utf-8 -*-
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.z3cform import layout
from zope import schema
from zope.interface import Interface


class ICMOControlPanel(Interface):

    birs_api_uri = schema.URI(
        title=u'Birs API',
        required=False,
    )


class CMOControlPanelForm(RegistryEditForm):
    schema = ICMOControlPanel
    schema_prefix = 'cmo'
    label = u'CMO Settings'


CMOControlPanelView = layout.wrap_form(
    CMOControlPanelForm, ControlPanelFormWrapper)
