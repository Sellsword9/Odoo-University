import re
from odoo import models, fields, api

class Professor(models.Model):
    _name = "university.professors"
    _description = "The professors of the universities."
    
    name = fields.Char()
    university_id = fields.Many2one("university.university", required=True)
    department_id = fields.Many2one("university.departments")
    subjects = fields.Many2many("university.subjects", compute="_compute_subjects", readonly = False)
    enrolls = fields.One2many("university.enrolls", "professor_id")

    enroll_count = fields.Char(string="Enroll Count", compute="_compute_enroll_count")
    @api.depends('enrolls')
    def _compute_enroll_count(self):
        for record in self:
           if record.enrolls:
               record.enroll_count = str(len(record.enrolls)) + " enrolls"
           else:
                record.enroll_count = "No enrolls yet"
    @api.depends('enrolls')
    def _compute_subjects(self):
        for record in self:
            for enroll in record.enrolls:
                record.subjects = record.subjects | enroll.subject_id
    image = fields.Image()
    
    
                
    # Department head calculation
    boss = fields.One2many("university.departments", "head")
    is_head = fields.Boolean(compute="_is_head", readonly = False)
    @api.depends('department_id')
    def _is_head(self):
        for record in self:
            if record.boss == record:
                record.is_head = True
            else:
                record.is_head = False
    
    @api.model
    def create(self, vals):
        res = super(Professor, self).create(vals)
        res.is_head = res.boss == res
        return res          