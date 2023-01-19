from odoo import api, fields, models

class BookGenre(models.Model):
    _name = "book.genre"
    _description = "all books genre"
    _order = "name"
    _sql_constraints = [
        ("check_name", "UNIQUE(name)", "The book genre must be unique"),
    ]

    name = fields.Char(string='Book Genre')
    color = fields.Integer("Color Index")
    book_id = fields.Many2one('product.template')
    manager_id = fields.Many2one('res.users', string = 'Manager')



