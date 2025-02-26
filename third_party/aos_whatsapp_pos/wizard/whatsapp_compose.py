# See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, sql_db, _
from odoo.tools.mimetypes import guess_mimetype
from datetime import datetime
from odoo.exceptions import UserError
import html2text
import logging

_logger = logging.getLogger(__name__)

class WhatsappComposeMessage(models.TransientModel):
    _inherit = 'whatsapp.compose.message'
    
    pos_order_ids = fields.Many2many('pos.order', string='Pos Order')
    
    @api.model
    def default_get(self, fields):
        is_multi_order = False
        active_model = self.env.context.get('active_model')
        res_id = self.env.context.get('active_id')
        if active_model == 'pos.order':
            res_ids = self.env.context.get('active_ids')
            if len(res_ids) > 1:
                template_id = self.env.ref('aos_whatsapp_pos.pos_sales_confirm_multi', raise_if_not_found=False)
                is_multi_order = True
            else:
                template_id = self.env.ref('aos_whatsapp_pos.pos_sales_confirm_status', raise_if_not_found=False)
        result = super(WhatsappComposeMessage, self.with_context(template=template_id)).default_get(fields)
        if self.env.context.get('active_model') == 'pos.order' and self.env.context.get('active_id'):
            #res_ids = self.env.context.get('active_ids')
            rec = self.env[active_model].browse(res_id)
            result['subject'] = ''
            msg = result.get('message', '')
            if active_model == 'pos.order' and template_id:
                template = template_id.generate_email(rec.id, ['body_html'])
                body = template.get('body_html')
                msg = html2text.html2text(body)
                if not is_multi_order:
                    result['template_id'] = template_id and template_id.id
                    result['subject'] = template_id and template_id.subject
                result['subject'] = result['subject'] or 'Pos Order'
            if is_multi_order:
                result['pos_order_ids'] = res_ids
            result['message'] = msg
        return result
    
                