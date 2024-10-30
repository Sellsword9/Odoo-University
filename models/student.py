from odoo import models, fields, api
from odoo.exceptions import UserError
import base64

class Student(models.Model):
    _name = 'university.students'
    _description = 'The students of the universities.'
    _inherit = ['university.has.directions']
    name = fields.Char(string='Name', required=True)
    university_id = fields.Many2one('university.university', string='University')
    
    # Image field
    image = fields.Image()
    
    
    
    # Academic Information
    tutor = fields.Many2one('university.professors', string='Tutor')
    enrolls = fields.One2many('university.enrolls', 'student_id', string='enrolls')
    notes = fields.One2many('university.notes', 'student_id', string='Notes')

    # Computed fields
    enroll_count = fields.Char(string="Enroll Count", compute="_compute_enroll_count")
    note_count = fields.Integer(string="Notes Count", compute="_compute_note_count")
    note_count_str = fields.Char(string="Notes Count", compute="_compute_note_count_str")
    average = fields.Float(string="Average", compute="_compute_average", store=True)
    @api.depends('enrolls')
    def _compute_enroll_count(self):
        for record in self:
           if record.enrolls:
               record.enroll_count = str(len(record.enrolls)) + " enrolls"
           else:
                record.enroll_count = "No enrolls yet"
    @api.depends('notes')
    def _compute_note_count(self):
        for record in self:
            if record.notes:
                record.note_count = len(record.notes) 
            else:
                record.note_count = 0
    @api.depends('note_count')
    def _compute_note_count_str(self):
        for record in self:
            if record.note_count:
                record.note_count_str = str(record.note_count) + " notes"
            else:
                record.note_count_str = "No notes yet"
    @api.depends('enrolls.average', 'enrolls')
    def _compute_average(self):
        for record in self:
            if record.enrolls:
                sum = 0
                for enroll in record.enrolls:
                    sum += enroll.average
                record.average = sum / len(record.enrolls)
            else:
                record.average = 0
        
    def action_student_send(self):
        """ Opens a wizard to compose an email, with relevant mail template loaded by default """

        ctx = {
            'default_model': 'university.students',
            'default_res_ids': self.ids,
            'default_composition_mode': 'comment',
            'default_email_layout_xmlid': 'mail.mail_notification_layout_with_responsible_signature',
        }

        # Select mass mailing mode if multiple records are selected
        if len(self) > 1:
            ctx['default_composition_mode'] = 'mass_mail'
        else:
            # Update context for single emails
            ctx.update({
                'force_email': True,
                'model_description': 'Student Report',
            })
            mail_template = self._find_mail_template()
            if mail_template:
                ctx.update({
                    'default_template_id': mail_template.id,
                    'mark_as_sent': True,
                })

        # Define action for email composition wizard
        action = {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(False, 'form')],
            'target': 'new',
            'context': ctx,
        }
        return action

    def _find_mail_template(self):
        """ Get the appropriate mail template for the enrollment based on its state. """
        self.ensure_one()
        return self.env.ref('university.email_template_student', raise_if_not_found=False)

        