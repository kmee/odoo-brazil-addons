# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2016 KMEE (http://www.kmee.com.br)
#    @author Bianca Tella <bianca.tella@kmee.com.br>
#    @author Luis Felipe Miléo <mileo@kmee.com.br>
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

from openerp import models, fields, api


class ProductFciFromProductProductLines(models.TransientModel):
    _name = "product_fci.from.product.product.lines"
    _description = "Produtos FCI"

    products_ids = fields.Many2many('product.product', 'product_id',
                                    'line_id', 'product_line_rel')

    @api.multi
    def populate_l10n_br_fci(self):
        for wizard in self:
            active_id = wizard._context.get('active_id')

            for product in self.products_ids:
                custo_importado = 0
                if product.bom_ids:
                    for bom in product.bom_ids[0]:
                        for item in bom.bom_line_ids:
                            if item.product_id.origin in ('1', '2', '6', '7'):
                                custo_importado += (
                                    item.product_id.standard_price *
                                    item.product_qty)
                else:
                    if product.origin in ('1', '2', '6', '7'):
                                custo_importado = (
                                    product.standard_price)
                vals = {}
                vals = {
                    'product_id': product.id,
                    'product_uom': product.uom_id.id,
                    'l10n_br_fci_id': active_id,
                    'valor_parcela_importada': round(custo_importado, 2),
                    'list_price': product.list_price,
                }
                fci_line_obj = self.env['l10n_br.fci.line']
                fci_line_obj.create(vals)
        return True
