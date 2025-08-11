from odoo import api, models, fields


class RealEstateProperty(models.Model):
    _name = 'real.estate.property'
    _description = 'Real Estate Property'

    name = fields.Char(string="Property Name", required=True)
    description = fields.Text(string="Description")
    price = fields.Float(string="Price", required=True)
    property_type = fields.Selection([
        ('apartment', 'Apartment'),
        ('house', 'House'),
        ('land', 'Land'),
    ], string="Property Type", required=True)
    state = fields.Selection([
        ('available', 'Available'),
        ('sold', 'Sold'),
    ], string="Status", default='available')


