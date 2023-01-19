from odoo import api, fields, models, _
from odoo.exceptions import *
class BookDetails(models.Model):
    _name = "book.details"
    _description = "all books details"
    _order = "name"
    _sql_constraints = [
        ("check_isbn_no", "UNIQUE(isbn_no)", "The ISBN Number must be unique"),
        ("check_stock_of_copies", "CHECK(stock_of_copies > 0)", "The copies of available book must be strictly positive"),
        ("check_copies_of_book", "CHECK(copies_of_book >= 0)", "The Available Copies must be strictly positive"),
    ]
    name = fields.Char(required=True,string='Name Of Book')
    author_id = fields.Many2many('res.partner',string='Author')
    isbn_no = fields.Char(string='ISBN No', required=True)
    published_year = fields.Char(string='Published Year',size=4)
    book_state = fields.Selection(compute='_compute_book_state',
        selection=[
            ("available", "Available"),
            ("not_available", "Not Available"),
        ],
        string="Status",
        required=True,
        copy=False,
        default="available",
    )
    copies_of_book = fields.Integer(string='Available Copies ')
    stock_of_copies = fields.Integer(string='Stock')
    borrow_ids = fields.One2many('book.borrow','book_id')
    genre_ids = fields.Many2many('book.genre',string="Genre")
    manager_id = fields.Many2one('res.users',string='Manager',related='genre_ids.manager_id')
    @api.depends('book_state','copies_of_book')
    def _compute_book_state(self):
        for record in self:
            if record.copies_of_book == 0:
                return record.write({'book_state': 'not_available'})
            else:
                return record.write({'book_state': 'available'})

    @api.constrains('copies_of_book','stock_of_book')
    def _constraints_check_available_copy(self):
        if self.copies_of_book>self.stock_of_copies:
            raise ValidationError(_('Copies of book cannot greater than Stock '))





