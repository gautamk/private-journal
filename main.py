#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
from google.appengine.ext import ndb
import webapp2
import jinja2
from models.blog import BlogPost
from util.custom_filters.pretty_time import pretty_time
from util.custom_filters.render_markdown import render_markdown

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__),"templates")),
    extensions=['jinja2.ext.autoescape'])
JINJA_ENVIRONMENT.filters["pretty_time"] = pretty_time
JINJA_ENVIRONMENT.filters["render_markdown"] = render_markdown

class BaseHandler(webapp2.RequestHandler):
    def write_template(self,template_name ,template_values):
        template = JINJA_ENVIRONMENT.get_template(template_name)
        self.response.write(template.render(template_values))

    def _get_title(self):
        return self.request.get("title")
    def _get_body(self):
        return self.request.get("body")




class MainHandler(BaseHandler):
    def get(self):
        posts = BlogPost.query().order(-BlogPost.created_at).fetch()
        self.write_template("index.html",{
            "posts":posts
        })


class PostHandler(BaseHandler):
    def get(self,post_id = None):
        post = None if post_id == None else ndb.Key(urlsafe=post_id).get()

        self.write_template("post.html",{
            "post":post
        })

    def post(self,post_id=None):
        title = self._get_title()
        body  = self._get_body()

        post = BlogPost() if post_id == None else ndb.Key(urlsafe = post_id).get()

        post.title = title
        post.body  = body
        post.put()
        self.redirect("/")

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/new/post',PostHandler),
    ('/post/(.*)',PostHandler)
], debug=True)
