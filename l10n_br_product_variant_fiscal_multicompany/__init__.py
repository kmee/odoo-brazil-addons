# -*- coding: utf-8 -*-
##############################################################################
#
#   Copyright (c) 2016 Kmee - www.kmee.com.br
#   @author Luis Felipe Mileo
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

from . import models


def pre_init_hook(cr):
    cr.execute("INSERT INTO ir_property(value_text, name, type, "
               "fields_id, res_id) SELECT fci as value_text, "
               "'fci' as name, 'char' as type, ("
               "SELECT id from ir_model_fields where model='product.product' "
               "and name='fci') as fields_id, 'product_product,' ||id as res_id"
               " from product_product where fci is not null;")

    cr.execute("INSERT INTO ir_property(value_text, name, type,"
               "fields_id, res_id ) SELECT origin as value_text,"
               " 'origin' as name, 'selection' as type,("
               "SELECT id from ir_model_fields where model='product.product' "
               "and name='origin') as fields_id, 'product_product,' ||id "
               "as res_id from product_product where origin is not null")
