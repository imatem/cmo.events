# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from zope.component import getUtility
from zope.component.hooks import getSite
from DateTime import DateTime
from zope.i18n import translate
from cmo.events import _
from zope.schema.interfaces import IVocabularyFactory
from plone import api


class SearchView(BrowserView):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def catalog(self):
        return getToolByName(getSite(), 'portal_catalog')

    def getYear(self):
        year = DateTime().year()
        if self.request.form:
            from_year = self.request.form.get('from', str(year))
            return eval(from_year)
        return year

    def getYears(self):
        year = DateTime().year() + 2
        return range(2010, year)

    def getDates(self):
        # format: 'dd-mm-yyyy'
        dates = {'from': '', 'to': ''}
        if self.request.form:
            from_date = self.request.form.get('from', '').replace('-', '/')
            to_date = self.request.form.get('to', '').replace('-', '/')
            dates['from'] = from_date
            dates['to'] = to_date
        return dates

    def workshops(self, from_date, to_date):

        query = {
            'portal_type': 'Workshop',
            'sort_on': 'workshop_start',
            'workshop_end': {'query': from_date, 'range': 'min'},
            'workshop_start': {'query': to_date, 'range': 'max'}
        }

        brains = self.catalog.searchResults(query)
        return brains

    def participants(self, dates):

        from_date = dates['from'] and dates['from'] or '01/01/1900'
        dt = DateTime().ISO().split('-')
        default_date = dt[2].split('T')[0] + '/' + dt[1] + '/' + dt[0]
        to_date = dates['to'] and dates['to'] or default_date
        fdate = DateTime(from_date, datefmt='MX')
        tdate = DateTime(to_date, datefmt='MX')

        workshops = self.workshops(fdate, tdate)

        participants = {
            'headers': [],
            'rows': [],
            'countries': {},
            'institutions': {},
            'genders': {},
        }

        countries = {}
        institutions = {}
        genders = {}

        exclude_names = (
            'IBasic.title',
            'IBasic.description',
            'description',
            'title'
            # 'IMembership.certificatesended',
            # 'IMembership.certificaterequested',
        )

        headers = []
        names = []
        obj = api.content.find(portal_type='Participant')[0].getObject()
        viewitem = obj.unrestrictedTraverse('view')
        viewitem.update()

        default_widgets = viewitem.widgets.values()

        for widget in default_widgets:
            if widget.__name__ not in exclude_names:
                headers.append(widget.label)
                names.append(widget.__name__)

        groups = viewitem.groups
        for group in groups:
            widgetsg = group.widgets.values()
            for widget in widgetsg:
                headers.append(widget.label)
                names.append(widget.__name__)

        participants['headers'] = headers

        for workshop in workshops:
            obj = workshop.getObject()
            for participant in obj.listFolderContents():
                if participant.portal_type == 'Participant' and participant.attendance == u'Confirmed':
                    row = [participant.UID()]
                    row.append(participant.absolute_url())
                    for name in names:
                        newname = name.split('.')[-1]
                        value = getattr(participant, newname, None)
                        row.append(value)
                        if name == 'IPerson.country':
                            countries.setdefault(value, 0)
                            countries[value] += 1
                        elif name == 'IPerson.affiliation':
                            institutions.setdefault(value, 0)
                            institutions[value] += 1
                        elif name == 'IPerson.gender':
                            genders.setdefault(value, 0)
                            genders[value] += 1

                    participants['rows'].append(row)

        # for workshop in workshops:
        #     obj = workshop.getObject()
        #     for participant in obj.listFolderContents():
        #         if participant.portal_type == 'Participant' and participant.attendance == u'Confirmed':
        #             row = [participant.UID()]
        #             row.append(participant.absolute_url())
        #             viewitem = participant.unrestrictedTraverse('view')
        #             viewitem.update()

        #             default_widgets = viewitem.widgets.values()
        #             groups = viewitem.groups

        #             for widget in default_widgets:
        #                 if widget.__name__ not in exclude_names:
        #                     row.append(widget.value)

        #             for group in groups:
        #                 widgetsg = group.widgets.values()
        #                 for widget in widgetsg:
        #                     if widget.__name__ in['IAcommodation.hotel', 'IMembership.certificatesended', 'IMembership.certificaterequested']:
        #                         row.append(','.join(widget.value))
        #                     else:
        #                         row.append(widget.value)

        #                     if widget.__name__ == 'IPerson.country':
        #                         countries.setdefault(widget.value, 0)
        #                         countries[widget.value] += 1

        #                     if widget.__name__ == 'IPerson.affiliation':
        #                         institutions.setdefault(widget.value, 0)
        #                         institutions[widget.value] += 1

        #                     if widget.__name__ == 'IPerson.gender':
        #                         genders.setdefault(widget.value, 0)
        #                         genders[widget.value] += 1

        #             participants['rows'].append(row)

        participants['countries'] = countries
        participants['institutions'] = institutions
        participants['genders'] = genders
        return participants
