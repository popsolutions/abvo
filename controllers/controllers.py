# -*- coding: utf-8 -*-
from odoo import http

# class Abvo(http.Controller):
    # @http.route('/abvo/abvo/', auth='public')
    # def index(self, **kw):
    #     return "Hello, world"

    # @http.route('/abvo/abvo/objects/', auth='public')
    # def list(self, **kw):
    #     return http.request.render('abvo.listing', {
    #         'root': '/abvo/abvo',
    #         'objects': http.request.env['abvo.abvo'].search([]),
    #     })

    # @http.route('/abvo/abvo/objects/<model("abvo.abvo"):obj>/', auth='public')
    # def object(self, obj, **kw):
    #     return http.request.render('abvo.object', {
    #         'object': obj
    #     })

    # partner = request.env.user.partner_id