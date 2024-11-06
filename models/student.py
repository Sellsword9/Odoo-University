from re import S
from odoo import models, fields, api
from odoo.exceptions import UserError
import base64

class Student(models.Model):
    _name = 'university.students'
    _description = 'The students of the universities.'
    _inherit = ['university.has.directions']
    
    name = fields.Char(string='Name', required=True)
    university_id = fields.Many2one('university.university', string='University', required=True)
    
    # User field
    user_id = fields.Many2one('res.users', string='User', store=True)
    username = fields.Char(string='Email', related='user_id.login', readonly = True, store = True)
    # Create user on creation
    
    @api.model
    def create(self, vals):
        student = super(Student, self).create(vals)
        if not student.user_id:
            student.create_user()
        return student
    
    @api.model
    def write(self, vals):
        res = super(Student, self).write(vals)
        if 'name' in vals:
            self.create_user()
        return res
    
    def create_user(self):
        self.ensure_one()
        words = self.name.split()
        if len(words) < 2:
            words.append(words[0]) # Duplicating the name if no last name of any kind provided
        university = self.university_id.shortname.lower().replace(" ", "")
        
        base_username = createUsername(words[0], words[1], university)
        
        c = 1
        # O(n) is not important because 
        # in a single university there will be a small number of students 
        # with the exact same initial & last name,
        # and for most cases it will be O(1)
        while self.env['res.users'].search([('login', '=', base_username)]):
            c += 1
            u = createUsername(words[0], words[1]+str(c), university)
            base_username = u
            
                
        user = self.env['res.users'].create({
            'name':  self.name,
            'login': base_username,
            'email': base_username,
        })
        self.user_id = user.id
    
    
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

    
    
    # Counts and average
    
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


    # Email and pdf generation

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
        
        attachment = self.env['ir.attachment'].create({
            'name': f"Student Report {self.name}.pdf",
            'datas': pdf_attach,
            'res_model': 'university.students',
            'res_id': self.id
        })
        
        ctx['default_attachment_ids'] = [attachment.id]
        
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

def createUsername(name, part2, university):
    username = f"{name[0]}{part2}@nb.{university}.com"
    return username.lower()