# -*- coding: utf-8 -*-
# Copyright 2018 Elitumdevelop S.A, Ing. Mario Rangel
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).


from odoo import fields, models


class StockLocation(models.Model):
    _inherit = 'stock.location'

    employees = fields.Boolean('¿Es bodega para Empleados?', default=False)
