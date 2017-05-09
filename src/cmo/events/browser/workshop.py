# -*- coding: utf-8 -*-
from cmo.events import _
from datetime import datetime
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
headers = {
    'Host': 'www.birs.ca',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:52.0) Gecko/20100101 Firefox/52.0',  # noqa
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',  # noqa
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Authorization': 'Basic Ymlyc3dzOkcwcjFsbDRfU2wxcHAzcno=',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
}


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

    def __call__(self):
        # utility function to add resource to rendered page
        # add_resource_on_request(self.request, 'tablecmo')
        # import pdb; pdb.set_trace()
        if self.request.form:
            self.handle_update_participants()

        return super(WorkshopView, self).__call__()

    def participants(self):

        items = self.context.values()

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
            row = [item.absolute_url()]
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
                    if widget.__name__ == 'IAcommodation.hotel':
                        row.append(','.join(widget.value))
                    # row.append(getattr(item, widget.name, None))
                    else:
                        row.append(widget.value)

            participants['rows'].append(row)
        return participants

    def participantsWithcolumnOrder(self):

        participants = self.participants()
        orderparticipants = {
            'headers': [],
            'rows': []
        }

        # order = {
        #     u'label_cmo_workshop': 0,  # 0
        #     u'label_cmo_firstname': 1,  # 1
        #     u'label_cmo_lastname': 2,  # 2
        #     u'label_cmo_affiliation': 3,  # 6
        #     u'label_cmo_year': 4,  # 10
        #     u'label_cmo_email': 5,  # 3
        #     u'label_cmo_role': 6,  # 15
        #     u'label_cmo_hotel': 7,  # 21
        #     u'label_cmo_externalHotel': 8,  # 23
        #     u'label_cmo_arrival': 9,  # 12
        #     u'label_cmo_departure': 10,  # 13
        #     u'label_cmo_hasguest': 11,  # 17
        #     u'label_cmo_nameGuest': 12,  # 24
        #     u'label_cmo_specialInfo': 13,  # 18
        #     u'label_cmo_gender': 14,  # 5
        #     u'label_cmo_country': 15,  # 4
        #     u'label_cmo_status': 16,  # 11
        #     u'label_cmo_attendance': 17,  # 14
        #     u'label_cmo_grade': 18,  # 7
        #     u'label_cmo_phone': 19,  # 9
        #     u'label_cmo_webpage': 20,  # 8
        #     u'label_cmo_replied': 21,  # 16
        #     u'label_cmo_offsite': 22,  # 19
        #     u'label_cmo_eventNotes': 23,  # 20
        #     u'label_cmo_visa': 24,  # 22
        # }

        try:
            headers = participants['headers']
            orderparticipants['headers'].append(headers[0])
            orderparticipants['headers'].append(headers[1])
            orderparticipants['headers'].append(headers[2])
            orderparticipants['headers'].append(headers[6])
            orderparticipants['headers'].append(headers[10])
            orderparticipants['headers'].append(headers[3])
            orderparticipants['headers'].append(headers[15])
            orderparticipants['headers'].append(headers[21])
            orderparticipants['headers'].append(headers[23])
            orderparticipants['headers'].append(headers[12])
            orderparticipants['headers'].append(headers[13])
            orderparticipants['headers'].append(headers[17])
            orderparticipants['headers'].append(headers[24])
            orderparticipants['headers'].append(headers[18])
            orderparticipants['headers'].append(headers[5])
            orderparticipants['headers'].append(headers[4])
            orderparticipants['headers'].append(headers[11])
            orderparticipants['headers'].append(headers[14])
            orderparticipants['headers'].append(headers[7])
            orderparticipants['headers'].append(headers[9])
            orderparticipants['headers'].append(headers[8])
            orderparticipants['headers'].append(headers[16])
            orderparticipants['headers'].append(headers[19])
            orderparticipants['headers'].append(headers[20])
            orderparticipants['headers'].append(headers[22])

            rows = participants['rows']

            for row in rows:
                orderrow = []
                orderrow.append(row[0])  # this column is the url
                orderrow.append(row[1])
                orderrow.append(row[2])
                orderrow.append(row[3])
                orderrow.append(row[7])
                orderrow.append(row[11])
                orderrow.append(row[4])
                orderrow.append(row[16])
                orderrow.append(row[22])
                orderrow.append(row[24])
                orderrow.append(row[13])
                orderrow.append(row[14])
                orderrow.append(row[18])
                orderrow.append(row[25])
                orderrow.append(row[19])
                orderrow.append(row[6])
                orderrow.append(row[5])
                orderrow.append(row[12])
                orderrow.append(row[15])
                orderrow.append(row[8])
                orderrow.append(row[10])
                orderrow.append(row[9])
                orderrow.append(row[17])
                orderrow.append(row[20])
                orderrow.append(row[21])
                orderrow.append(row[23])
                orderparticipants['rows'].append(orderrow)

        except Exception:
            return participants

        return orderparticipants


    def handle_update_participants(self):
        """Update participants list
        """
        logger.info('Updating participants for {0}'.format(self.context.id))
        birs_uri = api.portal.get_registry_record('cmo.birs_api_uri')
        url = '/'.join([birs_uri, 'members', self.context.id])
        try:
            req = requests.get(url, headers=headers)
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
            if item['Person']['email'] not in self.context:
                kargs = dict(item['Person'])
                kargs.update(item['Membership'])
                kargs['workshop'] = item['Workshop']
                for d in ['arrival_date', 'replied_at', 'departure_date']:
                    if kargs[d] is not None:
                        kargs[d] = datetime.strptime(kargs[d], '%Y-%m-%d %H:%M:%S')  # noqa
                    else:
                        del kargs[d]

                id = idnormalizer.normalize(kargs['email'])
                api.content.create(
                    type='Participant',
                    id=id,
                    title=kargs['firstname'],
                    container=self.context,
                    **kargs)
