from odoo import models, fields, api
from odoo.exceptions import ValidationError

class JobType(models.Model):
    _name = 'job.type'
    _inherit = ['mail.thread']
    _description = 'Job Type'
    _sql_constraints = [
        ('unique_code', 'unique(code)', 'The code must be unique!')  # SQL Constraint for uniqueness
    ]

    name = fields.Char(string="Job Type Name", required=True, tracking=True)
    code = fields.Char(string="Code", required=True, tracking=True)
    job_type = fields.Selection([
        ('material', 'Material'),
        ('labour', 'Labour'),
        ('overhead', 'Overhead')
    ], string="Job Type", required=True, tracking=True)

    @api.constrains('code')
    def _check_unique_code(self):
        for record in self:
            if record.code and self.search_count([('code', '=', record.code), ('id', '!=', record.id)]) > 0:
                raise ValidationError("The code must be unique!")
    # from odoo import api, models, fields
    #
    # class HospitalPatient(models.Model):
    #     _name = 'hospital.patient'
    #     _inherit = ['mail.thread']
    #     _description = 'Patient Master'
    #
    #     name = fields.Char(
    #         string="Name", required=True, tracking=True
    #     )
        # date_of_birth = fields.Date(string="Date of Birth")
        # description = fields.Text(string="Description")
        # gender = fields.Selection(
        #     [('male', 'Male'), ('female', 'Female')],
        #     string="Gender"
        # )
        #
        # tag_ids = fields.Many2many(
        #     'patient.tag', 'patient_tag_rel', 'patient_id', 'tag_id', string="Tags"
        # )
        #
        # product_ids = fields.Many2many(
        #     'product.product', string="Products"
        # )

