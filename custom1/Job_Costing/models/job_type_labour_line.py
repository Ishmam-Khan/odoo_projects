from odoo import models, fields, api
from odoo.odoo.api import ondelete

class JobCostingLabourLine(models.Model):
    _name = 'job.costing.labour.line'
    _description = 'Job Costing Labour Line'

    cost_sheet_id_labour = fields.Many2one('cost.sheet', string='Cost Sheet Reference', index=True, required=True, ondelete='cascade')
    #date = fields.Date(string="Date")
    date = fields.Datetime(string="Create Date", readonly=True, default=fields.Datetime.now)

    job_type_id = fields.Many2one('job.type', string="Job Type", domain="[('job_type', '=', 'labour')]")
    product_id = fields.Many2one('product.product', string="Product", required=True)
    description = fields.Char(string="Description")
    reference = fields.Char(string="Reference")
    hours = fields.Float(string="Hours")
    # quantity = fields.Float(string="Quantity", required=True)
    uom_id = fields.Many2one('uom.uom', string="Unit of Measure")
    invoiced_qty = fields.Float(string="Invoiced Quantity", readonly=True)
    unit_price = fields.Float(string="Cost/Unit Price")
    # actual_purchase_qty = fields.Float(string="Actual Purchase Quantity")
    # actual_invoice_qty = fields.Float(string="Actual Invoice Quantity")
    labour_subtotal = fields.Monetary(string="Labour Subtotal", compute="_compute_labour_subtotal")
    currency_id = fields.Many2one('res.currency', string="Currency", default=lambda self: self.env.company.currency_id)

    @api.depends('hours', 'unit_price')
    def _compute_labour_subtotal(self):
        for record in self:
            record.labour_subtotal = record.hours * record.unit_price
