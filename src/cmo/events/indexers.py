# -*- coding: utf-8 -*-
from cmo.events.interfaces import IWorkshop
from plone.indexer.decorator import indexer
import Missing


@indexer(IWorkshop)
def workshop_start(obj):
    date = obj.start_date
    if date is None:
        return Missing.Value
    return date

@indexer(IWorkshop)
def workshop_end(obj):
    date = obj.end_date
    if date is None:
        return Missing.Value
    return date
