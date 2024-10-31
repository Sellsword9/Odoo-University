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
    tutor_id = fields.Many2one('university.professors', string='Tutor')
    enrolls = fields.One2many('university.enrolls', 'student_id', string='Enrollments')
    notes = fields.One2many('university.notes', 'student_id', string='Notes')

    # Computed fields
    enroll_count = fields.Char(string="Enroll Count", compute="_compute_enroll_count")
    note_count = fields.Integer(string="Notes Count", compute="_compute_note_count")
    note_count_str = fields.Char(string="Notes Count", compute="_compute_note_count_str")
    average = fields.Float(string="Average", compute="_compute_average", store=True)

    def _compute_pdf(self):
        for record in self:
            record.pdf = record.create_pdf()
    
    @api.depends('enrolls')
    def _compute_enroll_count(self):
        for record in self:
            record.enroll_count = f"{len(record.enrolls)} enrolls" if record.enrolls else "No enrolls yet"

    @api.depends('notes')
    def _compute_note_count(self):
        for record in self:
            record.note_count = len(record.notes)

    @api.depends('note_count')
    def _compute_note_count_str(self):
        for record in self:
            record.note_count_str = f"{record.note_count} notes" if record.note_count else "No notes yet"

    @api.depends('enrolls.average', 'enrolls')
    def _compute_average(self):
        for record in self:
            if record.enrolls:
                record.average = sum(enroll.average for enroll in record.enrolls) / len(record.enrolls)
            else:
                record.average = 0

    def action_student_send(self):

        template = self._find_mail_template()
        ctx = {
            'default_model': 'university.students',
            'default_res_ids': [self.id],
            'default_use_template': bool(template),
            'default_template_id': template and template.id or False,
            'default_composition_mode': 'comment',
            'email_to': self.env.user.email,
            'force_email': True,
        }
        
        pdf_attach = self.env['ir.actions.report'].sudo()._render_qweb_pdf('university.action_report_student', [self.id])[0]
        pdf_attach = base64.b64encode(pdf_attach)
        
        ctx['default_attachment_ids'] = [(0, 0, {
            'name': f"Student Report {self.name}.pdf",
            'datas': pdf_attach,
            'res_model': 'university.students',
            'res_id': self.id
        })]
        
        #ctx['default_subject'] = f"Student Report for {self.name}"

        
        action = {
            'name': 'Compose Email',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'views': [(False, 'form')],
            'res_model': 'mail.compose.message',
            'target': 'new',
            'context': ctx,
        }
        return action

    def _find_mail_template(self):
        """ Get the appropriate mail template for the enrollment based on its state. """
        self.ensure_one()
        return self.env.ref('university.email_template_student', raise_if_not_found=False)