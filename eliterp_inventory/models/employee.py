# -*- coding: utf-8 -*-
# Copyright 2018 Elitumdevelop S.A, Ing. Mario Rangel
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import fields, models


class LinesUniformEmployee(models.Model):
    _name = 'eliterp.lines.uniform.employee'

    _description = 'Líneas de uniforme de empleado'

    movement = fields.Selection([('delivery', 'Entrega'),
                                 ('returned', 'Devuelto')], 'Movimiento', default='delivery')
    date = fields.Date('Fecha de registro', required=True)
    article = fields.Text('Producto')
    quantity = fields.Integer('Cantidad')
    employee_id = fields.Many2one('hr.employee', string='Empleado')
    category = fields.Text('Categoria')
    product_price = fields.Float('Precio')
    quantity = fields.Float('Cantidad')
    total = fields.Float('Total')
    select = fields.Boolean('Imprimir?')
    adjunt = fields.Binary('Documento', attachment=True)
    adjunt_name = fields.Char('Nombre')


class Employee(models.Model):
    _inherit = 'hr.employee'

    uniform_history = fields.One2many('eliterp.lines.uniform.employee', 'employee_id', string='Uniformes de empleado')
