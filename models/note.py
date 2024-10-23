from odoo import models, fields, api

class Note(models.Model):
    _name = 'university.notes'
    _description = 'The notes of the universities'

    student_id = fields.Many2one('university.students', string='Student')
    enroll_id = fields.Many2one('university.enrolls', string='enroll')
    note = fields.Float()
    name = fields.Char(compute='_compute_name', store=True, readonly=True)
    subject = fields.Char(related='enroll_id.subject_id.name', string='Subject',readonly=True)
    
    @api.depends('student_id', 'enroll_id', 'note')
    def _compute_name(self):
        if self.create_date:
            for record in self:
                day = record.create_date.day
                month = record.create_date.month
                year = record.create_date.year
                record.name = f"{year}-{month}-{day},{record.subject},{record.note}"