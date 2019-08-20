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
            'birs_membership_id',
            'event_id',
            'person_id',
            'arrival_date',
            'departure_date',
            'role',
            'attendance',
            'share_email',
            'event_notes',
            'membership_updated_by',
            'membership_updated_at',
            'off_site',
            'has_guest',
            'guest_disclaimer',
            'special_info',
            'billing',
            'reviewed',
            'room',
            'invited_by',
            'invited_on',
            'share_email_hotel',
            'room_notes',
            'replied_at',
            'certificatesended',
            'certificaterequested',
        ]
    )

    # id
    birs_membership_id = schema.TextLine(
        title=_(
            u'label_cmo_birs_membership_id',
            default=u'Birs Membership Id'
        ),
        required=False,
    )

    event_id = schema.TextLine(
        title=_(
            u'label_cmo_event_id',
            default=u'Event Id'
        ),
        required=False,
    )

    person_id = schema.TextLine(
        title=_(
            u'label_cmo_person_id',
            default=u'Person Id'
        ),
        required=False,
    )

    arrival_date = schema.TextLine(
        title=_(
            u'label_cmo_arrival',
            default=u'Arrival Date'
        ),
        required=False,
    )

    departure_date = schema.TextLine(
        title=_(
            u'label_cmo_departure',
            default=u'Departure'
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

    attendance = schema.TextLine(
        title=_(
            u'label_cmo_attendance',
            default=u'Attendance'
        ),
        required=False,
    )

    share_email = schema.TextLine(
        title=_(
            u'label_cmo_share_email',
            default=u'Share Email'
        ),
        required=False,
    )

    # This is staff_notes
    event_notes = schema.TextLine(
        title=_(
            u'label_cmo_eventNotes',
            default=u'Event Notes'
        ),
        required=False,
    )

    # updated_by
    membership_updated_by = schema.TextLine(
        title=_(
            u'label_cmo_membership_updated_by',
            default=u'Membership Updated by'
        ),
        required=False,
    )

    # updated_at
    membership_updated_at = schema.TextLine(
        title=_(
            u'label_cmo_membership_updated_at',
            default=u'Membership Updated at'
        ),
        required=False,
    )

    # own_accommodation
    off_site = schema.TextLine(
        title=_(
            u'label_cmo_offsite',
            default=u'Offsite'
        ),
        required=False,
    )

    has_guest = schema.TextLine(
        title=_(
            u'label_cmo_hasguest',
            default=u'Has Guest'
        ),
        required=False,
    )

    guest_disclaimer = schema.TextLine(
        title=_(
            u'label_cmo_guest_disclaimer',
            default=u'Guest Disclaimer'
        ),
        required=False,
    )

    special_info = schema.TextLine(
        title=_(
            u'label_cmo_specialInfo',
            default=u'Special Info'
        ),
        required=False,
    )

    billing = schema.TextLine(
        title=_(
            u'label_cmo_billing',
            default=u'Billing'
        ),
        required=False,
    )

    reviewed = schema.TextLine(
        title=_(
            u'label_cmo_reviewed',
            default=u'Reviewed'
        ),
        required=False,
    )

    room = schema.TextLine(
        title=_(
            u'label_cmo_room',
            default=u'Room'
        ),
        required=False,
    )

    invited_by = schema.TextLine(
        title=_(
            u'label_cmo_invited_by',
            default=u'Invited By'
        ),
        required=False,
    )

    invited_on = schema.TextLine(
        title=_(
            u'label_cmo_invited_on',
            default=u'Invited on'
        ),
        required=False,
    )

    share_email_hotel = schema.TextLine(
        title=_(
            u'label_cmo_share_email_hotel',
            default=u'Share Email Hotel'
        ),
        required=False,
    )

    room_notes = schema.TextLine(
        title=_(
            u'label_cmo_room_notes',
            default=u'Room Notes'
        ),
        required=False,
    )

    replied_at = schema.TextLine(
        title=_(
            u'label_cmo_replied',
            default=u'Replied At'
        ),
        required=False,
    )

    certificatesended = schema.Choice(
        title=_(
            u'label_cmo_certificatesended',
            default=u'Certificate Sended'
        ),
        values=[u'Yes', u'No'],
        required=True,
        default=u'No'
    )

    certificaterequested = schema.Choice(
        title=_(
            u'label_cmo_certificaterequested',
            default=u'Certificate Requested'
        ),
        values=[u'Yes', u'No'],
        required=True,
        default=u'No'
    )


@implementer(IMembership)
@adapter(IDexterityContent)
class Membership(object):

    def __init__(self, context):
        self.context = context
