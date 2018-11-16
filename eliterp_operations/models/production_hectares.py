# -*- coding: utf-8 -*-
# Copyright 2018 Elitumdevelop S.A, Ing. Mario Rangel
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import models, fields, api
from datetime import datetime
from odoo.exceptions import ValidationError


class ProductioHectares(models.Model):
    _name = 'eliterp.production.hectares'
    _description = 'Producción por hectáreas'
    _order = 'start_date desc'

    @api.depends('start_date')
    def _compute_week(self):
        """
        Obtenemos la semana de la fecha
        """
        if self.start_date:
            object_date = datetime.strptime(self.start_date, "%Y-%m-%d")
            self.name = object_date.isocalendar()[1]

    @api.constrains('start_date', 'end_date')
    def check_dates(self):
        if self.filtered(lambda x: x.start_date > x.end_date):
            raise ValidationError("Error fecha fin no puede ser menor a la de inicio.")

    @api.constrains('hectares')
    def _check_hectares(self):
        if not self.hectares > 0:
            raise ValidationError("Héctareas trabajadas deben ser mayores a 0.")

    name = fields.Char('Semana', compute='_compute_week', store=True)
    start_date = fields.Date('Fecha inicio', required=True)
    end_date = fields.Date('Fecha fin', required=True)
    ubication_id = fields.Many2one('eliterp.location', 'Ubicación', required=True)
    gang_id = fields.Many2one('eliterp.gang', 'Cuadrilla', required=True)
    hectares = fields.Float('Héctareas trabajadas', required=True, digits=(16, 4))
