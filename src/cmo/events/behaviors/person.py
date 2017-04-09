# -*- coding: utf-8 -*-
from cmo.events import _
# from plone.autoform.interfaces import IFormFieldProvider
# # from plone.directives import form
# # from plone.autoform import directives
# from plone.supermodel import model
# from zope import schema
# # from zope.interface import alsoProvides
# from plone.supermodel.directives import fieldset
from plone.supermodel import model
# from plone.dexterity.interfaces import IDexterityContent
# from zope.interface import provider

# from plone.app.contenttypes import _
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
# from plone.namedfile import field as namedfile
# from plone.supermodel import model
from zope import schema
from zope.component import adapter
from zope.interface import implementer
from zope.interface import provider


@provider(IFormFieldProvider)
class IPerson(model.Schema):
    """Behavior Information about the person
    """

    model.fieldset(
        'personInformation',
        label=_(
            u'label_cmo_personinformation',
            u'Person'
        ),
        # description=_(
        #     u'',
        #     u''
        # ),
        fields=[
            'firstname',
            'lastname',
            'email',
            'country',
            'affiliation',
            'grade',
            'home',
            'phone',
            'year',
            'status',
        ]
    )

    firstname = schema.TextLine(
        title=_(
            u'label_cmo_firstname',
            default=u'Firstname'
        ),
        required=True,
    )

    lastname = schema.TextLine(
        title=_(
            u'label_cmo_lastname',
            default=u'LastName'
        ),
        required=True,
    )
    email = schema.TextLine(
        title=_(
            u'label_cmo_email',
            default=u'Email'
        ),
        required=True,
    )
    country = schema.TextLine(
        title=_(
            u'label_cmo_country',
            default=u'Country'
        ),
        required=False,
    )
    affiliation = schema.TextLine(
        title=_(
            u'label_cmo_affiliation',
            default=u'Affiliation'
        ),
        required=False,
    )

    grade = schema.TextLine(
        title=_(
            u'label_cmo_grade',
            default=u'Grade'
        ),
        required=False,
    )

    home = schema.TextLine(
        title=_(
            u'label_cmo_home',
            default=u'Home'
        ),
        required=False,
    )

    phone = schema.TextLine(
        title=_(
            u'label_cmo_phone',
            default=u'Phone'
        ),
        required=False,
    )

    year = schema.TextLine(
        title=_(
            u'label_cmo_year',
            default=u'Graduation year'
        ),
        required=False,
    )

    status = schema.TextLine(
        title=_(
            u'label_cmo_status',
            default=u'Status'
        ),
        required=False,
    )

@implementer(IPerson)
@adapter(IDexterityContent)
class Person(object):

    def __init__(self, context):
        self.context = context
