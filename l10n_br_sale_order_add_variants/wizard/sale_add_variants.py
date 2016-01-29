# -*- coding: utf-8 -*-
##############################################################################
#
#   Copyright (c) 2015 Kmee - www.kmee.com.br
#   @author Daniel Sadamo
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
from openerp import api, models, fields


class SaleAddVariants(models.TransientModel):
    _inherit = 'sale.add.variants'

    @api.multi
    def add_to_order(self):
        result = {}
        ctx = dict(self.env.context)
        sale_order = self.env['sale.order'].browse(ctx.get('active_id'))
        for line in self.variant_line_ids:
            if not line.product_uom_qty:
                continue
            line_values = {
                'company_id': sale_order.company_id.id,
                'product_id': line.product_id.id,
                'product_uom_qty': line.product_uom_qty,
                'product_uom': line.product_uom.id,
                'discount': line.discount,
                'order_id': sale_order.id,
                'fiscal_category_id': sale_order.fiscal_category_id.id,
                'fiscal_position': sale_order.fiscal_position.id,
            }
            ctx.update({
                'company_id': sale_order.company_id.id,
                'field_parent': 'order_id',
                'parent_fiscal_category_id': sale_order.fiscal_category_id.id,
                'parent_fiscal_position': sale_order.fiscal_position.id,
                'partner_id': sale_order.partner_id.id,
                'partner_invoice_id': sale_order.partner_invoice_id.id,
                'pricelist': sale_order.pricelist_id.id,
                'quantity': line.product_uom_qty
            }
            )
            result = sale_order.order_line.with_context(
                ctx).product_id_change(
                pricelist=sale_order.pricelist_id.id,
                product=line_values['product_id'],
                qty=line_values['product_uom_qty'],
                uom=line_values['product_uom'],
                partner_id=sale_order.partner_id.id,
                fiscal_position=line_values['fiscal_position']
            )
            taxes = result['value']['tax_id']
            result['value']['tax_id'] = [[6, 0, (tax.id for tax in taxes)]]
            line_values.update(result['value'])
            sale_order.order_line.with_context(ctx).create(line_values)

class SaleAddVariantsLine(models.TransientModel):
    _inherit = 'sale.add.variants.line'

    discount = fields.Float(string="Discount (%)")
