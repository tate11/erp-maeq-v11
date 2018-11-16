# -*- coding: utf-8 -*-
# Copyright 2018 Elitumdevelop S.A, Ing. Abel Espinal
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models, _
import json
from datetime import datetime, timedelta, date


class SalesDashboard(models.Model):
    _name = 'sales.dashboard'
    _description = 'Tablero del módulo de ventas'

    name = fields.Char('Nombre')
    description = fields.Text('Descripción de la gráfica')
    kanban_dashboard = fields.Text('Datos tablero', compute='_kanban_dashboard')
    kanban_dashboard_graph = fields.Text('Datos gráfica', compute='_kanban_dashboard_graph')
    show_on_dashboard = fields.Boolean(string='Mostrar en tablero', default=True)
    type = fields.Selection([('bar', 'Barra'),
                             ('line', 'Línea'),
                             ('bar_stacked', 'Barra agrupada'),
                             ('pie', 'Pie')], string="Tipo de tablero")

    @api.one
    def _kanban_dashboard(self):
        """
        Datos en formato JSON
        :return:
        """
        self.kanban_dashboard = json.dumps(self._get_dashboard_datas())

    @api.multi
    def _get_dashboard_datas(self):
        """
        Retornamos datos para mostrar en tablero
        :return:
        """
        return {
            'data_dashboard_invoicing': self._get_data_dashboard_invoicing(),
        }

    @api.multi
    def _get_data_dashboard_invoicing(self):
        """
        Datos para Facturación (Último trimestre)
        :return:
        """
        data = []
        global_functions = self.env['eliterp.global.functions']
        today = fields.date.today()
        for x in range(-2, 1):
            query = """select cast((sum(inv.amount_untaxed)) as float)
                                               from account_invoice as inv
                                               where extract(MONTH FROM inv.date_invoice) = EXTRACT(month FROM current_date + '%s  month'::interval)
                                               and extract(YEAR FROM inv.date_invoice) = EXTRACT(YEAR FROM current_date + '%s month'::interval)
                                               and inv.type = 'out_invoice'
                                               and inv.state in ('open', 'paid')""" % (x, x)
            self.env.cr.execute(query)
            invoices = self.env.cr.dictfetchall()
            month = today.month + x
            data.append({
                'month': global_functions._get_month_name(month),
                'amount': "{:.2f}".format(float(invoices[0]['sum'])) if invoices[0]['sum'] else 0.00
            })
        return data

    @api.one
    def _kanban_dashboard_graph(self):
        """
        Datos para gráficas
        :return:
        """
        if self.type in ['bar']:
            self.kanban_dashboard_graph = json.dumps(self._get_bar_graph_datas())

    @api.multi
    def _get_bar_graph_datas(self):
        """
        TODO: Mejorar data para gráficas, código muy extenso
        :return:
        """
        data = []
        query = """select cast((sum(inv.amount_untaxed)) as float)
                                        from account_invoice as inv
                                        where extract(MONTH FROM inv.date_invoice) = EXTRACT(month FROM current_date - '2 month'::interval)
                                        and extract(YEAR FROM inv.date_invoice) = EXTRACT(YEAR FROM current_date - '2 month'::interval)
                                        and inv.type='out_invoice'
                                        and inv.state in ('open', 'paid')"""
        self.env.cr.execute(query)
        invoices_2 = self.env.cr.dictfetchall()
        query = """select cast((sum(inv.amount_untaxed)) as float)
                                        from account_invoice as inv
                                        where extract(MONTH FROM inv.date_invoice) = EXTRACT(month FROM current_date - '1 month'::interval)
                                        and extract(YEAR FROM inv.date_invoice) = EXTRACT(YEAR FROM current_date - '1 month'::interval)
                                        and inv.type='out_invoice'
                                        and inv.state in ('open', 'paid')"""
        self.env.cr.execute(query)
        invoices_1 = self.env.cr.dictfetchall()
        query = """select cast((sum(inv.amount_untaxed)) as float)
                                        from account_invoice as inv
                                        where extract(MONTH FROM inv.date_invoice) = EXTRACT(month FROM current_date)
                                        and extract(YEAR FROM inv.date_invoice) = EXTRACT(YEAR FROM current_date)
                                        and inv.type='out_invoice'
                                        and inv.state in ('open', 'paid')"""
        self.env.cr.execute(query)
        invoices = self.env.cr.dictfetchall()
        today = fields.date.today()
        global_functions = self.env['eliterp.global.functions']
        data.append({
            'label': global_functions._get_month_name(today.month - 2),
            'value': "{:.2f}".format(float(invoices_2[0]['sum'])) if invoices_2[0]['sum'] else 0.00
        })
        data.append({
            'label': global_functions._get_month_name(today.month - 1),
            'value': "{:.2f}".format(float(invoices_1[0]['sum'])) if invoices_1[0]['sum'] else 0.00
        })
        data.append({
            'label': global_functions._get_month_name(today.month),
            'value': "{:.2f}".format(float(invoices[0]['sum'])) if invoices[0]['sum'] else 0.00
        })
        return [{'values': data}]

    @api.multi
    def open_action(self):
        """
        Abrimos acciones para dirigir a vistas del tablero
        :return:
        """
        action_name = self._context.get('action_name', False)
        type = self._context.get('type', False)
        month = self._context.get('month', False)
        ctx = self._context.copy()
        ctx.pop('group_by', None)
        [action] = self.env.ref(action_name).read()
        today = fields.date.today()
        if type == 'invoices':
            month = today.month + month
            year = today.year
            if month == -1:
                month = 11
                year = year - 1
            if month == 0:
                month = 12
                year = year - 1
            start_date = date(year, month, 1)
            end_date = self.env['eliterp.global.functions']._get_last_day_month(start_date)
            domain = [
                ('type', '=', 'out_invoice'),
                ('state', 'in', ('open', 'paid')),
                ('date_invoice', '<=', end_date.strftime('%Y-%m-%d')),
                ('date_invoice', '>=', start_date.strftime('%Y-%m-%d'))
            ]
            action['domain'] = domain
        action['context'] = ctx
        return action
