# -*- coding: utf-8 -*-
###############################################################################
#
# Copyright (C) 2015  Luis Felipe Miléo - KMEE
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
###############################################################################

# -*- coding: utf-8 -*-
##############################################################################
#
#    Account Product - Fiscal Classification module for Odoo
#    Copyright (C) 2014 -Today GRAP (http://www.grap.coop)
#    @author Sylvain LE GAL (https://twitter.com/legalsylvain)
#    @author Renato Lima (https://twitter.com/renatonlima)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


from openerp import models, fields, api, _
from openerp.exceptions import ValidationError


class AccountProductFiscalClassification(models.Model):
    """Fiscal Classification of customer and supplier taxes.
    This classification is linked to a product to select a bundle of taxes
     in one time."""
    _inherit = 'account.product.fiscal.classification'

    product_product_ids = fields.One2many(
        comodel_name='product.product', string='Products',
        compute='_compute_product_product_info')

    product_product_qty = fields.Integer(
        string='Products Quantity', compute='_compute_product_product_info')

    # Compute Section
    @api.one
    def _compute_product_product_info(self):
        res = self.env['product.product'].search([
            ('fiscal_classification_id', '=', self.id), '|',
            ('active', '=', False), ('active', '=', True)])
        self.product_product_ids = res
        self.product_product_qty = len(res)
        self.product_tmpl_ids = self.env['product.template']
        self.product_tmpl_qty = 0

    @api.multi
    def write(self, vals):
        res = super(AccountProductFiscalClassification, self).write(vals)
        pt_obj = self.env['product.product']
        if ('purchase_tax_definition_line' in vals or
                'sale_tax_definition_line' in vals):
            for fc in self:
                pt_lst = pt_obj.browse([x.id for x in fc.product_product_ids])
                if pt_lst:
                    pt_lst.write({'fiscal_classification_id': fc.id})
        return res

    @api.multi
    def unlink(self):
        for fc in self:
            if fc.product_product_qty != 0:
                raise ValidationError(_(
                    "You cannot delete The Fiscal Classification '%s' because"
                    " it contents %s products. Please move products"
                    " to another Fiscal Classification first.") % (
                    fc.name, fc.product_product_qty))
        return super(AccountProductFiscalClassification, self).unlink()

    # Custom Sections
    @api.model
    def find_or_create(self, company_id, sale_tax_ids, purchase_tax_ids):
        at_obj = self.env['account.tax']
        # Search for existing Fiscal Classification

        fcs = self.search(
            ['|', ('active', '=', False), ('active', '=', True)])

        for fc in fcs:
            if (
                    fc.company_id.id == company_id
                    and sorted(fc.sale_tax_ids.ids) ==
                    sorted(sale_tax_ids)
                    and sorted(fc.purchase_tax_ids.ids) ==
                    sorted(purchase_tax_ids)
                    ):
                return fc.id

        # create new Fiscal classification if not found
        if len(sale_tax_ids) == 0 and len(purchase_tax_ids) == 0:
            name = _('No taxes')
        elif len(purchase_tax_ids) == 0:
            name = _('No Purchase Taxes - Sale Taxes: ')
            for tax in at_obj.browse(sale_tax_ids):
                name += tax.description and tax.description or tax.name
                name += ' + '
            name = name[:-3]
        elif len(sale_tax_ids) == 0:
            name = _('Purchase Taxes: ')
            for tax in at_obj.browse(purchase_tax_ids):
                name += tax.description and tax.description or tax.name
                name += ' + '
            name = name[:-3]
            name += _('- No Sale Taxes')
        else:
            name = _('Purchase Taxes: ')
            for tax in at_obj.browse(purchase_tax_ids):
                name += tax.description and tax.description or tax.name
                name += ' + '
            name = name[:-3]
            name += _(' - Sale Taxes: ')
            for tax in at_obj.browse(sale_tax_ids):
                name += tax.description and tax.description or tax.name
                name += ' + '
            name = name[:-3]
        name = name[:self._MAX_LENGTH_NAME] \
            if len(name) > self._MAX_LENGTH_NAME else name
        return self.create({
            'name': name,
            'company_id': company_id,
            'sale_tax_ids': [(6, 0, sale_tax_ids)],
            'purchase_tax_ids': [(6, 0, purchase_tax_ids)]}).id
