# -*- coding: utf-8 -*-
# Copyright 2018 Elitumdevelop S.A, Ing. Mario Rangel
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import models, fields, api
from odoo.exceptions import UserError

STATES = [
    ('draft', 'Borrador'),
    ('validate', 'Validado'),
    ('cancel', 'Anulado')
]


class ResignationEmployment(models.Model):
    _name = 'eliterp.resignation.employment'

    _description = 'Renuncia'

    @api.multi
    def validate(self):
        new_name = self.env['ir.sequence'].next_by_code('hr.resignation')
        self.write({
            'state': 'validate',
            'name': new_name
        })

    @api.model
    def _get_date_format(self):
        return self.env['eliterp.global.functions'].get_date_format_invoice(self.date)

    @api.multi
    def imprimir_resignation_employment(self):
        """
        Imprimimo renuncia
        """
        self.ensure_one()
        return self.env.ref('eliterp_hr.eliterp_action_report_resignation_employment').report_action(self)

    date = fields.Date('Fecha documento', default=fields.Date.context_today, required=True, readonly=True,
                       states={'draft': [('readonly', False)]})
    name = fields.Char('No. Documento')
    employee = fields.Many2one('hr.employee', string='Empleado', readonly=True,
                               required=True,
                               states={'draft': [('readonly', False)]})
    identification_id = fields.Char(related='employee.identification_id', string='No. identificación')
    job = fields.Many2one('hr.job', related='employee.job_id', string='Cargo')
    state = fields.Selection(STATES, string='Estado', default='draft')