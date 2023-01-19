from odoo import api, fields, models, _
from datetime import datetime, timedelta
from odoo.exceptions import *
from dateutil.relativedelta import relativedelta


class BookBorrow(models.Model):
    _name = "book.borrow"
    _description = "borrow data details"
    _rec_name = 'id'

    _sql_constraints = [
        ("check_validity", 'CHECK(validity > 0)', "Validity should be more than 1 day"),

    ]
    name = fields.Char(string='Borrow Data ID', copy=False, readonly=True)
    reader_id = fields.Many2one('res.partner', string='Reader', required=True,
                                domain=[('is_library_member', '=', True)])
    book_id = fields.Many2many('book.details', string='Book', required=True,ondelete='cascade')
    date_of_borrow = fields.Date(default=datetime.today(), string='Date of borrow')
    fine = fields.Integer(string='penalty(per book)', readonly=True)
    validity = fields.Integer(required=True, default=1, string='Validity')
    deadline = fields.Date(compute='_compute_deadline', readonly=True)
    return_date = fields.Date(string='Return date', readonly=True)
    current_date = fields.Date(default=datetime.today())
    borrow_state = fields.Selection(
        selection=[
            ('new', 'New'),
            ("taken", "Taken"),
            ('returned', 'Returned')
        ],
        string="Status",
        copy=False,
        default='new'
    )

    @api.depends('validity', 'date_of_borrow')
    def _compute_deadline(self):
        for record in self:
            record.deadline = record.date_of_borrow + timedelta(days=record.validity)

    @api.constrains('validity')
    def _constrains_check_validity(self):
        max_day = self.env['ir.config_parameter'].sudo().get_param('library.max_day')
        if self.validity > int(max_day):
            raise ValidationError(_('Max day of validity is less than provide data.'))

    @api.constrains('current_date', 'date_of_borrow')
    def _constrains_check_date_of_borrow(self):
        if self.date_of_borrow > self.current_date:
            raise ValidationError(_('You can not enter the date of borrow from future.'))

    def action_borrow(self):
        for book_id in self.book_id:
            domain = []
            for book_id in book_id:
                domain += [('name', '=', book_id.name)]
            book_stock = self.env['book.details'].search(domain)
            for record in book_stock:
                if record.copies_of_book > 0:
                    record.copies_of_book -= 1
                else:
                    raise ValidationError("Books are not available")
        self.write({
            'borrow_state' : 'taken'
        })



    def action_return(self):
        fine = self.env['ir.config_parameter'].sudo().get_param('library.penalty_amount')
        for book_id in self.book_id:
            domain = []
            for book_id in book_id:
                domain += [('name', '=', book_id.name)]
            book_stock = self.env['book.details'].search(domain)
            for rec in self:
                rec.return_date = datetime.today()
                if rec.return_date > rec.deadline:
                    max_days = int(self.env['ir.config_parameter'].sudo().get_param('library.max_day'))
                    fine_add_from = rec.date_of_borrow + relativedelta(days=max_days)
                    if rec.return_date > fine_add_from:
                        rec.fine = int((rec.return_date - fine_add_from).days) * float(fine)
                for record in book_stock:
                    record.copies_of_book += 1

        self.write(
            {
                'borrow_state': 'returned'
            }
        )


