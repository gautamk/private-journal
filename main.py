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



class MainHandler(BaseHandler):
    def get(self):
        posts = BlogPost.query().order(-BlogPost.created_at).fetch()
        self.write_template("index.html",{
            "posts":posts
        })
    def post(self):
        title = self.request.get("title")
        body = self.request.get("body")
        post = BlogPost(title = title, body = body)
        post.put()
        self.redirect("/")


class PostHandler(BaseHandler):
    def get(self,post_id):
        post = ndb.Key(urlsafe=post_id).get()
        self.write_template("post.html",{
            "post":post
        })

    def post(self,post_id):
        post = ndb.Key(urlsafe=post_id).get()
        post.title = self.request.get("title")
        post.body  = self.request.get("body")
        post.put()
        self.redirect("/")

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/post/(.*)',PostHandler)
], debug=True)
