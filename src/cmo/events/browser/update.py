# -*- coding: utf-8 -*-

from cmo.events import _
from datetime import datetime
from plone import api
from plone.supermodel import model
from requests.exceptions import ConnectionError
from requests.exceptions import HTTPError
from z3c.form import button
from z3c.form import field
from z3c.form import form
from zope import schema

import datetime
import logging
import mysql.connector
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


class IMyForm(model.Schema):

    year = schema.Choice(
        title=_(u'Year'),
        values=[u'2015', u'2016', u'2017', u'2018', u'2019'],
        required=False,
    )


class UpdateWorkshopsForm(form.Form):
    """Update workshops list."""

    fields = field.Fields(IMyForm)
    ignoreContext = True

    label = _(u'Workshops Administration')

    @button.buttonAndHandler(_(u'Update Workshops'))
    def handle_update_workshops(self, action):
        """Update workshops list from Birds API
        """
        logger.info('Updating Workshops')
        data, errors = self.extractData()
        year = data['year']
        birs_uri = api.portal.get_registry_record('cmo.birs_api_uri')
        url = '/'.join([birs_uri, 'event_data_for_year', year])
        try:
            req = requests.get(url, headers=headers)
            req.raise_for_status()
        except (ConnectionError, HTTPError) as err:
            api.portal.show_message(err, self.request, type=u'error')
        else:
            self.update_workshops(year, req.json())
            api.portal.show_message(_(u'Updated!'), self.request, type=u'info')
        logger.info('Done.')

    @button.buttonAndHandler(_(u'Update Workshops from DB'))
    def handle_update_workshops_db(self, action):
        """Update workshops list from CIMAT db
        """
        logger.info('Updating Workshops')
        data, errors = self.extractData()
        year = data['year']

        config = {
            'user': 'user',
            'password': 'some_password',
            'host': '192.168.33.1',
            'database': 'databasename'
        }

        try:
            cnx = mysql.connector.connect(**config)
        except mysql.connector.Error as err:
            api.portal.show_message(err, self.request, type=u'error')
        else:
            cursor = cnx.cursor()
            query = ("SELECT codigo, nombre FROM eventos WHERE fechaIni BETWEEN %s AND %s")
            event_start = datetime.date(int(year), 1, 1)
            event_end = datetime.date(int(year), 12, 31)
            cursor.execute(query, (event_start, event_end))
            # self.update_workshops(year, json_data)
            for (codigo, nombre) in cursor:
                print("{}, {}".format(codigo, nombre))
            api.portal.show_message(_(u'Updated!'), self.request, type=u'info')
            cursor.close()
            cnx.close()
        logger.info('Done.')

    def update_workshops(self, year, json_data):
        """Update workshops for year
        """
        folder = api.content.get(path='/{0}'.format(year))
        if not folder:
            folder = api.content.create(
                type='Folder',
                title=year,
                container=api.portal.get())
        for item in json_data:
            if item['code'] not in folder:
                item['start_date'] = datetime.strptime(item['start_date'], '%Y-%m-%d')  # noqa
                item['end_date'] = datetime.strptime(item['end_date'], '%Y-%m-%d')  # noqa
                item['max_participants'] = int(item['max_participants'])
                api.content.create(
                    type='Workshop',
                    id=item['code'],
                    title=item['name'],
                    container=folder,
                    **item)


class UpdateParticipantsForm(form.Form):
    """Update Participants from Birs DB."""

    @button.buttonAndHandler(_(u'Update participants'))
    def handle_update_participants(self, action):
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
                api.content.create(
                    type='Participant',
                    id=kargs['email'],
                    title=kargs['firstname'],
                    container=self.context,
                    **kargs)
