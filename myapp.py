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
import urllib2
import os
from google.appengine.ext.webapp import template
from google.appengine.ext import db

class StudentDetail(db.Model):
    id = db.StringProperty()
    date = db.StringProperty()
    exams = db.StringProperty(multiline=True)
    daily_notes = db.StringProperty(multiline=True)
    contact_matters = db.StringProperty(multiline=True)

class Student(db.Model):
    id = db.StringProperty()
    birthday = db.StringProperty()
    name = db.StringProperty()
    address = db.StringProperty()
    parent_name = db.StringProperty()
    parent_tel = db.StringProperty()
    emergency_tel = db.StringProperty()
    school = db.StringProperty()
    classno = db.StringProperty()
    teacher = db.StringProperty()
    teacher_tel = db.StringProperty()
    district = db.StringProperty()
    progress = db.StringProperty(multiline=True)
    exams = db.StringProperty(multiline=True)
    daily_notes = db.StringProperty(multiline=True)
    contact_matters = db.StringProperty(multiline=True)
    date = db.DateTimeProperty(auto_now_add=True)

class StudentDetailHandler(webapp2.RequestHandler):
    def post(self):
        q = self.request
        r = self.response
        s = Student(key_name=q.get('id','0'))
        sd = StudentDetail.gql('where id=:1 and date=:2',q.get('id','0'),q.get('date','2013/01/01')).get()
        sd.id = q.get('id','0')
        sd.date = q.get('date','2013/01/01')
        sd.exams = q.get('exams','')
        sd.daily_notes = q.get('daily_notes','')
        sd.contact_matters = q.get('contact_matters','')
        sd.put()
        s = Student.gql('where id =:1',q.get('id','0')).get()
        s.exams = q.get('exams','')
        s.daily_notes = q.get('daily_notes','')
        s.contact_matters = q.get('contact_matters','')
        s.put()
        
        self.redirect('/students')

class StudentsHandler(webapp2.RequestHandler):
    def get(self):
        r = self.response
        template_values = { }

        students = Student.all().fetch(100)
        
        template_values['students'] = students
        for s in students:
            if s!= None and ( s.name == None or len(s.name)==0 ):
                s.name = '[Name]'

        request = urllib2.unquote(self.request.path)
        path = os.path.join(os.path.dirname(__file__), 'students.html')
        r.out.write(template.render(path, template_values))
        
class StudentHandler(webapp2.RequestHandler):
    def get(self):
        q = self.request
        r = self.response
        s = Student.gql('where id =:1',q.get('id','0')).get()
            
        student_details = StudentDetail.gql('where id =:1 order by date desc',q.get('id','0')).fetch(100)
        
        template_values = { }
        template_values['s'] = s
        template_values['student_details'] = student_details

        request = urllib2.unquote(self.request.path)
        path = os.path.join(os.path.dirname(__file__), 'student.html')
        r.out.write(template.render(path, template_values))

    def post(self):
        q = self.request
        r = self.response
        s = Student(key_name=q.get('id','0'))
        s.id = q.get('id','0')
        s.name = q.get('name','')
        s.birthday = q.get('birthday','')
        s.address = q.get('address','')
        s.parent_name = q.get('parent_name','')
        s.parent_tel = q.get('parent_tel','')
        s.emergency_tel = q.get('emergency_tel','')
        s.school = q.get('school','')
        s.classno = q.get('classno','')
        s.teacher = q.get('teacher','')
        s.teacher_tel = q.get('teacher_tel','')
        s.district = q.get('district','')
        s.progress = q.get('progress','')
        s.exams = q.get('exams','')
        s.daily_notes = q.get('daily_notes','')
        s.contact_matters = q.get('contact_matters','')
        s.put()
        
        self.redirect('/students')

class LoginHandler(webapp2.RequestHandler):
    def get(self):
        r = self.response
        template_values = { }

        request = urllib2.unquote(self.request.path)
        path = os.path.join(os.path.dirname(__file__), 'login.html')

        r.out.write(template.render(path, template_values))

    def post(self):
        q = self.request
        r = self.response
        password = q.get('password')
        if password=='1111':
            self.redirect('/students')
        else:
            r.write('login failed')



class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.redirect('/login')
        
class CommandHandler(webapp2.RequestHandler):
    def get(self):
        r = self.response
        command = urllib2.unquote(self.request.path)
        r.write(command)
        
        if command == '/info':
            r.write('ssss')

app = webapp2.WSGIApplication([
    ('/', MainHandler)
    , ('/login', LoginHandler)
    , ('/students', StudentsHandler)
    , ('/student', StudentHandler)
    , ('/student_detail', StudentDetailHandler)
    , ('/.*', CommandHandler)
], debug=True)
