from odoo import models, fields, api, tools

class Dossier(models.Model):
    _name = 'university.dossier'
    _description = 'Dossier containing detailed data about students'
    _rec_name = 'enroll'
    _auto = False
    
    enroll = fields.Many2one('university.enrolls', readonly = True)
    university = fields.Many2one('university.university', readonly = True)
    student = fields.Many2one('university.students', readonly = True)
    department = fields.Many2one('university.departments', readonly = True)
    professor = fields.Many2one('university.professors', readonly = True)
    subject = fields.Many2one('university.subjects', readonly = True)
    average = fields.Float(readonly = True)

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""
            CREATE OR REPLACE VIEW university_dossier AS (
                SELECT
                    ROW_NUMBER() OVER() AS id,
                    e.id AS enroll,
                    e.university_id AS university,
                    e.student_id AS student,
                    e.professor_id AS professor,
                    p.department_id AS department,
                    e.subject_id AS subject,
                    AVG(s.average) AS average
                    
                FROM
                    university_enrolls e
                    JOIN university_professors p ON e.professor_id = p.id
                    LEFT JOIN university_students s ON e.student_id = s.id
                GROUP BY
                    e.id,
                    e.university_id,
                    e.student_id,
                    e.professor_id,
                    p.department_id,
                    e.subject_id,
                    s.average
            )""")
    
    
    
    
    
    
    
    
    
    
    
            
    """def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""
    """  CREATE OR REPLACE VIEW university_dossier AS (
                SELECT
                    ROW_NUMBER() OVER() AS id,
                    e.id AS enroll,
                    e.university_id AS university,
                    e.student_id AS student,
                    e.professor_id AS professor,
                    p.department_id AS department,
                    e.subject_id AS subject,
                    ARRAY_AGG(n.id) AS notes,
                    AVG(n.note) AS average
                FROM
                    university_enrolls e
                    JOIN university_professors p ON e.professor_id = p.id
                    LEFT JOIN university_notes n ON e.student_id = n.student_id
                GROUP BY
                    e.id,
                    e.university_id,
                    e.student_id,
                    e.professor_id,
                    p.department_id,
                    e.subject_id
            )
        """ """)"""