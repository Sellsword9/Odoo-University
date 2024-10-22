from odoo import models, fields, api

class Department(models.Model):
    _name = "university.departments"
    _description = "The departments of the universities."
    
    name = fields.Char()
    university_id = fields.Many2one("university.university")
    head = fields.Many2one("university.professors")
    professors = fields.One2many("university.professors", "department_id")

    @api.onchange('professors')
    def _onchange_professors(self):
        for professor in self.professors:
            professor.department_id = self.id
        if self.university_id is None:
            self.university_id = self.professors[0].university_id
            
    @api.onchange('head')
    def _onchange_head(self):
        if self.head not in self.professors:
            self.professors += self.head
    # Restricting invalid head
    @api.constrains('head')
    def _check_head(self):
        for record in self:
            if record.head and record.head.department_id != record:
                raise ValueError("The head of the department should also be a professor of the department.")