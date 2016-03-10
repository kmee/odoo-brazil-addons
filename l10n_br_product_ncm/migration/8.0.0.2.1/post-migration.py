# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Alexandre Fayolle
#    Copyright 2014 Camptocamp SA
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
import logging

from openerp.openupgrade import openupgrade
from openerp import pooler, SUPERUSER_ID

logger = logging.getLogger('OpenUpgrade.product')


def create_properties_fci(cr, pool):
    """ Fields moved to properties (fci).

    Write using the ORM so the prices will be written as properties.
    """
    product_obj = pool['product.product']
    sql = ("SELECT id, %s FROM product_product" %
           openupgrade.get_legacy_name('fci'))
    cr.execute(sql)
    logger.info(
        "Creating product_product.property_fci properties"
        " for %d products." % (cr.rowcount))
    for product_id, fci in cr.fetchall():
        product_obj.write(cr, SUPERUSER_ID, [product_id],
                           {'fci': fci})
    # make properties global
    sql = ("""
        UPDATE ir_property
        SET company_id = null
        WHERE res_id like 'product.product,%%'
        AND name = 'fci'""")
    openupgrade.logged_query(cr, sql)


def create_properties_origin(cr, pool):
    """ Fields moved to properties (origin).

    Write using the ORM so the prices will be written as properties.
    """
    product_obj = pool['product.product']
    sql = ("SELECT id, %s FROM product_product" %
           openupgrade.get_legacy_name('origin'))
    cr.execute(sql)
    logger.info(
        "Creating product_product.property_origin properties"
        " for %d products." % (cr.rowcount))
    for product_id, origin in cr.fetchall():
        product_obj.write(cr, SUPERUSER_ID, [product_id],
                           {'origin': origin})
    # make properties global
    sql = ("""
        UPDATE ir_property
        SET company_id = null
        WHERE res_id like 'product.product,%%'
        AND name = 'origin'""")
    openupgrade.logged_query(cr, sql)

@openupgrade.migrate()
def migrate(cr, version):
    pool = pooler.get_pool(cr.dbname)
    create_properties_origin(cr, pool)
    create_properties_fci(cr, pool)