# -*- coding: utf-8 -*-
from matem.sis import MessageFactory as _
# from plone.directives import form
from zope import schema
# from zope.interface import provider
# from zope.schema.interfaces import IContextAwareDefaultFactory

from plone.supermodel import model
from zope.interface import Interface

class IParticipant(model.Schema):
    # class IParticipant(Interface):
    """An application form for renewal scholarship.
    """
    # form.mode(title='hidden')
    title = schema.TextLine(
        title=_(u'Title'),
        required=False,
        # default=u'solicitud-20171'
    )

    workshop = schema.TextLine(
        title=_(u'label_cmo_workshop', u'Workshop'),
        required=False,
    )

