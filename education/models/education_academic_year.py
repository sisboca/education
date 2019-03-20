# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class EducationAcademicYear(models.Model):
    _name = 'education.academic_year'
    _description = 'Academic Year'
    _order = 'name DESC'

    name = fields.Char(string='Academic Year', required=True)
    date_start = fields.Date(string='Start Date')
    date_end = fields.Date(string='End Date')

    @api.constrains('name')
    def _check_education_code(self):
        code_length = 9
        for record in self:
            if not len(record.name) == code_length:
                raise ValidationError(
                    _('Academic year must be {} digits long!').format(
                        code_length))

    @api.constrains('date_start', 'date_end')
    def _check_date_end_after_date_start(self):
        for record in self.filtered(lambda r: r.date_start and r.date_end):
            if not record.date_end > record.date_start:
                raise ValidationError(
                    _('End date must be after start date.'))

    _sql_constraints = [
        ('name_unique', 'unique(name)', 'Academic year must be unique!'),
    ]
