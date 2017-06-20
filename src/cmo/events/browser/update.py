# -*- coding: utf-8 -*-

from datetime import date
from datetime import datetime
from cmo.events import _
from plone import api
from plone.i18n.normalizer import idnormalizer
from plone.supermodel import model
from requests.exceptions import ConnectionError
from requests.exceptions import HTTPError
from z3c.form import button
from z3c.form import field
from z3c.form import form
from zope import schema

import logging
import mysql.connector
import requests

logger = logging.getLogger('Plone')

config = {
    'user': 'user',
    'password': 'some_password',
    'host': '192.168.33.1',
    'database': 'databasename'
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
        """Update workshops list from Birs API
        """
        logger.info('Updating Workshops')
        data, errors = self.extractData()
        year = data['year']
        birs_uri = api.portal.get_registry_record('cmo.birs_api_uri')
        if birs_uri is None:
            api.portal.show_message(_(u'CMO Settings: No Birs API defined!'), self.request, type=u'error')
            return
        url = '/'.join([birs_uri, 'event_data_for_year', year])
        try:
            req = requests.get(url)
            req.raise_for_status()
        except (ConnectionError, HTTPError) as err:
            api.portal.show_message(err, self.request, type=u'error')
        else:
            self.update_workshops(year, req.json())
            api.portal.show_message(_(u'Updated!'), self.request, type=u'info')
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
                workshop = api.content.create(
                    type='Workshop',
                    id=item['code'],
                    title=item['name'],
                    container=folder,
                    **item)
                template = api.content.get('/templates-for-certificates/latex-template')
                api.content.create(
                    type='Certificate',
                    id='Certificate',
                    title='Certificate',
                    container=workshop,
                    ctemplate=api.content.get_uuid(obj=template))

    @button.buttonAndHandler(_(u'Update Workshops from DB'))
    def handle_update_workshops_db(self, action):
        """Update workshops list from CIMAT db
        """
        logger.info('Updating Workshops')
        data, errors = self.extractData()
        year = data['year']
        try:
            cnx = mysql.connector.connect(**config)
        except mysql.connector.Error as err:
            api.portal.show_message(err, self.request, type=u'error')
        else:
            # A MySQLCursorDict cursor returns each row as a dictionary
            cursor = cnx.cursor(dictionary=True)
            query = ("SELECT * FROM eventos WHERE fechaIni BETWEEN %s AND %s ORDER BY fechaIni")
            event_start = date(int(year), 1, 1)
            event_end = date(int(year), 12, 31)
            cursor.execute(query, (event_start, event_end))
            json_data = [self.workshop_to_birs(row) for row in cursor]
            self.update_workshops(year, json_data)
            cursor.close()
            cnx.close()
            api.portal.show_message(_(u'Updated!'), self.request, type=u'info')
        logger.info('Done.')

    def workshop_to_birs(self, data):
        """Returns a workshop with birs api format
        """
        workshop = {
            'code': data['codigo'],
            'name': data['nombre'],
            'short_name': data['nombreCorto'],
            'start_date': str(data['fechaIni']),
            'end_date': str(data['fechaFin']),
            'event_type': data['tipoEvento'],
            'max_participants': data['maximoParticipante'],
            'description': data['descripcion'],
            # 'press_release': '<p></p>',
        }
        return workshop


class UpdateParticipantsForm(form.Form):
    """Update Participants lists."""

    @button.buttonAndHandler(_(u'Update Participants'))
    def handle_update_participants(self, action):
        """Update participants list from Birs API
        """
        logger.info('Updating participants for {0}'.format(self.context.id))
        birs_uri = api.portal.get_registry_record('cmo.birs_api_uri')
        if birs_uri is None:
            api.portal.show_message(_(u'CMO Settings: No Birs API defined!'), self.request, type=u'error')
            return
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
            item_id = idnormalizer.normalize(item['Person']['email'])
            if item_id not in self.context:
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
                    id=item_id,
                    title=kargs['firstname'],
                    container=self.context,
                    **kargs)

    @button.buttonAndHandler(_(u'Update Participants from DB'))
    def handle_update_participants_db(self, action):
        """Update participants list from CIMAT db
        """
        logger.info('Updating participants for {0}'.format(self.context.id))
        try:
            cnx = mysql.connector.connect(**config)
        except mysql.connector.Error as err:
            api.portal.show_message(err, self.request, type=u'error')
        else:
            # A MySQLCursorDict cursor returns each row as a dictionary
            cursor = cnx.cursor(dictionary=True)
            query = ("SELECT * FROM user WHERE evento = %s ORDER BY lastname")
            cursor.execute(query, (self.context.id,))
            json_data = [self.person_to_birs(row) for row in cursor]
            self.update_participants(json_data)
            cursor.close()
            cnx.close()
            api.portal.show_message(_(u'Updated!'), self.request, type=u'info')
        logger.info('Done.')

    def person_to_birs(self, data):
        """Returns a workshop with birs api format
        """
        person = {
            'Workshop': data['evento'],
            'Person': {
                'lastname': data['lastname'],
                'firstname': data['name'],
                'country': data['pais'],
                'email': data['email'],
                'gender': data['genero'],
                'affiliation': data['company'],
                'salutation': data['grado'],
                'url': data['pagina'],
                'phone': data['phone'],
                'phd_year': data['graduacion'] or None,
                'academic_status': data['status'],
            },
            'Membership': {
                'arrival_date': str(data['arrival_date']) or None,
                'departure_date': str(data['departure_date']) or None,
                'attendance': data['confirmed'],
                'role': data['rol'],
                'replied_at': None,
                'has_guest': data['acompanante'],
                'special_info': data['informacion'],
                'off_site': data['reserva'],
                # 'event_notes': None
            }
        }
        return person
