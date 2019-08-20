# -*- coding: utf-8 -*-
from cmo.events import _
from datetime import datetime
from operator import itemgetter
from plone import api
from plone.autoform.view import WidgetsView
from plone.dexterity.interfaces import IDexterityFTI
from plone.dexterity.utils import getAdditionalSchemata
from plone.i18n.normalizer import idnormalizer
from requests.exceptions import ConnectionError
from requests.exceptions import HTTPError
from zope.component import getUtility

import logging
import requests


logger = logging.getLogger('Plone')

COLUMN_ORDER = [
    u'label_cmo_workshop',
    u'label_cmo_firstname',
    u'label_cmo_lastname',
    u'label_cmo_affiliation',
    u'label_cmo_year',
    u'label_cmo_attendance',
    u'label_cmo_email',
    u'label_cmo_role',
    u'label_cmo_hotel',
    u'label_cmo_externalHotel',  # OJO
    u'label_cmo_arrival',
    u'label_cmo_departure',
    u'label_cmo_hasguest',
    u'label_cmo_nameGuest',   # OJO
    u'label_cmo_specialInfo',
    u'label_cmo_gender',
    u'label_cmo_country',
    u'label_cmo_status',
    u'label_cmo_grade',
    u'label_cmo_phone',
    u'label_cmo_webpage',
    u'label_cmo_replied',
    u'label_cmo_offsite',
    u'label_cmo_eventNotes',
    u'label_cmo_visa',
    u'label_cmo_certificatesended',
    u'label_cmo_certificaterequested',
    u'label_cmo_birs_person_id',
    u'label_cmo_emergency_contact',
    u'label_cmo_emergency_phone',
    u'label_cmo_department',
    u'label_cmo_birs_title',
    u'label_cmo_address1',
    u'label_cmo_address2',
    u'label_cmo_address3',
    u'label_cmo_city',
    u'label_cmo_region',
    u'label_cmo_postal_code',
    u'label_cmo_biography',
    u'label_cmo_research_areas',
    u'label_cmo_updated_by',
    u'label_cmo_updated_at',
    u'label_cmo_grant_id',
    u'label_cmo_birs_membership_id',
    u'label_cmo_event_id',
    u'label_cmo_person_id',
    u'label_cmo_share_email',
    u'label_cmo_membership_updated_by',
    u'label_cmo_membership_updated_at',
    u'label_cmo_guest_disclaimer',
    u'label_cmo_billing',
    u'label_cmo_reviewed',
    u'label_cmo_room',
    u'label_cmo_invited_by',
    u'label_cmo_invited_on',
    u'label_cmo_share_email_hotel',
    u'label_cmo_room_notes',
]


