# -*- coding: utf-8 -*-
# Copyright 2018 Elitumdevelop S.A, Ing. Mario Rangel
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import api, models, fields


class StockMoveLine(models.Model):
    _inherit = 'stock.move'

    date_delivery = fields.Date('Fecha de entrega')


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def _create_history_employee(self):
        """
        Creamos los registros de equipos según el inventario
        """

        if self.location_id.employees:
            movement = 'returned'
        else:
            movement = 'delivery'
        object_record_history = self.env['eliterp.lines.uniform.employee']
        for line in self.move_lines:
            product_price = line.product_id.lst_price
            quantity = line.quantity_done
            total = product_price * quantity
            object_record_history.create({
                'employee_id': self.employee_id.id,
                'date': line.date_delivery if line.date_delivery else self.scheduled_date,
                'movement': movement,
                'category': line.product_id.categ_id.name,
                'article': line.product_id.name,
                'product_price': product_price,
                'quantity': line.quantity_done,
                'total': total
            })

    @api.multi
    def action_done(self):
        """
        SM: Para crear líneas de equipos entregados a empleado
        """
        res = super(StockPicking, self).action_done()
        if self.show_employee:
            self._create_history_employee()
        return res

    @api.depends('location_id', 'location_dest_id')
    @api.one
    def _get_parameter(self):
        """
        Mostramos empleado o no
        """
        self.show_employee = self.location_id.employees or self.location_dest_id.employees

    @api.multi
    def print_picking(self):
        """
        Imprimimo operación de bodega
        """
        self.ensure_one()
        if self.picking_type_code == 'outgoing':  # Egreso
            return self.env.ref('eliterp_inventory.eliterp_action_report_stock_picking_egre').report_action(self)
        elif self.picking_type_code == 'incoming':  # Ingreso
            return self.env.ref('eliterp_inventory.eliterp_action_report_stock_picking_ingr').report_action(self)
        else:  # Transferencia
            return self.env.ref('eliterp_inventory.eliterp_action_report_stock_picking_trans').report_action(self)

    employee_id = fields.Many2one('hr.employee', string='Empleado')
    show_employee = fields.Boolean('Mostrar', compute='_get_parameter')
