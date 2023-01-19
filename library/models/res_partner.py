from odoo import api, fields, models

class LibraryMember(models.Model):
    _inherit = 'res.partner'
    _description = "all member details"

    is_library_member = fields.Boolean('Is member', default=False)
    borrow_ids = fields.One2many('book.borrow', 'reader_id')

