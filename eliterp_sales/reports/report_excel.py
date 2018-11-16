# -*- coding: utf-8 -*-
# Copyright 2018 Elitumdevelop S.A, Ing. Mario Rangel
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import models


class SalesOrder(models.AbstractModel):
    _name = 'report.eliterp_sales.eliterp_sales_invoice_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, records):
        for record in records:
            sheet = workbook.add_worksheet('Factura de venta')
            # Formatos
            money_format = workbook.add_format({'num_format': '$ #,##0.00'})
            date_format = workbook.add_format({'num_format': 'dd-mm-yyyy', 'bold': 1})
            bold = workbook.add_format({'bold': 1})
            # Columnas
            sheet.set_margins (left = 0.05,right = 0.05)
            sheet.set_column("A:A", 7.71)
            sheet.set_column("B:B", 3.43)
            sheet.set_column("C:C", 3)
            sheet.set_column("D:D", 35)
            sheet.set_column("E:E", 16.57)
            sheet.set_column("F:F", 14)
            sheet.set_column("G:G", 3.57)
            sheet.set_column("H:H", 12.71)
            # Filas
            sheet.set_default_row(15)
            sheet.set_row(0, 102)
            sheet.set_row(1, 12)
            sheet.set_row(2, 17.25)
            sheet.set_row(3, 1.75)
            sheet.set_row(4, 17.00)
            sheet.set_row(5, 1.5)
            sheet.set_row(6, 14.25)
            sheet.set_row(7, 23.25)
            sheet.set_row(8, 18.75)
            sheet.set_row(37, 12)
            sheet.set_row(38, 15.75)
            # Datos
            sheet.write(2, 2, record.partner_id.name)
            sheet.write(2, 5, record.date_invoice, date_format)
            sheet.write(4, 2, record.partner_id.street)
            sheet.write(6, 1, record.partner_id.documentation_number)
            sheet.write(6, 7, 'X')
            row = 9
            for line in record.invoice_line_ids:
                sheet.merge_range(row, 0, row, 1, round(line.quantity, 2))
                sheet.write(row, 3, line.name)
                sheet.write(row, 5, line.price_unit, money_format)
                sheet.write(row, 7, line.price_subtotal, money_format)
                row += 1
            sheet.write(23, 3, record.comment if record.comment else '')
            sheet.write(34, 5, 'Subtotal')
            sheet.write(36, 5, 'Impuesto')
            sheet.write(34, 7, record.amount_untaxed, money_format)
            sheet.write(36, 7, record.amount_tax, money_format)
            sheet.write(38, 7, record.amount_total, money_format)

