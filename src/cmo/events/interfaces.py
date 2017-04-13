# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from cmo.events import _
from zope import schema
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class ICmoEventsLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IEvent(Interface):

    title = schema.TextLine(
        title=_(u'Title'),
        required=True,
    )

    description = schema.Text(
        title=_(u'Description'),
        required=False,
    )


class IParticipant(Interface):
    """An application form for renewal scholarship.
    """
    # form.mode(title='hidden')
    title = schema.TextLine(
        title=_(u'Title'),
        required=False,
        # default=u'solicitud-20171'
    )

    workshop = schema.TextLine(
        title=_(u'label_cmo_workshop', u'Workshop'),
        required=False,
    )


class IWorkshop(Interface):
    """Workshop
    """
    # form.mode(title='hidden')
    title = schema.TextLine(
        title=_(u'Title'),
        required=False,
    )

    workshopid = schema.TextLine(
        title=_(u'label_cmo_workshopid', u'Workshop ID'),
        required=False,
    )

    workshopstart = schema.TextLine(
        title=_(u'label_cmo_workshopstart', u'Workshop Start Date'),
        required=False,
    )

    workshopend = schema.TextLine(
        title=_(u'label_cmo_workshopend', u'Workshop End Date'),
        required=False,
    )

