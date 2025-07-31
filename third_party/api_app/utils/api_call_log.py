
def api_call_log_save(request, api_type='READ'):
    try:
        http_request = getattr(request, 'httprequest', None)
        if http_request:
            environ = http_request.environ
            query_data = ''
            try:
                query_data = str(http_request.json or '')
            except Exception:
                query_data = str(http_request.params or {})

            values = {
                'user_id': request.env.user.id or False,
                'name': request.params.get('model_alias', ''),
                'remote_addr': environ.get('REMOTE_ADDR', ''),
                'remote_port': environ.get('REMOTE_PORT', ''),
                'request_method': environ.get('REQUEST_METHOD', ''),
                'path_info': environ.get('PATH_INFO', ''),
                'query_string': query_data,
                'api_type': api_type,
            }
        else:
            values = {
                'user_id': request.env.user.id or False,
                'name': request.params.get('model_alias', ''),
                'remote_addr': 'NO_HTTPREQUEST',
                'remote_port': '',
                'request_method': '',
                'path_info': '',
                'query_string': 'httprequest not available in request',
                'api_type': api_type,
            }

        request.env['api.app.call.log'].sudo().create(values)

    except Exception as e:
        request.env['api.app.call.log'].sudo().create({
            'user_id': request.env.user.id or False,
            'name': request.params.get('model_alias', ''),
            'remote_addr': 'EXCEPTION',
            'remote_port': '',
            'request_method': '',
            'path_info': '',
            'query_string': f"Exception Found: {str(e)}",
            'api_type': api_type,
        })
