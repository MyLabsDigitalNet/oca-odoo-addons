# -*- coding:utf-8 -*-
from odoo import fields, models, api
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError
import re
import json

class ApiAppRead(models.Model):
    _name = 'api.app.read'
    _description = 'Read API'
    # _rec_name = 'model_name'


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

    default_limit = fields.Char('Default Limit', default='10')
    default_offset = fields.Char('Default Offset', default='0')

    final_url = fields.Html('Final URI', compute='_compute_final_url')

    state = fields.Selection([
        ('Active', 'Active'),
        ('In-Active', 'In-Active'),
        ], default='Active', string='State')
    is_api_active = fields.Boolean(compute="_check_api_expiry_date")

    user_filter_ids = fields.One2many('api.app.read.user.filter', 'read_api_id','User Filters')
    default_filter_ids = fields.One2many('api.app.read.default.filter', 'read_api_id','Default Filters')
    allow_field_ids = fields.One2many('api.app.read.allow.field', 'read_api_id','Allow Fields')
    orderby_ids = fields.One2many('api.app.read.orderby', 'read_api_id','Order By Fields')

    allowed_user_list = fields.Many2many('res.users', 'api_app_read_allowed_user_list_rel',
                               string='Allowed Users')


    _sql_constraints = [
        ('api_app_read_unique_model_alias', 'unique(model_alias)', 'Model Alias must be unique!')
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
                "model_alias": record.model_alias,
                "offset": 0,
                "limit": 20
            })
            # Add Dynamic filters
            for allow_filter in record.user_filter_ids:
                field = allow_filter.field_name.name
                if field:
                    default_value = ""
                    if allow_filter.field_name.ttype == 'boolean':
                        default_value = True
                    elif allow_filter.field_name.ttype == 'integer':
                        default_value = 0
                    elif allow_filter.field_name.ttype =='float':
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
<p>Then Read the data:<br /></p>
<pre>
curl --location '{base_url}/api_app/read_data' \\
--header 'Content-Type: application/json' \\
--data '{filter_json}'
</pre>
    """


class ApiAppReadUserFilter(models.Model):
    _name = 'api.app.read.user.filter'
    _description = 'Read API User Filter'

    read_api_id = fields.Many2one('api.app.read', string='Read API ID')

    @api.onchange('model_name')
    def _get_model_name_default(self):
        if self.read_api_id.model_name:
            model_name = self.read_api_id.model_name
            self.model_name = model_name
    model_name = fields.Many2one('ir.model', string='Model Name', store=True )
    field_name = fields.Many2one('ir.model.fields', string='Field Name')
    field_alias = fields.Char('Field Alias')
    comparison_operator = fields.Selection(
        [
            ('=', '='),
            ('!=', '!='),
            ('>', '>'),
            ('>=', '>='),
            ('<', '<'),
            ('<=', '<='),
            ('ilike', 'ilike'),
            ('not ilike', 'not ilike'),
        ], required=True, string='Operator', default='ilike')
    dot_variable = fields.Char('Dot Variable')
    sequence = fields.Integer('Sequence')

class ApiAppReadDefaultFilter(models.Model):
    _name = 'api.app.read.default.filter'
    _description = 'Read API Default Filter'

    read_api_id = fields.Many2one('api.app.read', string='Read API ID')

    @api.onchange('model_name')
    def _get_model_name_default(self):
        if self.read_api_id.model_name:
            model_name = self.read_api_id.model_name
            self.model_name = model_name
    model_name = fields.Many2one('ir.model', string='Model Name', store=True )
    field_name = fields.Many2one('ir.model.fields', string='Field Name')
    comparison_operator = fields.Selection(
        [
            ('=', '='),
            ('!=', '!='),
            ('>', '>'),
            ('>=', '>='),
            ('<', '<'),
            ('<=', '<='),
            ('ilike', 'ilike'),
            ('not ilike', 'not ilike'),
        ], required=True, string='Operator', default='ilike')
    field_value = fields.Char('Field Value', required=True)
    dot_variable = fields.Char('Dot Variable')
    sequence = fields.Integer('Sequence')

class ApiAppReadAllowField(models.Model):
    _name = 'api.app.read.allow.field'
    _description = 'Read API Allow Fields'

    read_api_id = fields.Many2one('api.app.read', string='Read API ID')

    @api.onchange('model_name')
    def _get_model_name_default(self):
        if self.read_api_id.model_name:
            model_name = self.read_api_id.model_name
            self.model_name = model_name
    model_name = fields.Many2one('ir.model', string='Model Name', store=True )
    field_name = fields.Many2one('ir.model.fields', string='Field Name')
    field_alias = fields.Char('Field Alias')
    null_default_value = fields.Char('Null Default Value')
    dot_variable = fields.Char('Dot Variable')
    sequence = fields.Integer('Sequence')

class ApiAppReadOrderBy(models.Model):
    _name = 'api.app.read.orderby'
    _description = 'Read API Order By'

    read_api_id = fields.Many2one('api.app.read', string='Read API ID')
    @api.onchange('model_name')
    def _get_model_name_default(self):
        model_name = None
        if self.read_api_id.model_name:
            model_name = self.read_api_id.model_name
            self.model_name = model_name
    model_name = fields.Many2one('ir.model', string='Model Name', store=True )
    field_name = fields.Many2one('ir.model.fields', string='Field Name')
    sequence = fields.Integer('Sequence')
