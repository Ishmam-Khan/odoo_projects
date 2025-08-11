from odoo import models, fields, api
from odoo.odoo.api import ondelete

class JobCostingMaterialLine(models.Model):
    _name = 'job.costing.material.line'
    _description = 'Job Costing Material Line'


    cost_sheet_id = fields.Many2one('cost.sheet', string='Cost Sheet Reference', index=True, required=True, ondelete='cascade')
    date = fields.Datetime(string="Create Date", readonly=True, default=fields.Datetime.now)
    job_type_id = fields.Many2one('job.type', string="Job Type", domain="[('job_type', '=', 'material')]")
    product_id = fields.Many2one('product.product', string="Product", required=True, ondelete='restrict')
    description = fields.Char(string="Description",related='job_type_id.name',store=True)
    # date_of_birth = fields.Date(string="Date of Birth",related='patient_id.date_of_birth',store=True)
    reference = fields.Char(string="Reference")
    quantity = fields.Float(string="Quantity", required=True)
    uom_id = fields.Many2one('uom.uom', string="Unit of Measure", related='product_id.uom_id', readonly=True)
    invoiced_qty = fields.Float(string="Invoiced Quantity", readonly=True)
    unit_price = fields.Float(string="Unit Price")
    actual_purchase_qty = fields.Float(string="Actual Purchase Quantity")
    actual_invoice_qty = fields.Float(string="Actual Invoice Quantity")
    material_subtotal = fields.Monetary(string="Material Subtotal", compute="_compute_material_subtotal")
    currency_id = fields.Many2one('res.currency', string="Currency", default=lambda self: self.env.company.currency_id)

    @api.depends('quantity', 'unit_price')
    def _compute_material_subtotal(self):
        for record in self:
            record.material_subtotal = record.quantity * record.unit_price

    # @api.onchange('product_id')
    # def _onchange_product_id(self):
    #     """Automatically set UoM from the selected product"""
    #     if self.product_id:
    #         self.uom_id = self.product_id.uom_id

    # @api.onchange('product_id')
    # def _onchange_product_id(self):
    #     if self.product_id and self.product_id.type != 'consu':
    #         self.product_id = False
    #         return {'warning': {
    #             'title': "Invalid Product Selection",
    #             'message': "Only storable products are allowed in the material line."
    #         }}