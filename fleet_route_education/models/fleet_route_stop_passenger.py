# Copyright 2020 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models, api


class FleetRouteStopPassenger(models.Model):
    _inherit = "fleet.route.stop.passenger"
    _order = ("stop_id,partner_center_id,partner_level_id,partner_course_id,"
              "partner_group_section_id,partner_id")

    partner_group_id = fields.Many2one(
        comodel_name="education.group", string="Current Group",
        related="partner_id.current_group_id", store=True)
    partner_center_id = fields.Many2one(
        comodel_name="res.partner", string="Current Education Center",
        related="partner_id.current_center_id", store=True)
    partner_level_id = fields.Many2one(
        comodel_name="education.level", string="Current Education Level",
        related="partner_id.current_level_id", store=True)
    partner_course_id = fields.Many2one(
        comodel_name="education.course", string="Current Course",
        related="partner_id.current_course_id", store=True)
    partner_group_section_id = fields.Many2one(
        comodel_name="education.section", string="Section",
        related="partner_id.current_group_id.section_id", store=True)
    route_complete_product_id = fields.Many2one(
        comodel_name='product.product', string='Route complete product',
        compute='_compute_route_complete_product_id',
        store=True)
    route_half_product_id = fields.Many2one(
        comodel_name='product.product', string='Route half product',
        compute='_compute_route_half_product_id',
        store=True)

    @api.multi
    @api.depends('route_id', 'route_id.name_id',
                 'route_id.name_id.complete_route_product_id')
    def _compute_route_complete_product_id(self):
        for passenger in self:
            product = False
            if passenger.route_id.name_id.complete_route_product_id:
                product = passenger.route_id.name_id.complete_route_product_id
            passenger.route_complete_product_id = (
                product.id if product else False)

    @api.multi
    @api.depends('route_id', 'route_id.name_id',
                 'route_id.name_id.half_route_product_id')
    def _compute_route_half_product_id(self):
        for passenger in self:
            product = False
            if passenger.route_id.name_id.half_route_product_id:
                product = passenger.route_id.name_id.half_route_product_id
            passenger.route_half_product_id = (
                product.id if product else False)
