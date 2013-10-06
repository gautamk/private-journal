__author__ = 'gautam'

from google.appengine.ext import ndb

class BaseModel(ndb.Model):
    created_at  = ndb.DateTimeProperty(auto_now_add=True)
    modified_at = ndb.DateTimeProperty(auto_now=True)
    created_by  = ndb.UserProperty(auto_current_user_add=True)
    modified_by = ndb.UserProperty(auto_current_user=True)


class BlogPost(BaseModel):
    title = ndb.StringProperty(required=True)
    body  = ndb.TextProperty(required=True)
