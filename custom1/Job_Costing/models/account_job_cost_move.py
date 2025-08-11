from odoo import api, models, fields

class AccountJobCostMove(models.Model):
   _inherit = 'account.move'

   #appointment_id = fields.Many2one('hospital.appointment', string="Appointment")
   #material_line_ids = fields.One2many('job.costing.material.line', 'cost_sheet_id', string="Job Type Material")
   #job_type_id = fields.Many2one('job.type', string="Job Type", domain="[('job_type', '=', 'material')]")
   cost_sheet_id = fields.Many2one('cost.sheet', string='Cost Sheet Reference', index=True, required=True,
                                    ondelete='cascade')

   @api.onchange('cost_sheet_id')
   def _onchange_cost_sheet_id(self):
      """Auto-fill invoice lines when selecting a Cost Sheet."""
      if self.cost_sheet_id:
         self.invoice_line_ids = [(5, 0, 0)]  # Clear existing lines
         new_lines = []
         for line in self.cost_sheet_id.material_line_ids:  # Assuming this relation exists
            new_lines.append((0, 0, {
               'product_id': line.product_id.id,
               'name': line.description or line.product_id.name,  # Ensure a name is set
               'quantity': line.quantity,
               'price_unit': line.unit_price,
               # 'tax_ids': [(6, 0, line.tax_ids.ids)],
               # 'account_id': line.account_id.id or self.journal_id.default_credit_account_id.id,
            }))

         self.invoice_line_ids = new_lines


class AccountJobCostMoveLine(models.Model):
   _inherit = 'account.move.line'

   remark = fields.Char(string="Remark")
   # cost_sheet_id = fields.Many2one(
   #    'your.cost.sheet.model',
   #    string="Cost Sheet",
   #    related='move_id.cost_sheet_id',
   #    store=True)
