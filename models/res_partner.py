from odoo import api, fields, models
from . import abvo_certificates


class ResPartner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    # boat_partner_id = fields.Many2one('res.partner') 
    # company_type = 

    estaleiro = fields.Char(u'Estaleiro')
    modelo = fields.Char(u'Modelo')
    loa = fields.Float(u'Loa')
    deslocamento = fields.Integer(u'Deslocamento')
    numeral = fields.Char(u'Numeral')
    clube = fields.Char(u'Clube')

    certificates_lines = fields.One2many('abvo.certificates', 'partner_id',
                                         readonly=True, copy=True)

    # lines_ids = fields.One2many('pops.measurement.lines', 'measurement_id', 'Measurement Lines', readonly=True,
    #                             copy=True)

    # photo_lines_ids = fields.One2many('pops.measurement.photolines', 'measurement_id', 'Measurement Photo Lines',
                                      # readonly=True, copy=True)
    # missions_id = fields.Many2one('pops.missions', 'Missions', ondelete='cascade', required=True)