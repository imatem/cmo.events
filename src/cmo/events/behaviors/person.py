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
            'birs_person_id',
            'lastname',
            'firstname',
            'salutation',
            'gender',
            'email',
            'url',
            'phone',
            'emergency_contact',
            'emergency_phone',
            'affiliation',
            'department',
            'birs_title',
            'address1',
            'address2',
            'address3',
            'city',
            'region',
            'country',
            'postal_code',
            'academic_status',
            'phd_year',
            'biography',
            'research_areas',
            'person_updated_by',
            'person_updated_at',
            'grant_id',
        ]
    )

    # id
    birs_person_id = schema.TextLine(
        title=_(
            u'label_cmo_birs_person_id',
            default=u'Birs Person Id'
        ),
        required=False,
    )

    lastname = schema.TextLine(
        title=_(
            u'label_cmo_lastname',
            default=u'LastName'
        ),
        required=True,
    )

    firstname = schema.TextLine(
        title=_(
            u'label_cmo_firstname',
            default=u'Firstname'
        ),
        required=True,
    )

    # change to saludation for web service
    salutation = schema.TextLine(
        title=_(
            u'label_cmo_grade',
            default=u'Grade'
        ),
        required=False,
    )

    gender = schema.TextLine(
        title=_(
            u'label_cmo_gender',
            default=u'Gender'
        ),
        required=False,
    )

    email = schema.TextLine(
        title=_(
            u'label_cmo_email',
            default=u'Email'
        ),
        required=True,
    )

    url = schema.TextLine(
        title=_(
            u'label_cmo_webpage',
            default=u'Web page'
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

    emergency_contact = schema.TextLine(
        title=_(
            u'label_cmo_emergency_contact',
            default=u'Emergency Contact'
        ),
        required=False,
    )

    emergency_phone = schema.TextLine(
        title=_(
            u'label_cmo_emergency_phone',
            default=u'Emergency Phone'
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

    department = schema.TextLine(
        title=_(
            u'label_cmo_department',
            default=u'Department'
        ),
        required=False,
    )

    # title
    birs_title = schema.TextLine(
        title=_(
            u'label_cmo_birs_title',
            default=u'Birs Title'
        ),
        required=False,
    )

    address1 = schema.TextLine(
        title=_(
            u'label_cmo_address1',
            default=u'Address 1'
        ),
        required=False,
    )

    address2 = schema.TextLine(
        title=_(
            u'label_cmo_address2',
            default=u'Address 2'
        ),
        required=False,
    )

    address3 = schema.TextLine(
        title=_(
            u'label_cmo_address3',
            default=u'Address 3'
        ),
        required=False,
    )

    city = schema.TextLine(
        title=_(
            u'label_cmo_city',
            default=u'City'
        ),
        required=False,
    )

    region = schema.TextLine(
        title=_(
            u'label_cmo_region',
            default=u'Region'
        ),
        required=False,
    )

    country = schema.TextLine(
        title=_(
            u'label_cmo_country',
            default=u'Country'
        ),
        required=False,
    )

    postal_code = schema.TextLine(
        title=_(
            u'label_cmo_postal_code',
            default=u'Postal Code'
        ),
        required=False,
    )

    academic_status = schema.TextLine(
        title=_(
            u'label_cmo_status',
            default=u'Academic Status'
        ),
        required=False,
    )

    phd_year = schema.TextLine(
        title=_(
            u'label_cmo_year',
            default=u'Graduation year'
        ),
        required=False,
    )

    biography = schema.TextLine(
        title=_(
            u'label_cmo_biography',
            default=u'Biography'
        ),
        required=False,
    )

    research_areas = schema.TextLine(
        title=_(
            u'label_cmo_research_areas',
            default=u'Research Areas'
        ),
        required=False,
    )

    # updated_by
    person_updated_by = schema.TextLine(
        title=_(
            u'label_cmo_updated_by',
            default=u'Updated by'
        ),
        required=False,
    )

    # updated_at
    person_updated_at = schema.TextLine(
        title=_(
            u'label_cmo_updated_at',
            default=u'Updated at'
        ),
        required=False,
    )

    grant_id = schema.TextLine(
        title=_(
            u'label_cmo_grant_id',
            default=u'Grant id'
        ),
        required=False,
    )


@implementer(IPerson)
@adapter(IDexterityContent)
class Person(object):

    def __init__(self, context):
        self.context = context
