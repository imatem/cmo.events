# -*- coding: utf-8 -*-

from datetime import datetime
from plone import api
from requests.exceptions import ConnectionError
from requests.exceptions import HTTPError
from z3c.form import button
from z3c.form import form

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


class UpdateWorshopsForm(form.Form):
    """Update workshops from Birs DB."""

    @button.buttonAndHandler(u'Update Workshops')
    def handle_update_workshops(self, action):
        """Update workshops list
        """
        logger.info('Updating Workshops')
        year = str(2017)
        birs_uri = api.portal.get_registry_record('cmo.birs_api_uri')
        url = '/'.join([birs_uri, 'event_data_for_year', year])
        try:
            req = requests.get(url, headers=headers)
            req.raise_for_status()
        except (ConnectionError, HTTPError) as err:
            api.portal.show_message(err, self.request, type=u'error')
        else:
            self.update_workshops(year, req.json())
            api.portal.show_message(u'Updated!', self.request, type=u'info')
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

    @button.buttonAndHandler(u'Update participants')
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
            api.portal.show_message(u'Updated!', self.request, type=u'info')
        logger.info('Done.')

    def update_participants(self, json_data):
        """
        """
        for item in json_data:
            if item['Person']['email'] not in self.context:
                api.content.create(
                    type='Participant',
                    id=item['Person']['email'],
                    title=item['Person']['firstname'],
                    container=self.context)
