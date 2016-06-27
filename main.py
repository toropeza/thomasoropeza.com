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
import webapp2
import os
import jinja2
from google.appengine.ext.webapp import template

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'homepage.html')
        self.response.out.write(template.render(path, {}))

class PhotographyHandler(webapp2.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'photography.html')
        self.response.out.write(template.render(path, {}))

class GalleryHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('gallery.html')
        urls = []
        names = []
        for url in os.listdir(os.path.join(os.path.dirname(__file__), "gallery/galleryphotos")):
            urls.append(os.path.splitext(url)[0])

        templateValues = {
            # Files that are in a "static" directory cannot be referenced by os
            'urls': urls

        }
        self.response.out.write(template.render(templateValues))

class ProjectHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('project.html')
        project = self.request.get('p')
        url = self.request.url
        urls = []
        for url in os.listdir(os.path.join(os.path.dirname(__file__), "gallery/projects/" + project)):
            urls.append(os.path.splitext(url)[0])

        templateValues = {
            'project': project,
            'urls': urls,
            'fullURL':url
        }
        self.response.out.write(template.render(templateValues))

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/photo', PhotographyHandler),
    ('/gallery', GalleryHandler),
    ('/project', ProjectHandler)
], debug=True)
