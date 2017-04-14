# -*- coding: utf-8 -*-

from plone import api
from unidecode import unidecode
from z3c.form import button
from z3c.form import form

import json
import logging
import requests

logger = logging.getLogger('Plone')


class UpdateWorshopsForm(form.Form):
    """Update workshops from Birs."""

    @button.buttonAndHandler(u'Update Workshops')
    def handle_update_workshops(self, action):
        """
        """
        logger.info("Updating Workshops")
        # event_data_for_year/2017
        # members/17w5060
        year = str(2017)
        birs_uri = api.portal.get_registry_record('cmo.birs_api_uri')
        url = '/'.join([birs_uri, 'event_data_for_year', year])
        headers = {
            'Host': 'www.birs.ca',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:52.0) Gecko/20100101 Firefox/52.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Authorization': 'Basic Ymlyc3dzOkcwcjFsbDRfU2wxcHAzcno=',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
        }
        req = requests.get(url, headers=headers)
        logger.info(url)
        logger.info(req.status_code)
        logger.info("Done.")
