from odoo import models, fields, api

class Note(models.Model):
    _name = 'university.notes'
    _description = 'The notes of the universities'

    student_id = fields.Many2one('university.students', string='Student')
    enroll_id = fields.Many2one('university.enrolls', string='enroll')
    note = fields.Float()
    name = fields.Char(compute='_compute_name', store=True, readonly=True)
    #subject = fields.Char(related='enroll_id.subject_id.name', string='Subject',readonly=True)
    
    @api.depends('student_id', 'enroll_id', 'note')
    def _compute_name(self):
        for record in self:
            subject = record.enroll_id.subject_id.name;
            if record.create_date:
                day = record.create_date.day
                month = record.create_date.month
                year = record.create_date.year
                record.name = f"{year}-{month}-{day},{subject},{record.note}"
    
    @api.onchange('enroll_id')
    def _onchange_enroll_id(self):
        if self.enroll_id:
            self.student_id = self.enroll_id.student_id
    
    # Constraints
    _sql_constraints = [
        ('note_check', 'CHECK(note >= 0 AND note <= 10)', 'The note must be between 0 and 10'),
    ]