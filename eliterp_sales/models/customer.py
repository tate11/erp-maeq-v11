# -*- coding: utf-8 -*-
# Copyright 2018 Elitumdevelop S.A, Ing. Mario Rangel
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.onchange('property_account_receivable_id')
    def _onchange_property_account_receivable_id(self):
        """
        Le colocamos cuentas por defecto del plan de cuentas
        :return: self
        """
        return

    origen_income = fields.Selection([('b', 'Empleado Público'),
                                      ('v', 'Empleado Privado'),
                                      ('i', 'Independiente'),
                                      ('a', 'Ama de casa o Estudiante'),
                                      ('r', 'Rentista'),
                                      ('h', 'Jubilado'),
                                      ('m', 'Remesas del exterior'), ], string='Origen de ingreso')
    client_type = fields.Selection([
        ('ct_1', 'MAEQ AAA'),
        ('ct_2', 'MAEQ AA'),
        ('ct_3', 'MAEQ A'),
        ('ct_4', 'MAEQ BBB'),
        ('ct_5', 'MAEQ BB'),
        ('ct_6', 'MAEQ B')
    ], string='Tipo de cliente', default='ct_1')
    client_segmentation = fields.Selection([
        ('cs_1', 'Agroindustrial'),
        ('cs_2', 'Bananero'),
        ('cs_3', 'Camaronero'),
        ('cs_4', 'Construcción'),
        ('cs_5', 'Intermediario'),
        ('cs_6', 'Servicios'),
        ('cs_7', 'Sector Público'),
        ('cs_8', 'Financiero'),
        ('cs_9', 'Palma')],
        string='Segmentación de cliente', default='cs_1')
    type_seller = fields.Selection([('consultant', 'Asesor'), ('freelance', 'FreeLance')], 'Tipo de vendedor',
                                   default='consultant')
    freelance_id = fields.Many2one('res.partner', string='Freelance')
    is_contact = fields.Boolean('Es contacto?')
    credit_limit = fields.Float('Cupo de crédito')
    if_freelance = fields.Boolean('FreeLance')
    consultant_id = fields.Many2one('hr.employee', string='Asesor')

    property_account_receivable_id = fields.Many2one('account.account',
                                                     string='Cuenta a cobrar',
                                                     domain=[('account_type', '=', 'movement')])
