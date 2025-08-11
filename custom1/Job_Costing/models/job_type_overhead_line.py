from odoo import models, fields, api
from odoo.odoo.api import ondelete

class JobCostingOverheadLine(models.Model):
    _name = 'job.costing.overhead.line'
    _description = 'Job Costing Overhead Line'

    cost_sheet_overhead_id = fields.Many2one('cost.sheet', string='Cost Sheet Reference', index=True, required=True, ondelete='cascade')
    date = fields.Datetime(string="Create Date", readonly=True, default=fields.Datetime.now)
    job_type_id = fields.Many2one('job.type', string="Job Type", domain="[('job_type', '=', 'overhead')]")
    product_id = fields.Many2one('product.product', string="Product", required=True, ondelete='restrict')
    description = fields.Char(string="Description")
    reference = fields.Char(string="Reference")
    basis = fields.Char(string="Basis")
    quantity = fields.Float(string="Quantity", required=True)
    uom_id = fields.Many2one('uom.uom', string="Unit of Measure", readonly=True)
    invoiced_qty = fields.Float(string="Invoiced Quantity", readonly=True)
    unit_price = fields.Float(string="Unit Price")
    actual_purchase_qty = fields.Float(string="Actual Purchase Quantity")
    actual_invoice_qty = fields.Float(string="Actual Invoice Quantity")
    overhead_subtotal = fields.Monetary(string="Overhead Subtotal", compute="_compute_overhead_subtotal")
    currency_id = fields.Many2one('res.currency', string="Currency", default=lambda self: self.env.company.currency_id)

    @api.depends('quantity', 'unit_price')
    def _compute_overhead_subtotal(self):
        for record in self:
            record.overhead_subtotal = record.quantity * record.unit_price

    @api.onchange('product_id')
    def _onchange_product_id(self):
        """Automatically set UoM from the selected product"""
        if self.product_id:
            self.uom_id = self.product_id.uom_id