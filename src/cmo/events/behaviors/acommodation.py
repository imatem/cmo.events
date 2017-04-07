# -*- coding: utf-8 -*-
from cmo.events import _
from plone.autoform.interfaces import IFormFieldProvider
# from plone.directives import form
from plone.autoform import directives
from plone.supermodel import model
from plone.supermodel.directives import fieldset
from zope import schema
from zope.interface import alsoProvides
from zope.interface import provider

@provider(IFormFieldProvider)
class IAcommodation(model.Schema):
    """Behavior Information about the person
    """

    hotel = schema.TextLine(
        title=_(
            u'label_cmo_hotel',
            default=u'Hotel'
        ),
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

    fieldset(
        'acommodationInformation',
        label=_(
            u'label_cmo_acommodationInformation',
            u'Acommodation'
        ),
        fields=[
            hotel,
            visa,
            externalHotel,
            nameGuest,
        ]
    )

# alsoProvides(IAcommodation, IFormFieldProvider)
