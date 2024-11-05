from odoo import http
from odoo.http import request

class NotesController(http.Controller):
  
  @http.route(['/students/<model("university.students"):student>'], type='http', auth='public', website=True)
  def list_notes(self, student, **kw):
      # Retrieve all notes for the selected student
      notes = request.env['university.notes'].sudo().search([('student_id', '=', student.id)])
      return request.render('university.notes_list', {
          'notes': notes,
          'student': student,
      })
  @http.route(['/subjects/<model("university.subjects"):subject>'], type='http', auth='public', website=True)
  def list_notes_per_subject(self, subject, **kw):
      # Retrieve all notes for the selected subject
      notes = request.env['university.notes'].sudo().search([('enroll_id.subject_id', '=', subject.id)])
      return request.render('university.notes_list', {
          'notes': notes,
          'subject': subject,
      })