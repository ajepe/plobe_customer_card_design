from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = "res.partner"

    birthday = fields.Date(string="Birthday")
    age = fields.Integer(string="Age", compute="_compute_age")
    branch_id = fields.Many2one(
        comodel_name="res.users",
        string="Branch",
        default=lambda self: self.env.user.id,
    )
    hmo = fields.Selection(
        selection=[
            ("national", "National"),
            ("clalit", "Clalit"),
            ("maccabi", "Maccabi"),
            ("united", "United"),
            ("private", "Private"),
        ],
        string="Health Maintenance Organization"
    )

    @api.depends("birthday")
    def _compute_age(self):
        today = fields.Date.today()
        for rec in self:
            birthday = rec.birthday
            rec.age = (
                today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))
                if rec.birthday and today >= birthday
                else 0
            )
