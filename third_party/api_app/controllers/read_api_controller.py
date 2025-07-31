# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
import re
from datetime import date, datetime
from odoo.addons.api_app.utils.api_call_log import api_call_log_save
import ast


class ReadApiController(http.Controller):
    @http.route('/api_app/read_data', type='json', auth='user', csrf=False, methods=['POST'])
    def read_data(self, **kw):

        for key, value in kw.items():
            if not re.match(r'^[a-z_]+$', key):
                return {
                    'response': 'ERROR',
                    'data_received': "Please provide a valid parameter list (only lowercase letters and underscores are allowed)"
                }

        api_call_log_save(request,api_type = 'READ')

        model_alias = kw.get('model_alias')
        offset = kw.get('offset')
        limit = kw.get('limit')
        if model_alias is None:
            return {
                'response': 'ERROR',
                'data_received': "'model_alias' is required Field!"
            }

        if offset is not None and  limit is not None:
            # Validate positive integers
            try:
                offset = int(offset)
                limit = int(limit)
                if offset < 0 or limit <= 0:
                    raise ValueError
            except (ValueError, TypeError):
                return {
                    'response': 'ERROR',
                    'data_received': "'offset' must be >= 0 and 'limit' must be > 0 (positive integers only)."
                }
        else:
            offset = None
            limit = None


        api_search = request.env['api.app.read'].sudo().search([('model_alias','=',model_alias)], limit=1)

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

        order_by_field_list = []
        for order_by_field in api_search.orderby_ids:
            order_by_field_list.append(order_by_field.field_name.name)

        allow_field_list = []
        for allow_field in api_search.allow_field_ids:
            allow_field_list.append(allow_field.field_name.name)

        model_name = api_search.model_name.model
        default_limit = limit or api_search.default_limit
        default_offset = offset or api_search.default_offset

        filter_list = []

        # Append Default Filter List
        for allow_filter in api_search.default_filter_ids:
            try:
                # Try to evaluate literal types (int, float, list, dict, bool, None)
                filter_list.append((allow_filter.field_name.name, allow_filter.comparison_operator, ast.literal_eval(allow_filter.field_value)))
            except (ValueError, SyntaxError):
                aaa = 10


        # Now append user filter list
        for key, value in kw.items():
            if key not in ['model_name','limit','offset']:
                for allow_filter in api_search.user_filter_ids:
                    if key == allow_filter.field_name.name:
                        filter_list.append((key,allow_filter.comparison_operator,value))

        model_data_ser = request.env[model_name].sudo().search_read(filter_list,allow_field_list, limit=default_limit, offset=default_offset, order= (','.join(order_by_field_list)) )

        if model_data_ser:
            return {
                'response': 'OK',
                'data_received': model_data_ser
            }
        else:
            return {
                'response': 'OK',
                'data_received': []
            }
