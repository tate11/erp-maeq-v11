# -*- coding: utf-8 -*-
# Copyright 2018 Elitumdevelop S.A, Ing. Mario Rangel
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import models
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError
import math

UNIDADES = (
    '', 'Un ', 'Dos ', 'Tres ', 'Cuatro ', 'Cinco ', 'Seis ', 'Siete ', 'Ocho ', 'Nueve ', 'Diez ', 'Once ',
    'Doce ',
    'Trece ', 'Catorce ', 'Quince ', 'Dieciséis ', 'Diecisiete ', 'Dieciocho ', 'Diecinueve ', 'Veinte ')
DECENAS = ('Veinti', 'Treinta ', 'Cuarenta ', 'Cincuenta ', 'Sesenta ', 'Setenta ', 'Ochenta ', 'Noventa ', 'Cien ')
CENTENAS = (
    'Ciento ', 'Doscientos ', 'Trescientos ', 'Cuatrocientos ', 'Quinientos ', 'Seiscientos ', 'Setecientos ',
    'Ochocientos ', 'Novecientos ')


class ConsolidatedRole(models.AbstractModel):
    _name = 'report.eliterp_hr.eliterp_report_payslip_run_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, records):
        for record in records:
            sheet = workbook.add_worksheet('Rol Consolidado')
            # Formatos
            _right_format = workbook.add_format({'align': 'right', 'num_format': '$#,##0.00'})
            title = workbook.add_format({
                'bold': True,
                'border': 1,
                'align': 'center'
            })
            # Columnas
            sheet.set_column("A:A", 36)
            sheet.set_column("B:B", 10.30)
            sheet.set_column("C:C", 3.90)
            sheet.set_column("D:D", 10)
            sheet.set_column("E:E", 7)
            sheet.set_column("F:F", 5)
            sheet.set_column("G:G", 5)
            sheet.set_column("H:H", 7.14)
            sheet.set_column("I:I", 7.14)
            sheet.set_column("J:J", 9.14)
            sheet.set_column("K:K", 9.14)
            sheet.set_column("L:L", 9.14)
            sheet.set_column("M:M", 9.14)
            sheet.set_column("N:N", 9.14)
            sheet.set_column("O:O", 9.14)
            sheet.set_column("P:P", 9.14)
            sheet.set_column("Q:Q", 9.14)
            sheet.set_column("R:R", 9.14)
            sheet.set_column("S:S", 9.14)
            sheet.set_column("T:T", 9.14)
            sheet.set_column("U:U", 9.14)
            sheet.set_column("V:V", 9.14)
            sheet.set_column("W:W", 9.14)
            sheet.set_column("X:X", 10.57)
            # Datos Principal
            sheet.write(2, 0, "Nombre")
            sheet.write(2, 1, "CI")
            sheet.write(2, 2, "Días")
            sheet.write(2, 3, "SLD")
            sheet.write(2, 4, "H.E.")
            sheet.write(2, 5, "FR")
            sheet.write(2, 6, "MOV")
            sheet.write(2, 7, "13º")
            sheet.write(2, 8, "14º")
            sheet.write(2, 9, "O. Ing")
            sheet.write(2, 10, "T. Ing")
            sheet.write(2, 11, "AQ")
            sheet.write(2, 12, "9,45%")
            sheet.write(2, 13, "17,60%")
            sheet.write(2, 14, "PAS")
            sheet.write(2, 15, "PQ")
            sheet.write(2, 16, "PH")
            sheet.write(2, 17, "CYG")
            sheet.write(2, 18, "MUL")
            sheet.write(2, 19, "F/A")
            sheet.write(2, 20, "CEL")
            sheet.write(2, 21, "O. EGR")
            sheet.write(2, 22, "T. EGR")
            sheet.write(2, 23, "NETO")
            row = 3
            sheet.autofilter('A3:X3')
            sheet.merge_range('A1:X2', 'ROL CONSOLIDADO', title)
            for line in record.lines_payslip_run:
                sheet.write(row, 0, line.name)
                sheet.write(row, 1, line.identification_id)
                sheet.write(row, 2, line.worked_days)
                sheet.write(row, 3, line.wage, _right_format)
                sheet.write(row, 4, line.additional_hours, _right_format)
                sheet.write(row, 5, line.reserve_funds, _right_format)
                sheet.write(row, 6, line.mobilization, _right_format)
                sheet.write(row, 7, line.tenth_3, _right_format)
                sheet.write(row, 8, line.tenth_4, _right_format)
                sheet.write(row, 9, line.other_income, _right_format)
                sheet.write(row, 10, line.total_income, _right_format)
                sheet.write(row, 11, line.payment_advance, _right_format)
                sheet.write(row, 12, line.iess_personal, _right_format)
                sheet.write(row, 13, line.iess_patronal, _right_format)
                sheet.write(row, 14, line.loan_payment_advance, _right_format)
                sheet.write(row, 15, line.loan_unsecured, _right_format)
                sheet.write(row, 16, line.loan_mortgage, _right_format)
                sheet.write(row, 17, line.spouses_extension, _right_format)
                sheet.write(row, 18, line.penalty, _right_format)
                sheet.write(row, 19, line.absence, _right_format)
                sheet.write(row, 20, line.cellular_plan, _right_format)
                sheet.write(row, 21, line.other_expenses, _right_format)
                sheet.write(row, 22, line.total_expenses, _right_format)
                sheet.write(row, 23, line.net_receive, _right_format)
                row += 1
            # Total
            total = sum(line.wage for line in record.lines_payslip_run)
            sheet.write(row, 3, total, _right_format)
            total = sum(line.additional_hours for line in record.lines_payslip_run)
            sheet.write(row, 4, total, _right_format)
            total = sum(line.reserve_funds for line in record.lines_payslip_run)
            sheet.write(row, 5, total, _right_format)
            total = sum(line.mobilization for line in record.lines_payslip_run)
            sheet.write(row, 6, total, _right_format)
            total = sum(line.tenth_3 for line in record.lines_payslip_run)
            sheet.write(row, 7, total, _right_format)
            total = sum(line.tenth_4 for line in record.lines_payslip_run)
            sheet.write(row, 8, total, _right_format)
            total = sum(line.other_income for line in record.lines_payslip_run)
            sheet.write(row, 9, total, _right_format)
            total = sum(line.total_income for line in record.lines_payslip_run)
            sheet.write(row, 10, total, _right_format)
            total = sum(line.payment_advance for line in record.lines_payslip_run)
            sheet.write(row, 11, total, _right_format)
            total = sum(line.iess_personal for line in record.lines_payslip_run)
            sheet.write(row, 12, total, _right_format)
            total = sum(line.iess_patronal for line in record.lines_payslip_run)
            sheet.write(row, 13, total, _right_format)
            total = sum(line.loan_payment_advance for line in record.lines_payslip_run)
            sheet.write(row, 14, total, _right_format)
            total = sum(line.loan_unsecured for line in record.lines_payslip_run)
            sheet.write(row, 15, total, _right_format)
            total = sum(line.loan_mortgage for line in record.lines_payslip_run)
            sheet.write(row, 16, total, _right_format)
            total = sum(line.spouses_extension for line in record.lines_payslip_run)
            sheet.write(row, 17, total, _right_format)
            total = sum(line.penalty for line in record.lines_payslip_run)
            sheet.write(row, 18, total, _right_format)
            total = sum(line.absence for line in record.lines_payslip_run)
            sheet.write(row, 19, total, _right_format)
            total = sum(line.cellular_plan for line in record.lines_payslip_run)
            sheet.write(row, 20, total, _right_format)
            total = sum(line.other_expenses for line in record.lines_payslip_run)
            sheet.write(row, 21, total, _right_format)
            total = sum(line.total_expenses for line in record.lines_payslip_run)
            sheet.write(row, 22, total, _right_format)
            total = sum(line.net_receive for line in record.lines_payslip_run)
            sheet.write(row, 23, total, _right_format)


