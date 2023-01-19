from odoo import models, Command, fields


class BookBorrow(models.Model):
    _inherit = "book.borrow"
    move_id = fields.Many2one('account.move')

    def action_return(self):
        res = super().action_return()
        journal = self.env["account.journal"].search([("type", "=", "sale")], limit=1)
        for record in self:
            if record.fine > 0:
                move_id = self.env["account.move"].create(
                    {
                        'partner_id': record.reader_id.id,
                        'move_type': "out_invoice",
                        "journal_id": journal.id,
                        "invoice_line_ids": [
                             (0, 0, {
                                 'name': x.name,
                                 'quantity':1.0,
                                 'price_unit': record.fine
                             }) for x in record.book_id
                        ],
                    }
                )
                record.move_id = move_id
        return res
