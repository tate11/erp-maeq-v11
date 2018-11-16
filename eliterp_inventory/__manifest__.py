# -*- coding: utf-8 -*-
# Copyright 2018 Elitumdevelop S.A, Ing. Mario Rangel
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

{
    'name': "Módulo de Inventario",
    'summary': "Inventario.",
    'author': "Ing. Mario Rangel, Elitumgroup S.A",
    'website': "http://www.elitumgroup.com",
    'category': "Personalization",
    'license': "LGPL-3",
    'version': "1.0",
    'depends': [
        'base',
        'eliterp_management',
        'stock',
        'hr',
        'eliterp_hr'
    ],
    'data': [
        'security/ir.model.access.csv',
        'reports/reports_views.xml',
        'reports/inventory_reports.xml',
        'views/product_views.xml',
        'views/stock_location_views.xml',
        'views/stock_picking_views.xml',
        'views/employee_views.xml',
        'views/dashboard.xml',
    ],
    'init_xml': [],
    'update_xml': [],
    'installable': True,
    'active': False,
}
