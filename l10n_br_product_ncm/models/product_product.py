# -*- coding: utf-8 -*-
##############################################################################
#
#   Copyright (c) 2015 Kmee - www.kmee.com.br
#   @author Fernando Marcato Rodrigues
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
from openerp.addons.l10n_br_account_product.models.product import \
    PRODUCT_ORIGIN
from openerp.exceptions import ValidationError


class ProductProduct(models.Model):
    """Personalization to allow different ncm's in product variants"""
    _inherit = "product.product"

    fiscal_classification_id = fields.Many2one(
        'account.product.fiscal.classification', u'NCM')
    categ_id = fields.Many2one('product.category','Internal Category',
        required=True, change_default=True, domain="[('type','=','normal')]",
        help="Select category for the current product")
    origin = fields.Selection(PRODUCT_ORIGIN, 'Origem')
    fci = fields.Char('FCI do Produto', size=36)


    @api.multi
    def write(self, vals):
        res = super(ProductProduct, self).write(vals)
        self.write_taxes_setting(vals)
        return res

    # Custom Section
    def write_taxes_setting(self, vals):
        """If Fiscal Classification is defined, set the according taxes
        to the product(s); Otherwise, find the correct Fiscal classification,
        depending of the taxes, or create a new one, if no one are found."""
        if vals.get('fiscal_classification_id', False):
            # update or replace 'taxes_id' and 'supplier_taxes_id'
            classification = self.env[
                'account.product.fiscal.classification'].browse(
                vals['fiscal_classification_id'])
            tax_vals = {
                'supplier_taxes_id': [[6, 0, [
                    x.id for x in classification.purchase_tax_ids]]],
                'taxes_id': [[6, 0, [
                    x.id for x in classification.sale_tax_ids]]],
                }
            super(ProductProduct, self.sudo()).write(tax_vals)
        elif 'supplier_taxes_id' in vals.keys() or 'taxes_id' in vals.keys():
            # product template Single update mode
            fc_obj = self.env['account.product.fiscal.classification']
            if len(self) != 1:
                raise ValidationError(
                    _("You cannot change Taxes for many Products."))
            purchase_tax_ids = [x.id for x in self.sudo().supplier_taxes_id]
            sale_tax_ids = [x.id for x in self.sudo().taxes_id]
            fc_id = fc_obj.find_or_create(
                self.company_id.id, sale_tax_ids, purchase_tax_ids)
            super(ProductProduct, self.sudo()).write(
                {'fiscal_classification_id': fc_id})


class ProductTemplate(models.Model):
    """Personalization to allow different ncm's in product variants"""
    _inherit = "product.template"

    fiscal_classification_id = fields.Many2one(
        comodel_name='account.product.fiscal.classification',
        string='Fiscal Classification',
        help="Specify the combination of taxes for this product."
        " This field is required. If you dont find the correct Fiscal"
        " Classification, Please create a new one or ask to your account"
        " manager if you don't have the access right.", readonly=True)

    def write_taxes_setting(self, vals):
        """If Fiscal Classification is defined, set the according taxes
        to the product(s); Otherwise, find the correct Fiscal classification,
        depending of the taxes, or create a new one, if no one are found."""
        return
