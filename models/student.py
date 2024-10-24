from odoo import models, fields, api

class Student(models.Model):
    _name = 'university.students'
    _description = 'The students of the universities.'

    name = fields.Char(string='Name', required=True)
    university_id = fields.Many2one('university.university', string='University')
    
    # Image field
    image = fields.Image()
    
    # Directions
    street = fields.Char(string='Street')
    city = fields.Char(string='City')
    postal_code = fields.Char(string='Postal Code')
    country = fields.Many2one('res.country', string='Country')
    province = fields.Many2one('res.country.state', string='State')
    
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
