# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from cmo.events.testing import CMO_EVENTS_INTEGRATION_TESTING  # noqa
from plone import api

import unittest


class TestSetup(unittest.TestCase):
    """Test that cmo.events is properly installed."""

    layer = CMO_EVENTS_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if cmo.events is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'cmo.events'))

    def test_browserlayer(self):
        """Test that ICmoEventsLayer is registered."""
        from cmo.events.interfaces import (
            ICmoEventsLayer)
        from plone.browserlayer import utils
        self.assertIn(ICmoEventsLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = CMO_EVENTS_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['cmo.events'])

    def test_product_uninstalled(self):
        """Test if cmo.events is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'cmo.events'))

    def test_browserlayer_removed(self):
        """Test that ICmoEventsLayer is removed."""
        from cmo.events.interfaces import \
            ICmoEventsLayer
        from plone.browserlayer import utils
        self.assertNotIn(ICmoEventsLayer, utils.registered_layers())
