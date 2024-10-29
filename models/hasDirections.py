from odoo import models, fields, api
from odoo.exceptions import ValidationError

class HasDirections(models.AbstractModel):
    _name = 'university.has.directions'
    _description = 'Record which has a physical direction'
    
    street = fields.Char(string="Street")
    city = fields.Char(string="City")
    province = fields.Many2one('res.country.state', string='province')
    country = fields.Many2one('res.country', string='Country')

    postal_code = fields.Char('Postal Code')
    
    
    # Constrain so that province matches country
    @api.constrains('province', 'country')
    def _check_province(self):
        for record in self:
            if record.province and record.country:
                if record.province.country_id != record.country:
                    raise ValidationError('Province must be in the selected country')

    # If province is set, set country to province's country
    @api.onchange('province')
    def _onchange_province(self):
        if self.province:
            self.country = self.province.country_id
