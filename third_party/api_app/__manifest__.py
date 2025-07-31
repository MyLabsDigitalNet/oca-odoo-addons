# -*- coding: utf-8 -*-
{
    "name": "REST API App",
    "version": "1.0",
    "category": "Tools",
    'sequence': 215,
    "summary": """
    This module enables seamless communication with the Odoo database via RESTful API requests. 
    It is designed for developers and integrators who need secure, configurable, and dynamic access to Odoo models and records.
    """,
    'website': "https://www.zalinotech.com",
    'author': 'Zalino Tech (Private) Limited',
    'company': 'Zalino Tech',
    'maintainer': 'Zalino Tech',
    "description": """This module enables seamless communication with the Odoo database via RESTful API requests. It is designed for developers and integrators who need secure, configurable, and dynamic access to Odoo models and records.

Key Features
------------

- ✅ Dynamic API creation for any Odoo model or database table
- ✅ Access control for specific users or user groups
- ✅ Fine-grained permissions (Read / Write / Create / Unlink) per record and user
- ✅ Secure API endpoints for database operations
- ✅ Event logging to track API activity for audit and monitoring

    """,
    "depends": ['base'],
    "data": [
        'security/ir.model.access.csv',
        'views/api_app_read.xml',
        'views/api_app_write.xml',
        'views/api_app_create.xml',
        'views/api_app_unlink.xml',
        'views/api_app_call_log.xml',
    ],

    'images': ['static/description/banner.jpg'],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': True,
}
