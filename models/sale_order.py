# -*- coding: utf-8 -*-

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    boat_id = fields.Many2one('res.partner', 'Boat',
                              help="Use this field when the product is related to a Boat Membership")

    @api.multi
    def _prepare_invoice(self):
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        invoice_vals.update({'boat_id': self.boat_id.id})
        return invoice_vals
