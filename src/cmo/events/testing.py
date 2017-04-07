# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import cmo.events


class CmoEventsLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=cmo.events)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'cmo.events:default')


CMO_EVENTS_FIXTURE = CmoEventsLayer()


CMO_EVENTS_INTEGRATION_TESTING = IntegrationTesting(
    bases=(CMO_EVENTS_FIXTURE,),
    name='CmoEventsLayer:IntegrationTesting'
)


CMO_EVENTS_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(CMO_EVENTS_FIXTURE,),
    name='CmoEventsLayer:FunctionalTesting'
)


CMO_EVENTS_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        CMO_EVENTS_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='CmoEventsLayer:AcceptanceTesting'
)
