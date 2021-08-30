from odoo import api, fields, models


class AbvoCertificates(models.Model):
    _name = 'abvo.certificates'
    _description = 'ABVO Certificates'

    date = fields.Date()

    certificate_type = fields.Selection([('irc', 'IRC'), ('orc', 'ORC'), ('mocra', 'MOCRA'), ('vrps', 'VRPS'), ('bra-rgs', 'BRA-RGS')],
                                        default='bra-rgs', string='Type')
    raiting = fields.Float(digits=(1, 4))

    loa = fields.Char()

    pdf = fields.Binary()

    partner_id = fields.Many2one('res.partner', 'Partner')
    
    invoice_id = fields.Many2one('account.invoice', 'Invoice')
