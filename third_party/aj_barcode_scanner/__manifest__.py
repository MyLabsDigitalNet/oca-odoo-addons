# -*- coding: utf-8 -*-
{
    'name': "aj_barcode_scanner",

    'summary': """
        scan products barcode by camera and add to cart in point of sale""",

    'description': """
        scan products barcode by camera and add to cart in point of sale
    """,

    'author': "Abdullah Jaber",

    'category': 'Uncategorized',
    'version': '1.0',
    'license': 'OPL-1',

    # any module necessary for this one to work correctly
    'depends': [ 'point_of_sale'],

    'assets': {
        'point_of_sale.assets': [
            'aj_barcode_scanner/static/src/js/scan_barcode_button.js',
            'aj_barcode_scanner/static/src/xml/scan_barcode_button.xml',
            'aj_barcode_scanner/static/src/js/html5-qrcode.min.js',
            'aj_barcode_scanner/static/src/css/scanner.css',
        ]
    },
    'images': ['static/description/main_screenshot.png'],



}
