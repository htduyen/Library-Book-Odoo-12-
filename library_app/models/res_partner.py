from odoo import fields, models, _


class Partner(models.Model):
    _inherit = 'res.partner'

    published_book_ids = fields.One2many(
        'library.book',  # related model
         'publisher_id',  # field for "this" on related model
        string='Published Books')

    book_ids = fields.Many2many(
        'library.book',
        'author_ids', # new line
        string='Authored Books')
