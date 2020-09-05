# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http, _
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo.addons.payment.controllers.portal import PaymentProcessing
from odoo.exceptions import AccessError, MissingError
from odoo.http import request


class PortalABVOCertificates(CustomerPortal):

    def _prepare_portal_layout_values(self):
        cert_user = False
        values = super(PortalABVOCertificates, self)._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        # cert_count = partner.certificates_lines
        if partner.user_id and not partner.user_id._is_public():
            cert_user = partner.user_id
        return {
            'sales_user': cert_user,
            'page_name': 'home',
            'archive_groups': [],
            # 'certificates_count': cert_count
        }

    # ------------------------------------------------------------
    # My Invoices
    # ------------------------------------------------------------

    def _certificate_get_page_view_values(self, certificate, access_token, **kwargs):
        values = {
            'page_name': 'certificate',
            'invoice': certificate,
        }
        return self._get_page_view_values(certificate, access_token, values, 'my_certificates_history', False, **kwargs)

    @http.route(['/my/certificates', '/my/certificates/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_certificates(self, page=1, date_begin=None, date_end=None, sortby=None, **kw):
        values = self._prepare_portal_layout_values()
        AbvoCertificate = request.env['res_partner.certificates_lines']

        domain = []

        # searchbar_sortings = {
        #     'date': {'label': _('Invoice Date'), 'order': 'date_invoice desc'},
        #     'duedate': {'label': _('Due Date'), 'order': 'date_due desc'},
        #     'name': {'label': _('Reference'), 'order': 'name desc'},
        #     'state': {'label': _('Status'), 'order': 'state'},
        # }
        # # default sort by order
        if not sortby:
            sortby = 'date'
        # order = searchbar_sortings[sortby]['order']

        # archive_groups = self._get_archive_groups('account.invoice', domain)
        # if date_begin and date_end:
        #     domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]

        # count for pager
        cert_count = AbvoCertificate.search_count(domain)
        # pager
        pager = portal_pager(
            url="/my/certificates",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
            total=cert_count,
            page=page,
            step=self._items_per_page
        )
        # content according to pager and archive selected
        # certificates = AbvoCertificate.search(domain, order=order, limit=self._items_per_page, offset=pager['offset'])
        certificates = AbvoCertificate.search(domain, limit=self._items_per_page, offset=pager['offset'])
        # request.session['my_invoices_history'] = invoices.ids[:100]

        values.update({
            'date': date_begin,
            'certificates': certificates,
            'page_name': 'certificate',
            'pager': pager,
            # 'archive_groups': archive_groups,
            'default_url': '/my/certificates',
            # 'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
        })
        return request.render("account.portal_my_invoices", values)

    # @http.route(['/my/invoices/<int:invoice_id>'], type='http', auth="public", website=True)
    # def portal_my_invoice_detail(self, invoice_id, access_token=None, report_type=None, download=False, **kw):
    #     try:
    #         invoice_sudo = self._document_check_access('account.invoice', invoice_id, access_token)
    #     except (AccessError, MissingError):
    #         return request.redirect('/my')

    #     if report_type in ('html', 'pdf', 'text'):
    #         return self._show_report(model=invoice_sudo, report_type=report_type, report_ref='account.account_invoices', download=download)

    #     values = self._invoice_get_page_view_values(invoice_sudo, access_token, **kw)
    #     PaymentProcessing.remove_payment_transaction(invoice_sudo.transaction_ids)
    #     return request.render("account.portal_invoice_page", values)
