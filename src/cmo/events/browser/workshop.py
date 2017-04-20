# -*- coding: utf-8 -*-
from plone.autoform.view import WidgetsView
from plone.dexterity.interfaces import IDexterityFTI
from plone.dexterity.utils import getAdditionalSchemata
from Products.CMFPlone.resources import add_resource_on_request
from zope.component import getUtility


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
        # add_resource_on_request(self.request, 'jquery12')
        # add_resource_on_request(self.request, 'jquerydatatablemin')
        # add_resource_on_request(self.request, 'tablecmo')
        return super(WorkshopView, self).__call__()

    def participants(self):

        items = self.context.values()

        participants = {
            'headers': [],
            'rows': []
        }
        if not items:
            return participants
        exclude_names = ('IBasic.title', 'IBasic.description', 'description',)
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
                    # row.append(getattr(item, widget.name, None))
                    row.append(widget.value)

            participants['rows'].append(row)
        return participants
