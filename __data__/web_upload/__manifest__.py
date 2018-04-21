{
    'name': 'Multi Upload Files',
    'sequence': 3,
    'version': '1.0',
    'summary': 'Upload Multi Files',
    'category': 'Backend',
    'author': 'Bruce',
    'description':
        """
        Click drag, drop file to Odoo, odoo browse will be trigger upload files you need.
        """,
    'data': [
        'import/import_js.xml',
    ],
    'depends': [
        'document'
    ],
    'price': '50',
    'currency': 'USD',
    'qweb': ['static/src/xml/*.xml'],
    'application': True,
    'price': '0',
    'currency': 'USD',
}