# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class PosConfig(models.Model):
    _inherit = "pos.config"

    use_posagent = fields.Boolean(string="POS Agent")
    pos_agent_port = fields.Integer(string="Proxy Port", default=9069)
    posagent_enable_printer = fields.Boolean(string="Receipt Printer")
    posagent_enable_cashdrawer = fields.Boolean(string="Cash Drawer")

