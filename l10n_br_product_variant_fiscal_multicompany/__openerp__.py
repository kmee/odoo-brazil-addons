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

{
    'name': 'l10n_br_product_product_fiscal_multicompany',
    'summary': 'L10n Brazil Product Fiscal fields as properties',
    'version': '8.0.0.0.0',
    'author': 'KMEE,Odoo Community Association (OCA)',
    'website': 'https://odoo-community.org/',
    'category': "Localization",
    'license': 'AGPL-3',
    'depends': [
        'l10n_br_product_ncm',
    ],
    'data': [
      'views/view.xml'
    ],
    'installable': True,
    'auto_install': False,
    'pre_init_hook': 'pre_init_hook',
}