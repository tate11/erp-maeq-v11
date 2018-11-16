# -*- coding: utf-8 -*-
# Copyright 2018 Elitumdevelop S.A, Ing. Mario Rangel
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from collections import defaultdict
import pytz
from datetime import time, datetime, timedelta
from odoo import api, fields, models
import math


class ProductReportPdf(models.AbstractModel):
    _name = 'report.eliterp_inventory.eliterp_report_product_report'

    @staticmethod
    def _get_type(type):
        """
        Tipo de producto
        :return: string
        """
        data = ''
        if type == 'consu':
            data = 'CONSUMIBLE'
        elif type == 'service':
            data = 'SERVICIO'
        else:
            data = 'ALMACENABLE'
        return data

    def _get_lines(self, doc):
        """
        Obtenemos líneas de reporte
        :param doc:
        :return: list
        """
        data = []
        arg = []
        if doc.type == 'purchase':
            arg.append(('purchase_ok', '=', True))
        if doc.type == 'sale':
            arg.append(('sale_ok', '=', True))
        if doc.category != 'all':
            arg.append(('categ_id', '=', doc.category_id.id))
        products = self.env['product.template'].search(arg)
        for product in products.sorted(key=lambda r: r.categ_id.name):
            data.append({
                'type': self._get_type(product.type),
                'category': product.categ_id.name,
                'name': product.name,
                'code': product.default_code,
                'account_expense': product.categ_id.property_account_expense_categ_id.code + " " +  product.categ_id.property_account_expense_categ_id.name if product.categ_id.property_account_expense_categ_id else '-',
                'account_income': product.categ_id.property_account_income_categ_id.code + " " + product.categ_id.property_account_income_categ_id.name if product.categ_id.property_account_income_categ_id else '-',
                'uom': product.uom_id.name,
                'uom_purchase': product.uom_po_id.name,
                'price': product.list_price if product.list_price > 0 else '-',
                'price_purchase': product.standard_price if product.standard_price > 0 else '-'
            })
        return data

    @api.model
    def get_report_values(self, docids, data=None):
        return {
            'doc_ids': docids,
            'doc_model': 'eliterp.product.report',
            'docs': self.env['eliterp.product.report'].browse(docids),
            'get_lines': self._get_lines,
            'data': data,
        }


class ProductReport(models.TransientModel):
    _name = 'eliterp.product.report'

    _description = "Ventana para reporte de productos"

    @api.multi
    def print_report_xlsx(self):
        """
        Imprimimos reporte en xlsx
        """
        self.ensure_one()
        return self.env.ref('eliterp_inventory.eliterp_action_report_product_xlsx').report_action(self)

    @api.multi
    def print_report_pdf(self):
        """
        Imprimimos reporte en pdf
        """
        self.ensure_one()
        return self.env.ref('eliterp_inventory.eliterp_action_report_product_report').report_action(self)

    type = fields.Selection([
        ('all', 'Todos'),
        ('purchase', 'Para comprar'),
        ('sale', 'Para vender')
    ], default='all', string='Tipo', required=True)
    category = fields.Selection([
        ('all', 'Todas'),
        ('one', 'Invidual')
    ], default='all', string='Tipo de categoría', required=True)
    category_id = fields.Many2one('product.category', 'Categoría')