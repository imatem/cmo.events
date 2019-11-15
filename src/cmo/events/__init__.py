# -*- coding: utf-8 -*-
"""Init and utils."""

from datetime import datetime
from datetime import timedelta
from zope.i18nmessageid import MessageFactory


_ = MessageFactory('cmo.events')
token_timeout = 60 * 60 * 12  # 12 hours
_tokens = None


def _valid_token(email):
    if _tokens is None or email not in _tokens:
        return False
    expirationdate = datetime.utcfromtimestamp(_tokens[email]['time']) + timedelta(seconds=token_timeout)
    return datetime.utcnow() < expirationdate
