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
from collections import OrderedDict

import logging
import requests

logger = logging.getLogger('Plone')


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
        orderfields = OrderedDict()
        # orderfields[u'label_cmo_workshop'] = 0
        # orderfields[u'label_cmo_firstname'] = 1
        # orderfields[u'label_cmo_lastname'] = 2
        # orderfields[u'label_cmo_affiliation'] = 3
        # orderfields[u'label_cmo_year'] = 4
        # orderfields[u'label_cmo_attendance'] = 5
        # orderfields[u'label_cmo_email'] = 6
        # orderfields[u'label_cmo_role'] = 7
        # orderfields[u'label_cmo_hotel'] = 8
        # orderfields[u'label_cmo_externalHotel'] = 9
        # orderfields[u'label_cmo_arrival'] = 10
        # orderfields[u'label_cmo_departure'] = 11
        # orderfields[u'label_cmo_hasguest'] = 12
        # orderfields[u'label_cmo_nameGuest'] = 13
        # orderfields[u'label_cmo_specialInfo'] = 14
        # orderfields[u'label_cmo_gender'] = 15
        # orderfields[u'label_cmo_country'] = 16
        # orderfields[u'label_cmo_status'] = 17
        # orderfields[u'label_cmo_grade'] = 18
        # orderfields[u'label_cmo_phone'] = 19
        # orderfields[u'label_cmo_webpage'] = 20
        # orderfields[u'label_cmo_replied'] = 21
        # orderfields[u'label_cmo_offsite'] = 22
        # orderfields[u'label_cmo_eventNotes'] = 23
        # orderfields[u'label_cmo_visa'] = 24
        # orderfields[u'label_cmo_certificatesended'] = 25
        # orderfields[u'label_cmo_certificaterequested'] = 26

        orderfields[u'label_cmo_workshop'] = 0
        orderfields[u'label_cmo_firstname'] = 1
        orderfields[u'label_cmo_lastname'] = 2
        orderfields[u'label_cmo_email'] = 6
        orderfields[u'label_cmo_country'] = 16
        orderfields[u'label_cmo_gender'] = 15
        orderfields[u'label_cmo_affiliation'] = 3
        orderfields[u'label_cmo_grade'] = 18
        orderfields[u'label_cmo_webpage'] = 20
        orderfields[u'label_cmo_phone'] = 19
        orderfields[u'label_cmo_year'] = 4
        orderfields[u'label_cmo_status'] = 17
        orderfields[u'label_cmo_arrival'] = 10
        orderfields[u'label_cmo_departure'] = 11
        orderfields[u'label_cmo_attendance'] = 5
        orderfields[u'label_cmo_role'] = 7
        orderfields[u'label_cmo_replied'] = 21
        orderfields[u'label_cmo_hasguest'] = 12
        orderfields[u'label_cmo_specialInfo'] = 14
        orderfields[u'label_cmo_offsite'] = 22
        orderfields[u'label_cmo_eventNotes'] = 23
        orderfields[u'label_cmo_certificatesended'] = 25
        orderfields[u'label_cmo_certificaterequested'] = 26
        orderfields[u'label_cmo_hotel'] = 8
        orderfields[u'label_cmo_visa'] = 24
        orderfields[u'label_cmo_externalHotel'] = 9
        orderfields[u'label_cmo_nameGuest'] = 13
        return orderfields.get(labelfield, -1)






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
        url = '/'.join([birs_uri, 'members', self.context.id])
        try:
            req = requests.get(url)
            req.raise_for_status()
        except (ConnectionError, HTTPError) as err:
            api.portal.show_message(err, self.request, type=u'error')
        else:
            self.update_participants(req.json())
            api.portal.show_message(_(u'Updated!'), self.request, type=u'info')
        logger.info('Done.')

    def update_participants(self, json_data):
        """Update participants list
        """
        for item in json_data:
            userid = idnormalizer.normalize(item['Person']['email'])
            if userid not in self.context:
                kargs = dict(item['Person'])
                kargs.update(item['Membership'])
                kargs['workshop'] = item['Workshop']
                for d in ['arrival_date', 'replied_at', 'departure_date']:
                    if kargs[d] is not None and kargs[d] != '0000-00-00 00:00:00':
                        kargs[d] = datetime.strptime(kargs[d], '%Y-%m-%d %H:%M:%S')  # noqa
                    else:
                        del kargs[d]

                api.content.create(
                    type='Participant',
                    id=idnormalizer.normalize(kargs['email']),
                    title=kargs['firstname'],
                    container=self.context,
                    **kargs)
            else:
                participant = self.context[userid]
                participant.lastname = item['Person']['lastname']
                participant.firstname = item['Person']['firstname']
                participant.country = item['Person']['country']
                participant.affiliation = item['Person']['affiliation']
                participant.phd_year = item['Person']['phd_year']
                participant.academic_status = item['Person']['academic_status']
                participant.attendance = item['Membership']['attendance']
                participant.replied_at = item['Membership']['replied_at']
                participant.special_info = item['Membership']['special_info']
                participant.event_notes = item['Membership']['event_notes']
