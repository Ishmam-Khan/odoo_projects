from odoo import models, fields, api
from odoo.exceptions import UserError

class CostSheet(models.Model):
    _name = 'cost.sheet'
    _inherit = ['mail.thread']
    _description = 'Cost Sheet'

    name = fields.Char(string="Cost Sheet Name", required=True, tracking=True)
    #create_date = fields.Date(string="Create Date")
    #close_date = fields.Date(string="Close Date")
    #close_date = fields.Date(string="Close Date", required=True)
    reference = fields.Char(string="Reference", default='New')
    material_line_ids = fields.One2many('job.costing.material.line','cost_sheet_id', string="Job Type Material")
    labour_line_ids = fields.One2many('job.costing.labour.line','cost_sheet_id_labour', string="Job Type Labour")
    overhead_line_ids = fields.One2many('job.costing.overhead.line','cost_sheet_overhead_id', string="Job Type Overhead")
    currency_id = fields.Many2one('res.currency', string="Currency", default=lambda self: self.env.company.currency_id)
    #total_quantity = fields.Float(string="Total Quantity", compute="_compute_total_quantity")
    #total_subtotal = fields.Monetary(string="Total Subtotal", compute="_compute_total_subtotal")
    total_material_subtotal = fields.Monetary(string="Total Material Subtotal", compute="_compute_total_material_subtotal")
    total_labour_subtotal = fields.Monetary(string="Total Labour Subtotal", compute="_compute_total_labour_subtotal")
    total_overhead_subtotal = fields.Monetary(string="Total Overhead Subtotal", compute="_compute_total_overhead_subtotal")

    project_id = fields.Many2one(
        'project.project', string="Project")
    state = fields.Selection([
        ('draft', 'Draft'), ('confirmed', 'Confirmed'), ('approved', 'Approved'),
        ('done', 'Done'), ('cancel', 'Cancelled')
    ], default='draft')
    create_date = fields.Datetime(string="Create Date", readonly=True, default=fields.Datetime.now)
    close_date = fields.Date(string="Close Date", tracking=True)
    created_by = fields.Many2one('res.users', string="Created By", default=lambda self: self.env.user, readonly=True)

    # @api.depends('material_line_ids.quantity')  # Triggered when quantity changes
    # def _compute_total_quantity(self):
    #     for record in self:
    #         total_qty = sum(line.quantity for line in record.material_line_ids)
    #         record.total_quantity = total_qty

    @api.depends('material_line_ids.material_subtotal')  # Triggered when subtotal changes
    def _compute_total_material_subtotal(self):
        for record in self:
            total_material_subtotal = sum(line.material_subtotal for line in record.material_line_ids)
            record.total_material_subtotal = total_material_subtotal

    @api.depends('labour_line_ids.labour_subtotal')  # Triggered when subtotal changes
    def _compute_total_labour_subtotal(self):
        for record in self:
            total_labour_subtotal = sum(line.labour_subtotal for line in record.labour_line_ids)
            record.total_labour_subtotal = total_labour_subtotal

    @api.depends('overhead_line_ids.overhead_subtotal')  # Triggered when subtotal changes
    def _compute_total_overhead_subtotal(self):
        for record in self:
            total_overhead_subtotal = sum(line.overhead_subtotal for line in record.overhead_line_ids)
            record.total_overhead_subtotal = total_overhead_subtotal

    # def unlink(self):  # No need for `@api.model`
    #     for record in self:
    #         if record.state != 'draft':
    #             raise UserError("You cannot delete a cost sheet unless it is in Draft state.")
    #     return super(CostSheet, self).unlink()  # Call the parent unlink method
    #
    # records = self.env['cost.sheet'].search([])
    # filtered_records = records.filtered(lambda r: r.state == 'draft')
    # if filtered_records.state:
    #     filtered_records.state.unlink()
    # else:
    #     raise UserError("Only draft jobs can be deleted!")
    # @api.model
    # def delete_draft_jobs(self):
    #     records = self.env['cost.sheet'].search([])
    #     filtered_records = records.filtered(lambda r: r.state == 'draft')
    #
    #     if filtered_records:
    #         filtered_records.unlink()  # Unlink the records, not the state
    #     else:
    #         raise UserError("Only draft jobs can be deleted!")


    # product_id = fields.Many2one(
    #     'product.product', string="Product")

    def action_confirm(self):
        for rec in self:
            rec.state = 'confirmed'

    def action_approved(self):
        for rec in self:
            rec.state = 'approved'

    def action_done(self):
        for rec in self:
            rec.state = 'done'

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'

    # def _get_next_sequence(self):
    #     return self.env['ir.sequence'].next_by_code('cost.sheet') or '/'
    #
    # @api.model
    # def create(self, vals):
    #     if not vals.get('name') or vals['name'] == '/':
    #         vals['name'] = self.env['ir.sequence'].next_by_code('cost.sheet')
    #     return super(CostSheet, self).create(vals)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('reference') or vals['reference'] == 'New':
                vals['reference'] = self.env['ir.sequence'].next_by_code('cost.sheet')
        return super().create(vals_list)

    @api.constrains('create_date', 'close_date')
    def _check_close_date(self):
        for record in self:
            if record.close_date and record.create_date and record.close_date <= record.create_date.date():
                raise ValidationError("Close Date must be greater than Create Date.")