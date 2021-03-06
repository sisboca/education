# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import tools
from odoo import api, fields, models
from psycopg2.extensions import AsIs


class EducationGroupStudentProgenitorReport(models.Model):
    _name = "education.group.student.progenitor.report"
    _inherit = "education.group.report"
    _description = "Student Progenitor Group List"
    _auto = False
    _rec_name = "progenitor_id"
    _order = "student_id,progenitor_id"

    @api.model
    def _get_selection_relation(self):
        return self.env["res.partner.family"].fields_get(
            allfields=["relation"])["relation"]["selection"]

    progenitor_id = fields.Many2one(
        comodel_name="res.partner", string="Progenitor")
    progenitor_email = fields.Char()
    progenitor_phone = fields.Char()
    progenitor_mobile = fields.Char()
    relation = fields.Selection(
        string="Relation",  selection=_get_selection_relation)

    _depends = {
        "education.group": [
            "center_id", "course_id", "student_ids"
        ],
        "res.partner.family": [
            "child2_id", "responsible_id", "relation"
        ]
    }

    def _select(self):
        select_str = """
                , fam.responsible_id AS progenitor_id
                , p.email AS progenitor_email
                , p.phone AS progenitor_phone
                , p.mobile AS progenitor_mobile
                , fam.relation AS relation
        """
        return super(EducationGroupStudentProgenitorReport,
                     self)._select() + select_str

    def _from(self):
        from_str = """
                JOIN res_partner_family fam
                  ON fam.child2_id = stu.id
                JOIN res_partner p
                  ON fam.responsible_id = p.id
        """
        return super(EducationGroupStudentProgenitorReport,
                     self)._from() + from_str

    def _group_by(self):
        group_by_str = """
                , fam.responsible_id
                , fam.relation
                , p.email
                , p.phone
                , p.mobile
        """
        return super(EducationGroupStudentProgenitorReport,
                     self)._group_by() + group_by_str

    @api.model_cr
    def init(self):
        # self._table = education_group_student_progenitor_report
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute(
            """CREATE or REPLACE VIEW %s as
                (
                %s %s %s
            )""", (
                AsIs(self._table), AsIs(self._select()), AsIs(self._from()),
                AsIs(self._group_by()),))
