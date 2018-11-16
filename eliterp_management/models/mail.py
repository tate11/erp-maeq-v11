# -*- coding: utf-8 -*-
# Copyright 2018 Elitumdevelop S.A, Ing. Mario Rangel
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import _, api, fields, models, SUPERUSER_ID, tools
from odoo.tools.safe_eval import safe_eval


class MailComposeMessage(models.TransientModel):
    _inherit = 'mail.compose.message'

    @api.multi
    def send_mail(self, auto_commit=False):
        """
        Método sobrescrito para poder enviar correo y adjunto, estándar no funciona
        :param auto_commit:
        :return:
        """
        if self._context.get('send_mail_attachment', False):
            try:
                template = self.template_id
            except ValueError:
                template = False
            if template:
                template.sudo().send_mail(self.res_id, force_send=True, raise_exception=True)
        return super(MailComposeMessage, self).send_mail(auto_commit=auto_commit)


