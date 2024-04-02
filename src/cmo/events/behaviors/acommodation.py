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
class IAcommodation(model.Schema):
    """Behavior Information about the person
    """

    model.fieldset(
        'acommodationInformation',
        label=_(
            u'label_cmo_acommodationInformation',
            u'Acommodation'
        ),
        fields=[
            'hotel',
            'visa',
            'externalHotel',
            'nameGuest',
        ]
    )

    hotel = schema.Choice(
        title=_(
            u'label_cmo_hotel',
            default=u'Hotel'
        ),
        vocabulary='cmo.events.vocabularies.hotels',
        required=False,
    )

    visa = schema.TextLine(
        title=_(
            u'label_cmo_visa',
            default=u'Visa'
        ),
        required=False,
    )
    externalHotel = schema.TextLine(
        title=_(
            u'label_cmo_externalHotel',
            default=u'External Hotel'
        ),
        required=False,
    )
    nameGuest = schema.TextLine(
        title=_(
            u'label_cmo_nameGuest',
            default=u'Name Guest'
        ),
        required=False,
    )


@implementer(IAcommodation)
@adapter(IDexterityContent)
class Acommodation(object):

    def __init__(self, context):
        self.context = context
