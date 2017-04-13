# -*- coding: utf-8 -*-
from cmo.events import _
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
from plone.supermodel import model
from zope import schema
from zope.component import adapter
from zope.interface import implementer
from zope.interface import provider


@provider(IFormFieldProvider)
class IMembership(model.Schema):
    """Behavior Information about the person
    """

    model.fieldset(
        'membershipInformation',
        label=_(
            u'label_cmo_membershipInformation',
            u'Membership'
        ),
        fields=[
            'arrival',
            'departure',
            'attendance',
            'role',
            'replied',
            'hasguest',
            'specialInfo',
            'offsite',
            'eventNotes',
        ]
    )

    arrival = schema.TextLine(
        title=_(
            u'label_cmo_arrival',
            default=u'Arrival Date'
        ),
        required=False,
    )

    departure = schema.TextLine(
        title=_(
            u'label_cmo_departure',
            default=u'Departure'
        ),
        required=False,
    )
    attendance = schema.TextLine(
        title=_(
            u'label_cmo_attendance',
            default=u'Attendance'
        ),
        required=False,
    )
    role = schema.TextLine(
        title=_(
            u'label_cmo_role',
            default=u'Role'
        ),
        required=False,
    )
    replied = schema.TextLine(
        title=_(
            u'label_cmo_replied',
            default=u'Replied At'
        ),
        required=False,
    )

    hasguest = schema.TextLine(
        title=_(
            u'label_cmo_hasguest',
            default=u'Has Guest'
        ),
        required=False,
    )

    specialInfo = schema.TextLine(
        title=_(
            u'label_cmo_specialInfo',
            default=u'Special Info'
        ),
        required=False,
    )

    offsite = schema.TextLine(
        title=_(
            u'label_cmo_offsite',
            default=u'Offsite'
        ),
        required=False,
    )

    eventNotes = schema.TextLine(
        title=_(
            u'label_cmo_eventNotes',
            default=u'Event Notes'
        ),
        required=False,
    )


@implementer(IMembership)
@adapter(IDexterityContent)
class Membership(object):

    def __init__(self, context):
        self.context = context
