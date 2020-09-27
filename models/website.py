from odoo import models
from odoo.http import request


class WebsiteAbvo(models.Model):
    _inherit = 'website'

    def sale_get_order(self, force_create=False, code=None, update_pricelist=False, force_pricelist=False):
        order = super(WebsiteAbvo, self).sale_get_order(force_create, code, update_pricelist, force_pricelist)
        if update_pricelist:
            order.write({'boat_id': request.params.get('boat_id')})
        return order
