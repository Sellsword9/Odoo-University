from odoo import models, fields, api

class Dossier(models.Model):
    _name = 'university.dossier'
    _description = 'Dossier containing detailed data about students'

    university = fields.Many2one('university.university')
    student = fields.Many2one('university.students')
    department = fields.Many2one('university.departments')
    professor = fields.Many2one('university.professors')
    subject = fields.Many2one('university.subjects')
    notes = fields.Many2many('university.notes')
    average = fields.Float(compute='_compute_average', store=True)
    
    @api.depends('notes')
    def _compute_average(self):
        for record in self:
            record.average = sum(record.notes.grade) / len(record.notes)
            
    