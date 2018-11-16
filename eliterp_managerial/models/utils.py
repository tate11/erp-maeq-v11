# -*- coding: utf-8 -*-
# Copyright 2018 Elitumdevelop S.A, Ing. Mario Rangel
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import models


class ManagerialHelps(models.TransientModel):
    _name = 'eliterp.managerial.helps'
    _description = 'Ayudas para gerencial'

    def send_mail(self, id, table, template):
        # Envíamos un mail a los usuarios relacionados (Configuración módulo gerencial)
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        if base_url and base_url[-1:] != '/':
            base_url += '/'
        url = "{}web?#id={}&view_type=form&model={}".format(base_url, id, table)
        local_context = self.env.context.copy()
        local_context.update({
            'url': url
        })
        try:
            template = self.env.ref('eliterp_managerial.%s' % template)
        except ValueError:
            template = False
        if template:
            template.with_context(local_context).sudo().send_mail(id, force_send=True, raise_exception=True)
