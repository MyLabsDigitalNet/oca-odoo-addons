# -*- coding: utf-8 -*-

{
    'name': 'POSAgent for Community Edition Direct Print Cash Drawer',
    'version': '1.0',
    'author' : 'Diego A.',
    'support' : 'diegoandino@gmail.com',
    'category': 'Sales/Point of Sale',
    'sequence': 6,
    'summary': 'POSAgent support for the Point of Sale',
    'description': """

This module enables the use of PosAgent as an alternative proxy service to interface with POS hardware
Get PosAgent from this GitHub site: https://github.com/dieg0-a/posagentpro
""",
    'depends': ['point_of_sale'],
    'data': [
        'views/pos_config_views.xml',
    ],
    "images": ['static/images/thumbnail.png'],
    'installable': True,
#    'auto_install': True,
    'assets': {
        'point_of_sale._assets_pos': [
            'pos_posagent/static/src/**/*',
        ],
    },
    'license': 'LGPL-3',
}
