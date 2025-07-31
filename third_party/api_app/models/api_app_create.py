# -*- coding:utf-8 -*-
from odoo import fields, models, api
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError
import re
import json

class ApiAppCreate(models.Model):
    _name = 'api.app.create'
    _description = 'Create API'

    name = fields.Char('API Name')
    sequence = fields.Integer('Sequence')
    model_name = fields.Many2one('ir.model', string='Model Name')
    model_alias = fields.Char('Model Alias', required=True)
    @api.constrains('model_alias')
    def _check_model_alias_lowercase(self):
        for record in self:
            if not re.fullmatch(r'[a-z_]+', record.model_alias or ''):
                raise ValidationError("Model Alias must contain only lowercase letters (a-z) and underscores (_).")

    api_expiry_date = fields.Date('Expiry Date', default=datetime.now() + relativedelta(months=1))
    description = fields.Text('Description')

    final_url = fields.Html('Request Sample', compute='_compute_final_url')

    state = fields.Selection([
        ('Active', 'Active'),
        ('In-Active', 'In-Active'),
        ], default='Active', string='State')
    is_api_active = fields.Boolean(compute="_check_api_expiry_date")

    allowed_field_list = fields.Many2many('ir.model.fields', 'api_app_create_allowed_field_list_rel',
                               string='Allowed Fields')

    allowed_user_list = fields.Many2many('res.users', 'api_app_create_allowed_user_list_rel',
                               string='Allowed Users')

    _sql_constraints = [
        ('api_app_create_unique_model_alias', 'unique(model_alias)', 'Model Alias must be unique!')
    ]

    def _check_api_expiry_date(self):
        for record in self:
            if record.api_expiry_date < date.today():
                record.is_api_active = False
            else:
                record.is_api_active = True

    def _compute_final_url(self):
        for record in self:
            base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
            db_name = self.env.cr.dbname

            # Build the filter dictionary
            filter_dict = {}
            # Add static filter
            filter_dict.update({
                "model_alias": record.model_alias
            })
            # Add Dynamic filters
            for field_name in record.allowed_field_list:
                field = field_name.name
                if field:
                    default_value = ""
                    if field_name.ttype == 'boolean':
                        default_value = True
                    elif field_name.ttype == 'integer':
                        default_value = 0
                    elif field_name.ttype == 'float':
                        default_value = 0.0
                    filter_dict[field] = default_value

            # Convert to proper JSON string
            filter_json = json.dumps({
                "jsonrpc": "2.0",
                "params": filter_dict
            }, indent=2)

            # Authentication payload
            auth_json = json.dumps({
                "jsonrpc": "2.0",
                "params": {
                    "login": "apiUser",
                    "password": "12345",
                    "db": db_name
                }
            }, indent=2)

            # Set final_url
            record.final_url = f"""
<p>First Authenticate the user (if not already authenticated):<br /></p>
<pre>
curl --location '{base_url}/web/session/authenticate' \\
--header 'Content-Type: application/json' \\
--data '{auth_json}'
</pre>
<p>Then Call:<br /></p>
<pre>
curl --location '{base_url}/api_app/create_data' \\
--header 'Content-Type: application/json' \\
--data '{filter_json}'
</pre>
    """
