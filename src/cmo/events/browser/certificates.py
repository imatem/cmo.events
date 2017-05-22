from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
# from UNAM.imateCVct import _
# from UNAM.imateCVct.vocabularies import CURSOSEMUNAM
# from collections import OrderedDict
# from operator import itemgetter
# from plone.i18n.normalizer import idnormalizer as idn
# from zope.component import getUtility
from zope.component.hooks import getSite
# from zope.i18n import translate
# from zope.schema.interfaces import IVocabularyFactory
# import collections
# from DateTime import DateTime
# from matem.fsdextender import users


class CertificatesView(BrowserView):

    def __init__(self, context, request):
        self.context = context
        self.request = request

        # self.atype = self.context.portal_type.replace('Folder', '')

    def __call__(self):
        self.form = self.request.form
        if self.request.form:
            if 'certificatebox' in self.request.form.keys():
                    if type(self.request.form['certificatebox']) == str:
                        uids = [self.request.form['certificatebox']]
                    else:
                        uids = self.request.form['certificatebox']
                    # for uid in uids:
                    #     brain = self.catalog.searchResults(
                    #         portal_type='',
                    #         UID=uid,
                    #     )
                    #     if brain:
                    #         apps.append(brain[0].getObject())
            import pdb; pdb.set_trace()
            pass

        return self.index()

    @property
    def catalog(self):
        return getToolByName(getSite(), 'portal_catalog')

    def participants(self):

        participants = {}
        if self.context.portal_type == 'Workshop':
            myview = self.context.unrestrictedTraverse('view')
            participants = myview.participantsWithcolumnOrder()
        return participants

    # def getYear(self):
    #     year = DateTime().year()
    #     if self.request.form:
    #         from_year = self.request.form.get('from', str(year))
    #         return eval(from_year)
    #     return year



    # def getYears(self):
    #     year = DateTime().year()
    #     return range(2010, year + 1)

    # @property
    # def app_path(self):

    #     return [
    #         'servicios',
    #         'servicios-internos',
    #         'ayuda',
    #         'informes',
    #         str(self.getYear()),
    #     ]