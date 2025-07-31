# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
import re
from datetime import date, datetime
from odoo.addons.api_app.utils.api_call_log import api_call_log_save


class CreateApiController(http.Controller):
    @http.route('/api_app/create_data', type='json', auth='user', csrf=False, methods=['POST'])
    def create_data(self, **kw):

        for key, value in kw.items():
            if not re.match(r'^[a-z_]+$', key):
                return {
                    'response': 'ERROR',
                    'data_received': "Please provide a valid parameter list (only lowercase letters and underscores are allowed)"
                }

        api_call_log_save(request,api_type = 'CREATE')

        model_alias = kw.get('model_alias')
        if model_alias is None:
            return {
                'response': 'ERROR',
                'data_received': "['model_alias'] is required Field!"
            }

        api_search = request.env['api.app.write'].sudo().search([('model_alias','=',model_alias)], limit=1)

        if not api_search:
            return {
                'response': 'ERROR',
                'data_received': "Provided 'model_alias' not found, please provide a valid model_alias."
            }

        if not request.env.user.id in api_search.allowed_user_list.ids:
            return {
                'response': 'ERROR',
                'data_received': "This API is not allowed to your user!"
            }

        if api_search.api_expiry_date < date.today():
            return {
                'response': 'ERROR',
                'data_received': "This API is expired!"
            }

        model_name = api_search.model_name.model

        data_dict = {}
        for key, value in kw.items():
            if key not in ['model_name','limit','offset']:
                for allow_field in api_search.allowed_field_list:
                    if key == allow_field.name:
                        data_dict[key] = value

        create_record = request.env[model_name].sudo().create(data_dict)
        if create_record:
            return {
                'response': 'OK',
                'data_received': 'CREATED SUCCESSFULLY',
                'id': create_record.id
            }
        else:
            return {
                'response': 'ERROR',
                'data_received': 'No record found with given id!'
            }

