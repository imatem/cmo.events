# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s cmo.events -t test_event.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src cmo.events.testing.CMO_EVENTS_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot src/plonetraining/testing/tests/robot/test_event.robot
#
# See the http://docs.plone.org for further details (search for robot
# framework).
#
# ============================================================================

*** Settings *****************************************************************

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***************************************************************

Scenario: As a site administrator I can add a Event
  Given a logged-in site administrator
    and an add event form
   When I type 'My Event' into the title field
    and I submit the form
   Then a event with the title 'My Event' has been created

Scenario: As a site administrator I can view a Event
  Given a logged-in site administrator
    and a event 'My Event'
   When I go to the event view
   Then I can see the event title 'My Event'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add event form
  Go To  ${PLONE_URL}/++add++Event

a event 'My Event'
  Create content  type=Event  id=my-event  title=My Event


# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.title  ${title}

I submit the form
  Click Button  Save

I go to the event view
  Go To  ${PLONE_URL}/my-event
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a event with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the event title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
