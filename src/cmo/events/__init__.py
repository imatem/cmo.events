# -*- coding: utf-8 -*-
"""Init and utils."""

from datetime import datetime
from datetime import timedelta
from plone import api
from zope.i18nmessageid import MessageFactory


_ = MessageFactory('cmo.events')
token_timeout = 60 * 60 * 12  # 12 hours


def valid_token():
    """Check whether or not the token is still valid.

    A token is valid for token_timeout seconds.

    :returns: bool
    """
    token_time = api.portal.get_registry_record('cmo.token_time')
    if token_time is None:
        return False
    expirationdate = datetime.utcfromtimestamp(token_time) + timedelta(seconds=token_timeout)
    return datetime.utcnow() < expirationdate
