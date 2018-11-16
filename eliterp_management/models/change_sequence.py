# -*- coding: utf-8 -*-
# Copyright 2018 Elitumdevelop S.A, Ing. Mario Rangel
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models


class ChangeSequence(models.Model):
    _name = 'eliterp.change.sequence'
    _description = 'Cambiar secuencia de documentos'

    @api.multi
    def change_sequence(self):
        """
        Realizamos la operación para cambiar
        :return:
        """
        table = self.model_id.model
        order_by = '%s %s' % (self.sorty_by.name, self.type_ordering)
        records = self.env[table].search([], order=order_by)
        for register in records:
            new_name = self.env['ir.sequence'].next_by_code(self.sequence_id.code)  # Nueva secuencia
            register.update({'%s' % self.field_change.name: new_name})

    name = fields.Char('Nombre', default='Cambio')
    model_id = fields.Many2one('ir.model', 'Modelo', required=True, domain=[('transient', '=', False)])
    sequence_id = fields.Many2one('ir.sequence', 'Secuencia de cambio', required=True)
    sorty_by = fields.Many2one('ir.model.fields', 'Ordenar por', help="Campos de tipo fecha y fecha y hora.")
    field_change = fields.Many2one('ir.model.fields', 'Campo a cambiar', required=True)
    type_ordering = fields.Selection([('asc', 'Ascendente'), ('desc', 'Descendiente')], default='asc',
                                     string='Tipo de ordenamiento')