class WorkshopView(WidgetsView):
    """This class is the same in plone.dexterity.browser.view.DefaultView
    The default view for Dexterity content. This uses a WidgetsView and
    renders all widgets in display mode.
    """

    @property
    def schema(self):
        fti = getUtility(IDexterityFTI, name=self.context.portal_type)
        return fti.lookupSchema()

    @property
    def additionalSchemata(self):
        return getAdditionalSchemata(context=self.context)

    def urltocertificates(self):
        return self.context.absolute_url() + '/certificates'

    def __call__(self):
        # utility function to add resource to rendered page
        # add_resource_on_request(self.request, 'tablecmo')
        if self.request.form:
            self.handle_update_participants()

        return super(WorkshopView, self).__call__()

    def participants(self, attendance=[]):
        allvaluesitems = self.context.values()

        items = []
        # attendance
        for itemv in allvaluesitems:
            if itemv.portal_type == 'Participant':
                if attendance:
                    if itemv.attendance in attendance:
                        items.append(itemv)
                else:
                    items.append(itemv)

        participants = {
            'headers': [],
            'rows': []
        }
        if not items:
            return participants
        exclude_names = (
            'IBasic.title',
            'IBasic.description',
            'description',
            'title'
            # 'IMembership.certificatesended',
            # 'IMembership.certificaterequested',
        )
        headers = []
        obj = items[0]
        viewitem = obj.unrestrictedTraverse('view')
        viewitem.update()

        default_widgets = viewitem.widgets.values()

        for widget in default_widgets:
            if widget.__name__ not in exclude_names:
                headers.append(widget.label)

        groups = viewitem.groups
        for group in groups:
            widgetsg = group.widgets.values()
            for widget in widgetsg:
                headers.append(widget.label)

        participants['headers'] = headers

        for item in items:
            row = [item.UID()]
            row.append(item.absolute_url())
            # row = []

            obj = item
            viewitem = obj.unrestrictedTraverse('view')
            viewitem.update()

            default_widgets = viewitem.widgets.values()
            groups = viewitem.groups

            for widget in default_widgets:
                if widget.__name__ not in exclude_names:
                    # row.append(getattr(item, widget.__name__, None))
                    row.append(widget.value)

            for group in groups:
                widgetsg = group.widgets.values()
                for widget in widgetsg:
                    if widget.__name__ in['IAcommodation.hotel', 'IMembership.certificatesended', 'IMembership.certificaterequested']:
                        row.append(','.join(widget.value))
                    # row.append(getattr(item, widget.name, None))
                    # elif widget.__name__ not in exclude_names:
                        # row.append(widget.value)
                    else:
                        row.append(widget.value)

            participants['rows'].append(row)
        return participants

    def positionlabelfield(self, labelfield):
        if labelfield not in COLUMN_ORDER:
            return -1
        return COLUMN_ORDER.index(labelfield)

    def participantsWithcolumnOrder(self, attendance=[]):

        participants = self.participants(attendance)
        orderparticipants = {
            'headers': [],
            'rows': []
        }

        try:
            headers = participants['headers']
            for j in range(0, len(headers)):
                orderparticipants['headers'].append('')

            for header in headers:
                orderparticipants['headers'][self.positionlabelfield(header)] = header

            rows = participants['rows']
            for row in rows:
                orderrow = []
                for j in range(0, len(row)):
                    orderrow.append('')

                orderrow[0] = row[0]  # this column is the UID
                orderrow[1] = row[1]  # this column is the url
                k = 2
                for header in headers:
                    position = self.positionlabelfield(header)
                    orderrow[position + 2] = row[k]
                    k += 1
                orderparticipants['rows'].append(orderrow)

        except Exception:
            return participants

        hotels = {
            u'Los Laureles': 1,
            u'Angel Inn': 2,
            u'Sin Hotel': 3,

        }
        aux_applications = [
            (
                app,
                hotels.get(app[10], 4),
                idnormalizer.normalize(app[7]),
                idnormalizer.normalize(app[3]),
                idnormalizer.normalize(app[4])
            ) for app in orderparticipants['rows']
        ]
        aux_sorted = sorted(aux_applications, key=itemgetter(1, 2, 3, 4))
        orows = [i[0] for i in aux_sorted]
        orderparticipants['rows'] = orows
        return orderparticipants

    def handle_update_participants(self):
        """Update participants list from Birs API
        """
        logger.info('Updating participants for {0}'.format(self.context.id))
        birs_uri = api.portal.get_registry_record('cmo.birs_api_uri')
        email_autho = api.portal.get_registry_record('cmo.birs_api_user')
        passwd_autho = api.portal.get_registry_record('cmo.birs_api_password')


        try:
            token = requests.post(
                birs_uri + '/api/login.json',
                headers={
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                },
                json={'api_user': {'email': email_autho, 'password': passwd_autho}},
            )

            jwt = 'Bearer ' + token.json()['jwt']
            workshop_number = self.context.id


            birs_url_event = '%s/events/%s/memberships.json' % (birs_uri, workshop_number)
            req = requests.get(
                birs_url_event,
                headers={'Accept': 'application/json', 'Authorization': jwt})
            req.raise_for_status()
        except (ConnectionError, HTTPError) as err:
            api.portal.show_message(err, self.request, type=u'error')
        else:

            self.update_participants(req.json())
            api.portal.show_message(_(u'Updated!'), self.request, type=u'info')
        logger.info('Done.')

    def update_participants(self, json_data):

        newparticipants = []

        for attendance, participants in json_data.iteritems():
            for participant in participants:
                userid = idnormalizer.normalize(participant['person']['email'])
                if userid not in self.context:
                    kargs = dict(participant['person'])

                    kargs['birs_person_id'] = participant['person']['id']
                    kargs['birs_title'] = participant['person']['title']
                    kargs['person_updated_by'] = participant['person']['updated_by']
                    kargs['person_updated_at'] = participant['person']['updated_at']
                    kargs.update(participant['membership'])
                    kargs['workshop'] = self.context.id
                    kargs['birs_membership_id'] = participant['membership']['id']
                    kargs['event_notes'] = participant['membership']['staff_notes']
                    kargs['membership_updated_by'] = participant['membership']['updated_by']
                    kargs['membership_updated_at'] = participant['membership']['updated_at']
                    kargs['off_site'] = participant['membership']['own_accommodation']

                    for d in ['arrival_date', 'replied_at', 'departure_date', 'person_updated_by', 'person_updated_at', 'membership_updated_by', 'membership_updated_at']:
                        if kargs[d] is not None and kargs[d] != '0000-00-00 00:00:00':
                            try:
                                kargs[d] = datetime.strptime(kargs[d], '%Y-%m-%d %H:%M:%S')  # noqa
                            except Exception:
                                del kargs[d]
                        else:
                            del kargs[d]

                    # we define own title
                    del kargs['title']
                    del kargs['id']

                    api.content.create(
                        type='Participant',
                        id=idnormalizer.normalize(kargs['email']),
                        title=' '.join([kargs['firstname'], kargs['lastname']]),
                        container=self.context,
                        **kargs)
                    newparticipants.append(' '.join([kargs['firstname'], kargs['lastname']]))
                else:
                    obj = self.context[userid]
                    obj.title = ' '.join(
                        [participant['person']['firstname'], participant['person']['lastname']])
                    obj.lastname = participant['person']['lastname']
                    obj.firstname = participant['person']['firstname']
                    obj.country = participant['person']['country']
                    obj.affiliation = participant['person']['affiliation']
                    obj.phd_year = participant['person']['phd_year']
                    obj.academic_status = participant['person']['academic_status']
                    obj.attendance = participant['membership']['attendance']
                    # obj.replied_at = participant['membership']['replied_at']
                    obj.special_info = participant['membership']['special_info']
                    obj.event_notes = participant['membership']['staff_notes']
                    obj.reindexObject()
        if newparticipants:
            msg = _(u'New participants: ') + ', '.join(newparticipants)
            api.portal.show_message(msg, self.request, type=u'info')
