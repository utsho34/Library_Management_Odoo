from odoo import models, Command,fields

class AccountMove(models.Model):
    _inherit = "account.move"

    confirm_user_id = fields.Many2one('res.users',string='Confirm User', default=lambda self: self.env.user,readonly=True)