class AdvancePayment(models.AbstractModel):
    _name = 'report.eliterp_hr.eliterp_report_payslip_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, records):
        for record in records:
            sheet = workbook.add_worksheet('Rol Consolidado')
            # Formatos
            _right_format = workbook.add_format({'align': 'right', 'num_format': '$#,##0.00'})
            title = workbook.add_format({
                'bold': True,
                'border': 1,
                'align': 'center'
            })
            # Columnas
            sheet.set_column("A:A", 36)
            sheet.set_column("B:B", 12)
            sheet.set_column("C:C", 21)
            sheet.set_column("D:D", 15)
            sheet.set_column("E:E", 6)
            sheet.set_column("F:F", 8.5)
            sheet.set_column("G:G", 8.5)
            sheet.set_column("H:H", 7.4)
            # Datos Principal
            sheet.write(2, 0, "Empleado")
            sheet.write(2, 1, "No. Ident.")
            sheet.write(2, 2, "Cargo")
            sheet.write(2, 3, "Fecha ingreso")
            sheet.write(2, 4, "Días")
            sheet.write(2, 5, "Monto")
            sheet.write(2, 6, "Moviliz.")
            sheet.write(2, 7, "Total")
            row = 3
            sheet.autofilter('A3:H3')
            sheet.merge_range('A1:H2', 'Anticipo quincena', title)
            for line in record.lines_advance:
                sheet.write(row, 0, line.employee_id.name)
                sheet.write(row, 1, line.employee_id.identification_id)
                sheet.write(row, 2, line.job_id.name)
                sheet.write(row, 3, line.admission_date)
                sheet.write(row, 4, line.antiquity)
                sheet.write(row, 5, line.amount_advance)
                sheet.write(row, 6, line.mobilization)
                sheet.write(row, 7, line.amount_total)
                row += 1