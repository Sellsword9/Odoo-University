from odoo import models, fields, api
import pytz
from datetime import datetime

class University(models.Model):
    _name = "university.university"
    _description = "The universities of the system."
    _inherit = ['university.has.directions']
    
    name = fields.Char()
    shortname = fields.Char(compute="_compute_shortname", store=True)
    
    @api.depends("name")
    def _compute_shortname(self):
        for record in self:
            if record.name and len(record.name) > 0 and type(record.name) == str:
                parts = record.name.split()
                # remove less than 3 words parts except first and last
                if len(parts) > 2:
                    for i in range(1, len(parts)-1):
                        if len(parts[i]) < 3:
                            parts.pop(i)
                if len(record.name) < 5:
                    record.shortname = record.name
                elif len(parts) == 1:
                    record.shortname = record.name[:5]
                else: 
                    record.shortname = ""
                    while len(record.shortname) < 5 and parts:
                        record.shortname += parts.pop(0)[:1]
    
    # Image field
    image = fields.Image()
    imagePath = fields.Char(compute="_compute_imagePath", store=True)

    def _compute_imagePath(self):
        for record in self:
            if record.image:
                record.imagePath = "/web/image/university.university/" + str(record.id) + "/image/"
            else:
                record.imagePath = False
    
    # Internal relationships fields
    enrolls = fields.One2many("university.enrolls", "university_id")
    students = fields.One2many("university.students", "university_id")
    professors = fields.One2many("university.professors", "university_id")
    departments = fields.One2many("university.departments", "university_id")

    # Computed field for enroll & professor count
    enroll_count = fields.Char(string="Enroll Count", compute="_compute_enroll_count")
    professors_count = fields.Char(string="Professors Count", compute="_compute_professors_count")
    departments_count = fields.Char(string="Departments Count", compute="_compute_departments_count")
    students_count = fields.Char(string="Students Count", compute="_compute_students_count")
    
    
    @api.depends('enrolls')
    def _compute_enroll_count(self):
        
        for record in self:
           if record.enrolls:
               record.enroll_count = str(len(record.enrolls)) + " enrolls"
           else:
                record.enroll_count = "No enrolls yet"
    @api.depends('professors')
    def _compute_professors_count(self):
        for record in self:
           if record.professors:
               record.professors_count = str(len(record.professors)) + " professors"
           else:
                record.professors_count = "No professors yet"
    @api.depends('departments')    
    def _compute_departments_count(self):
        for record in self:
           if record.departments:
               record.departments_count = str(len(record.departments)) + " departments"
           else:
                record.departments_count = "No departments yet"
    @api.depends('students')
    def _compute_students_count(self):
        for record in self:
           if record.students:
               record.students_count = str(len(record.students)) + " students"
           else:
                record.students_count = "No students yet"


    # ---------------------------------------------------------- #
    #                       Odds and ends
    # ---------------------------------------------------------- #
    
    # Field for storing the path to country flags
    basepath = "/base/static/img/country_flags/"
    flag = fields.Char(compute="_compute_flag", store=True)
    
    @api.depends("country")
    def _compute_flag(self):
        for record in self:
            if record.country:
                record.flag = self.basepath + record.country.code.lower() + ".png"
            else:
                record.flag = False

    # Field for storing the local time of the university
    local_time = fields.Char(compute="_compute_local_time", store=False)
    @api.depends("country")
    def _compute_local_time(self):
        for record in self:
            if record.country and record.country.code:
                # Get the timezone based on the country code
                try:
                    timezone = pytz.country_timezones.get(record.country.code.lower(), [None])[0]
                    if timezone:
                        # Get the current time in the specified timezone
                        tz = pytz.timezone(timezone)
                        record.local_time = datetime.now(tz).strftime("%H:%M:%S")
                    else:
                        record.local_time = "Timezone not available"
                except Exception as e:
                    record.local_time = "Error: " + str(e)
            else:
                record.local_time = "Country not set"
