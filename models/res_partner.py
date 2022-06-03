from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = "res.partner"

    birthday = fields.Date(string="Birthday")
    age = fields.Integer(string="Age", compute="_compute_age", store=True, help="Current date- Birthday")
    branch = fields.Many2one(
        comodel_name="res.users",
        string="Branch",
        default=lambda self: self.env.user.id,
        help="According to the users list, default value is the user that created the customer card",
    )
    hmo = fields.Selection(
        selection=[
            ("national", "National"),
            ("clalit", "Clalit"),
            ("maccabi", "Maccabi"),
            ("united", "United"),
            ("private", "Private"),
        ],
        string="Health Maintenance Organization",
        help="לאומית,כללית,מכבי,מאוחדתפרטי",
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
