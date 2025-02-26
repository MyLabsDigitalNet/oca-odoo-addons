# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime
from uuid import uuid4
import pytz

from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError, UserError

class PosSession(models.Model):
    _inherit = 'pos.session'
    
    def _loader_params_res_partner(self):
        vals = super(PosSession, self)._loader_params_res_partner()
        vals['search_params']['fields'] += ['whatsapp'] 
        return vals
        
class PosConfig(models.Model):
    _inherit = 'pos.config'
    
    show_order = fields.Boolean('Show Order', default=True)
    show_limit = fields.Integer('Show Limit', default=10)
    pos_session_limit = fields.Selection([('all',  "Load all Session's Orders"), 
                                          ('last3', "Load last 3 Session's Orders"), 
                                          ('last5', " Load last 5 Session's Orders"),
                                          ('current_day', "Only Current Day Orders"), 
                                          ('lasto',  "Load last Orders"), 
                                          ('current_session', "Only Current Session's Orders")], 
                string='Session limit',default="current_day")
    whatsapp_default_message = fields.Text('Default Whatsapp Message', default="Dear *_CUSTOMER_*, Here is your electronic ticket for the ")
    whatsapp_server_id = fields.Many2one(
        'ir.whatsapp_server',
        string='Whatsapp Server',
        required=False,
        ondelete='restrict')
