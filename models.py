#!/usr/bin/env python3.6
import os
import uuid
import boto3
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, BooleanAttribute, MapAttribute, UTCDateTimeAttribute
from pynamodb.indexes import GlobalSecondaryIndex, AllProjection
from functions import get_time_now

class UserIndex(GlobalSecondaryIndex):
    """
    This class represents a global secondary index 
    (for now not used because change in table strcuture)
    """
    class Meta:
        index_name = 'user-index'
        read_capacity_units = 1
        write_capacity_units = 1
        # All attributes are projected
        projection = AllProjection()

    user = UnicodeAttribute(default='', hash_key=True)

class Event(Model):
    """
    This class define the Event table
    """
    class Meta:
        table_name = os.environ.get('STAGE', 'dev') + '.events'
        region = boto3.Session().region_name
        host = 'http://localhost:8000' \
	        if not os.environ.get('LAMBDA_TASK_ROOT') else None
    user = UnicodeAttribute(hash_key=True)
    id = UnicodeAttribute(range_key=True)
    is_free = BooleanAttribute(default=False)
    event_orig = MapAttribute()
    event_orig_str = UnicodeAttribute()
    created_at = UTCDateTimeAttribute(default=get_time_now)