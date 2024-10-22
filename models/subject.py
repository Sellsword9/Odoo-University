from odoo import models, fields, api

class Subject(models.Model):
    _name = "university.subjects"
    _description = "The subjects of the universities."
    
    name = fields.Char()
    university_id = fields.Many2one("university.university")
    professors = fields.Many2many("university.professors")
    enrolls = fields.One2many("university.enrolls", "subject_id")
    
    enroll_count = fields.Char(string="Enroll Count", compute="_compute_enroll_count")
    
    @api.depends('enrolls')
    def _compute_enroll_count(self):
        
        for record in self:
           if record.enrolls:
               record.enroll_count = str(len(record.enrolls)) + " enrolls"
           else:
                record.enroll_count = "No enrolls yet"
    
    @api.onchange('professors')
    def _onchange_professors(self):
        if self.university_id is None:
            self.university_id = self.professors[0].university_id