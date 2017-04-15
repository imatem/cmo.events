# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""
from cmo.events import _
from zope import schema
from zope.interface import Interface
from zope.interface import Invalid
from zope.interface import invariant
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


class StartBeforeEnd(Invalid):
    __doc__ = _('error_invalid_date',
                default=u'Invalid start or end date')


class IWorkshop(Interface):
    """Workshop
    """

    code = schema.TextLine(
        title=_(u'label_cmo_workshop_code', u'Workshop ID'),
        required=False,
    )

    # form.mode(title='hidden')
    title = schema.TextLine(
        title=_(u'label_cmo_workshop_name', u'Workshop Name'),
        required=False,
    )

    short_name = schema.TextLine(
        title=_(u'Shorname'),
        required=False,
    )

    start_date = schema.Date(
        title=_(u'label_cmo_workshop_start_date', u'Workshop Start Date'),
        required=False,
    )

    end_date = schema.Date(
        title=_(u'label_cmo_workshop_end_date', u'Workshop End Date'),
        required=False,
    )

    event_type = schema.TextLine(
        title=_(u'label_cmo_workshop_type', u'Workshop Type'),
        required=False,
    )
    max_participants = schema.Int(
        title=_(
            u'label_cmo_workshop_max_participants',
            u'Maximum Number of Participants'
        ),
        required=False,
    )

    description = schema.Text(
        title=_(u'label_cmo_workshop_description', u'Workshop Description'),
        required=False,
    )

    press_release = schema.TextLine(
        title=_(u'label_cmo_workshop_press_release', u'Press Release'),
        required=False,
    )

    @invariant
    def validate_start_end(data):
        if (
            data.start_date
            and data.end_date
            and data.start_date > data.end_date
        ):
            raise StartBeforeEnd(
                _('error_end_must_be_after_start_date',
                  default=u'End date must be after start date.')
            )
