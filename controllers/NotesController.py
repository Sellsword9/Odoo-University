from odoo import http
from odoo.http import request
import logging

class NotesController(http.Controller):
  #_logger = logging.getLogger(__name__) 

  @http.route(['/students/<model("university.students"):student>'], type='http', auth='public', website=True)
  def list_notes(self, student, **kw):
      # this should only work if the user is an admin. No need for a student to see their own notes bc no difference with /notes
      cuserint = request.env.context.get('uid')
      cuser = request.env['res.users'].sudo().search([('id', '=', cuserint)])
      
      
      if not cuser.has_group('base.group_system'):
          return False
        
        
      # Retrieve all notes for the selected student
      notes = request.env['university.notes'].sudo().search([('student_id', '=', student.id)])
      return request.render('university.notes_per_student', {
          'notes': notes,
          'student': student,
      })
  @http.route(['/subjects/<model("university.subjects"):subject>'], type='http', auth='public', website=True)
  def list_notes_per_subject(self, subject, **kw):

      cuserint = request.env.context.get('uid')
      cuser = request.env['res.users'].sudo().search([('id', '=', cuserint)])

      # If admin, show every note
      if cuser.has_group('base.group_system'):
        notes = request.env['university.notes'].sudo().search([('enroll_id.subject_id', '=', subject.id)])
      else:
        # the user is a student so we show they only their notes
        notes = request.env['university.notes'].sudo().search([('student_id',"=", cuser.id), ('enroll_id.subject_id', '=', subject.id)])


      return request.render('university.notes_per_subject', {
          'notes': notes,
          'subject': subject,
      })
  @http.route(['/notes'], type='http', auth='public', website=True)
  def list_all_notes(self, **kw):
      # Retrieve all notes from User student
      cuserint = request.env.context.get('uid')
      cuser = request.env['res.users'].sudo().search([('id', '=', cuserint)])
      
      #this var decides if there are links to students. 
      linkable_students = 1

      student = request.env['university.students'].sudo().search([('user_id', '=', cuserint)])
      studentid = student.id
      # if user is admin, all notes, if not admin, only notes from the student, if neither, empty list
      if cuser.has_group('base.group_system'):
        #self._logger.info('El usuario no es administrador')
        notes = request.env['university.notes'].sudo().search([])
        linkable_students = True
      elif studentid:
        notes = request.env['university.notes'].sudo().search([('student_id', '=', studentid)])
        linkable_students = False
      else:
        notes = []
        linkable_students = False
      return request.render('university.notes_list', {
          'notes': notes,
          'linkable_students': linkable_students
      })
