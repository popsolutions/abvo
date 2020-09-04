# -*- coding: utf-8 -*-

from odoo import api, fields, models
from . import abvo_certificates


class ResPartner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    company_type = fields.Selection(selection_add=[('boat','Embarcação')], 
                                    compute='_compute_company_type', inverse='_write_company_type')

    estaleiro = fields.Char(u'Estaleiro')
    modelo = fields.Char(u'Modelo')
    loa = fields.Float(u'Loa')
    deslocamento = fields.Integer(u'Deslocamento')
    numeral = fields.Char(u'Numeral')
    clube = fields.Char(u'Clube')

    certificates_lines = fields.One2many('abvo.certificates', 'partner_id',
                                         readonly=True, copy=True)

    is_boat = fields.Boolean(default=False)

    def _write_company_type(self):
        for partner in self:
            if partner.company_type == 'boat':
                self.is_boat = True
                self.is_company = True
            else:
                partner.is_company = partner.company_type == 'company'

    @api.depends('is_company')
    def _compute_company_type(self):
        for partner in self:
            if partner.is_boat == True:
                partner.company_type = 'boat'
            else:
                partner.company_type = 'company' if partner.is_company else 'person'

    @api.onchange('company_type')
    def onchange_company_type(self):
        for partner in self:
            if self.company_type == 'boat':
                self.is_boat = True
                self.is_company = True
            else: 
                self.is_company = (self.company_type == 'company')
