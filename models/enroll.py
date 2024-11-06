from odoo import models, fields, api

class enroll(models.Model):
    _name = "university.enrolls"
    _description = "Enrolls for every student for every subject in universities."
    
    student_id = fields.Many2one("university.students")
    university_id = fields.Many2one("university.university")
    professor_id = fields.Many2one("university.professors")
    subject_id = fields.Many2one("university.subjects")
    notes = fields.One2many("university.notes", "enroll_id")
    
    university_name = fields.Char(related="university_id.name", readonly=True)
    university_postal_code = fields.Char(related="university_id.postal_code", readonly=True)
    
    enrolls_this_subject = fields.Integer(compute="_compute_enrolls_in_subject", store=False, readonly=True)
    name = fields.Char(compute="_compute_name", store=True, readonly=True)
    
    average = fields.Float(string="Average", compute="_compute_average", store=True)
    
    @api.depends("notes", "notes.note")
    def _compute_average(self):
        for record in self:
            if record.notes:
                sum = 0
                for note in record.notes:
                    sum += note.note
                record.average = sum / len(record.notes)
            else:
                record.average = 0
    
    @api.depends("subject_id")
    def _compute_enrolls_in_subject(self):
        for record in self:
            if record.subject_id and record.subject_id.enrolls:
                record.enrolls_this_subject = len(record.subject_id.enrolls)
            else:
                record.enrolls_this_subject = 0
    
    @api.depends("subject_id")
    def _compute_name(self):
        for record in self:
            year = str(fields.Date.today().year)
            if record.create_date is not None and record.create_date is not False:
                year = str(record.create_date.year)
            
            number = record.enrolls_this_subject
            
            # Compute the subject abbreviation
            if record.subject_id.name:
                subject_abbr = get_subject_abbreviation(record.subject_id.name)
                record.name = subject_abbr + "/" + year + "/" + '{0:04}'.format(number)
            else:
                record.name = f"UNKNOWN"
        
        
        
        
    @api.onchange("student_id")
    def _onchange_student(self):
        if self.student_id.university_id and self.student_id.university_id != self.university_id:
            self.university_id = self.student_id.university_id
    @api.onchange("subject_id")
    def _onchange_subject(self):
        if self.university_id is None:
            self.university_id = self.subject_id.university_id
    @api.onchange("professor_id")
    def _onchange_professor(self):
        if self.university_id is None:
            self.university_id = self.professor_id.university_id
    
    
"""
Generate an abbreviation for a given subject name.
The abbreviation is created based on the number of words in the subject name:
- If the subject name consists of one word, the abbreviation is the first three letters of the word, in uppercase.
- If the subject name consists of two words, the abbreviation is the first two letters of the first word followed by the first letter of the second word, in uppercase.
- If the subject name consists of three or more words, the abbreviation is the first letter of each of the first three words, in uppercase.
Args:
    subject_name (str): The name of the subject to abbreviate.
Returns:
    str: The generated abbreviation for the subject name.
"""
def get_subject_abbreviation(subject_name):
    words = subject_name.split()
    if len(words) == 1:
        # One word: take the first three letters
        return words[0][:3].upper()
    elif len(words) == 2:
        # Two words: take first two letters of first word, first letter of second
        return (words[0][:2] + words[1][:1]).upper()
    else:
        # Three or more words: take the first letter of each of the first three words
        return (words[0][:1] + words[1][:1] + words[2][:1]).upper()