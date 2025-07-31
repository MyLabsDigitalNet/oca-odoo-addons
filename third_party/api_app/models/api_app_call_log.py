# -*- coding:utf-8 -*-
from odoo import fields, models, api

class ApiAppCallLog(models.Model):
    _name = 'api.app.call.log'
    _description = 'API Call Log'

    user_id = fields.Many2one('res.users', 'User', ondelete='restrict')

    name = fields.Char('API')
    remote_addr = fields.Char('REMOTE_ADDR')
    remote_port = fields.Char('REMOTE_PORT')
    request_method = fields.Char('REQUEST_METHOD')
    path_info = fields.Text('PATH_INFO')
    query_string = fields.Text('QUERY_STRING')
    api_type = fields.Selection([
        ('READ', 'READ'),
        ('CREATE', 'CREATE'),
        ('WRITE', 'WRITE'),
        ('UNLINK', 'UNLINK'),
    ], string='API Type')

