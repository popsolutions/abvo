# -*- coding: utf-8 -*-
from odoo import api, fields, models


class AccountInvoiceAbvo(models.Model):
    _inherit = 'account.invoice'

    boat_id = fields.Many2one('res.partner', 'Boat',
                              help="Use this field when the product is related to a Boat Membership")

    @api.multi
    def write(self, vals):
        '''Change the partner on related membership_line'''
        res = super(AccountInvoiceAbvo, self).write(vals)
        if 'boat_id' in vals or 'partner_id' in vals:
            self.env['membership.membership_line'].search([
                ('account_invoice_line', 'in', self.mapped('invoice_line_ids').ids)
            ]).write({'partner': vals.get('boat_id', res.boat_id)})
        return res


class AccountInvoiceLineAbvo(models.Model):
    _inherit = 'account.invoice.line'

    @api.multi
    def write(self, vals):
        MemberLine = self.env['membership.membership_line']
        res = super(AccountInvoiceLineAbvo, self).write(vals)
        if res.invoice_id.boat_id:
            member_lines = MemberLine.search([('account_invoice_line', '=', res.id)])
            member_lines.write({
                    'partner': res.invoice_id.boat_id.id})
        return res

    @api.model
    def create(self, vals):
        MemberLine = self.env['membership.membership_line']
        invoice_line = super(AccountInvoiceLineAbvo, self).create(vals)
        if invoice_line.invoice_id.boat_id:
            member_lines = MemberLine.search([('account_invoice_line', '=', invoice_line.id)])
            member_lines.write({
                'partner': invoice_line.invoice_id.boat_id.id})
        return invoice_line
