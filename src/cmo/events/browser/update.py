# -*- coding: utf-8 -*-

from cmo.events import _
from datetime import date
from datetime import datetime
from plone import api
from plone.i18n.normalizer import idnormalizer
from plone.supermodel import model
from requests.exceptions import ConnectionError
from requests.exceptions import HTTPError
from z3c.form import button
from z3c.form import field
from z3c.form import form
from zope import schema

# from zope.component import getMultiAdapter
import logging
import requests
import string


try:
    import mysql.connector
except Exception as e:
    MYSQL = False

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
        """Update workshops list from NEW Birs API
        """
        logger.info('Updating Workshops')
        data, errors = self.extractData()
        year = data['year']

        birs_uri = api.portal.get_registry_record('cmo.birs_api_uri')
        email_autho = api.portal.get_registry_record('cmo.birs_api_user')
        passwd_autho = api.portal.get_registry_record('cmo.birs_api_password')

        if birs_uri is None:
            api.portal.show_message(_(u'CMO Settings: No Birs API defined!'), self.request, type=u'error')
            return

        url = '%s/events/year/%s/location/EO.json' % (birs_uri, year)

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
            req = requests.get(
                url,
                headers={'Accept': 'application/json', 'Authorization': jwt})
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
                # item['max_participants'] = int(item['max_participants'])
                item['max_participants'] = int(item.get('max_participants', '0'))
                workshop = api.content.create(
                    type='Workshop',
                    id=item['code'],
                    title=item['name'],
                    container=folder,
                    **item)

                # create certificate
                template = api.content.get('/templates-for-certificates/latex-template')
                api.content.create(
                    type='Certificate',
                    id='Certificate',
                    title='Certificate',
                    container=workshop,
                    ctemplate=api.content.get_uuid(obj=template))


    # @button.buttonAndHandler(_(u'Update Workshops from DB'))
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
            query = ('SELECT * FROM eventos WHERE fechaIni BETWEEN %s AND %s ORDER BY fechaIni')
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
                    if kargs[d] is not None and kargs[d] != '0000-00-00 00:00:00':
                        kargs[d] = datetime.strptime(kargs[d], '%Y-%m-%d %H:%M:%S')  # noqa
                    else:
                        del kargs[d]
                api.content.create(
                    type='Participant',
                    id=item_id,
                    title=' '.join([kargs['firstname'], kargs['lastname']]),
                    container=self.context,
                    **kargs)

    # @button.buttonAndHandler(_(u'Update Participants from DB'))
    def handle_update_participants_db(self, action):
        """Update participants list from CIMAT db
        """
        logger.info('Updating participants for {0}'.format(self.context.id))
        try:
            cnx = mysql.connector.connect(**config)
            # cnx.set_charset_collation('utf-8')
        except mysql.connector.Error as err:
            api.portal.show_message(err, self.request, type=u'error')
        else:
            # A MySQLCursorDict cursor returns each row as a dictionary
            cursor = cnx.cursor(dictionary=True)
            query = ('SELECT * FROM user WHERE evento = %s ORDER BY lastname')
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
        try:
            lastname = data['lastname'].encode('iso-8859-1').decode('utf-8')
        except UnicodeEncodeError:
            lastname = data['lastname'].encode('cp1252').decode('utf-8')

        try:
            firstname = data['name'].encode('iso-8859-1').decode('utf-8')
        except UnicodeEncodeError:
            firstname = data['name'].encode('cp1252').decode('utf-8')

        try:
            affiliation = data['company'].encode('iso-8859-1').decode('utf-8')
        except UnicodeEncodeError:
            affiliation = data['company'].encode('cp1252').decode('utf-8')

        try:
            special_info = data['informacion'].encode('iso-8859-1').decode('utf-8')
        except UnicodeEncodeError:
            special_info = data['informacion'].encode('cp1252').decode('utf-8')

        person = {
            'Workshop': data['evento'],
            'Person': {
                'lastname': lastname,
                'firstname': firstname,
                'country': data['pais'],
                'email': data['email'],
                'gender': data['genero'],
                'affiliation': affiliation,
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
                'special_info': special_info or data['requerimientos'],
                'off_site': data['reserva'],
                # 'event_notes': None
                'visa': data['visa'],
                'nameGuest': data['acompaname'],
                'hotel': string.capwords(data['hotel']) or None,
            }
        }
        return person
