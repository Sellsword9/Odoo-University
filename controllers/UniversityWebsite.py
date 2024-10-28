from odoo import http
from odoo.http import request

class UniversityWebsite(http.Controller):

    @http.route(['/university'], type='http', auth='public', website=True)
    def list_universities(self, **kw):
        # Retrieve all universities
        universities = request.env['university.university'].sudo().search([])
        return request.render('university.university_list', {
            'universities': universities,
        })

    @http.route(['/professors/<model("university.university"):university>'], type='http', auth='public', website=True)
    def list_professors(self, university, **kw):
        # Retrieve all professors for the selected university
        professors = request.env['university.professors'].sudo().search([('university_id', '=', university.id)])
        return request.render('university.professor_list', {
            'professors': professors,
            'university': university,
        })
