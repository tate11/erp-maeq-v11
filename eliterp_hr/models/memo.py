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


class HrAppearance(models.Model):
    _name = 'eliterp.hr.appearance'

    _description = 'Aspecto de documento'

    @api.model
    def create(self, vals):
        context = dict(self._context or {})
        if 'default_document_select' in context:
            if context['default_document_select'] == False:
                raise UserError("No puede crear una aspecto sin escoger un documento.")
        return super(HrAppearance, self).create(vals)

    name = fields.Char('Aspecto')
    document_select = fields.Selection([
        ('reglament', 'Reglamento'),
        ('code_work', 'Código de Trabajo')
    ], 'Documento')


class TypeMemorandum(models.Model):
    _name = 'eliterp.type.memorandum'

    _description = 'Tipo de memorandum'

    name = fields.Char('Nombre', required=True)


class TypeMemo(models.Model):
    _name = 'eliterp.type.memo'
    _description = 'Tipo de memorandum'

    @api.multi
    def name_get(self):
        res = []
        for data in self:
            res.append((data.id, "%s - %s " % (data.name.name, data.provision)))
        return res

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        # Para realizar la busquedad por nombre y provision
        if operator in ('=', 'ilike', '=ilike', 'like', '=like'):
            domain = ['|', ('name', operator, name), ('provision', operator, name)]
        args = args or []
        rec = self.search(domain + args, limit=limit)
        return rec.name_get()

    appearance_id = fields.Many2one('eliterp.hr.appearance', 'Aspecto', required=True)
    name = fields.Many2one('eliterp.type.memorandum', 'Tipo', required=True)
    article = fields.Char('Artículo', required=True)
    numeral = fields.Char('Numeral', required=True)
    provision = fields.Text('Disposición', required=True)
    document_select = fields.Selection([
        ('reglament', 'Reglamento'),
        ('code_work', 'Código de Trabajo')
    ], 'Documento', default='reglament', required=True)

    _sql_constraints = [
        ('article_unique', 'unique (article,numeral)', "El artículo y código deben ser únicos.")
    ]


class Memo(models.Model):
    _name = 'eliterp.memo'

    _description = 'Memorandums'

    @api.multi
    def validate(self):
        new_name = self.env['ir.sequence'].next_by_code('hr.memorandum')
        self.write({
            'state': 'validate',
            'name': new_name
        })

    @api.model
    def _get_date_format(self):
        return self.env['eliterp.global.functions'].get_date_format_invoice(self.date)

    @api.multi
    def imprimir_memo(self):
        """
        Imprimimo Memorandums
        """
        self.ensure_one()
        return self.env.ref('eliterp_hr.eliterp_action_report_employee_memo').report_action(self)

    name = fields.Char('No. Documento')
    date = fields.Date('Fecha documento', default=fields.Date.context_today, required=True, readonly=True,
                       states={'draft': [('readonly', False)]})
    type_document = fields.Boolean('Sanción?', default=False, readonly=True,
                                   states={'draft': [('readonly', False)]})
    comment_sanction = fields.Text('Comentario de Sanción', readonly=True,
                                   states={'draft': [('readonly', False)]})
    employee = fields.Many2one('hr.employee', string='Empleado', readonly=True,
                               required=True,
                               states={'draft': [('readonly', False)]})
    document_select = fields.Selection([
        ('reglament', 'Reglamento'),
        ('code_work', 'Código de Trabajo')
    ], 'Documento', default='reglament', required=True, readonly=True,
        states={'draft': [('readonly', False)]})
    appearance_id = fields.Many2one('eliterp.hr.appearance', 'Aspecto', required=True, readonly=True,
                                    states={'draft': [('readonly', False)]})
    type_id = fields.Many2one('eliterp.type.memo', 'Tipo', required=True, readonly=True,
                              states={'draft': [('readonly', False)]})
    state = fields.Selection(STATES, string='Estado', default='draft')
    comment = fields.Text('Notas y comentarios',readonly=True,
                            states={'draft': [('readonly', False)]})
    firme = fields.Many2one('hr.employee', string='Firma', readonly=True,
                            states={'draft': [('readonly', False)]})
    adjunt = fields.Binary('Documento firmado', attachment=True)
    adjunt_name = fields.Char('Nombre')