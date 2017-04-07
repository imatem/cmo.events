# -*- coding: utf-8 -*-
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from cmo.events.interfaces import IEvent
from cmo.events.testing import CMO_EVENTS_INTEGRATION_TESTING  # noqa
from zope.component import createObject
from zope.component import queryUtility

import unittest


class EventIntegrationTest(unittest.TestCase):

    layer = CMO_EVENTS_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name='Event')
        schema = fti.lookupSchema()
        self.assertEqual(IEvent, schema)

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='Event')
        self.assertTrue(fti)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='Event')
        factory = fti.factory
        obj = createObject(factory)
        self.assertTrue(IEvent.providedBy(obj))

    def test_adding(self):
        obj = api.content.create(
            container=self.portal,
            type='Event',
            id='Event',
        )
        self.assertTrue(IEvent.providedBy(obj))
