from odoo import api, fields, models, _


class BookCategory(models.Model):
    _name = 'library.book.category'
    _description = 'Book Category'
    _parent_store = True

    name = fields.Char(translate=True, required=True)
    # Hierarchy fields
    parent_id = fields.Many2one(
        'library.book.category',
        string='Parent Category',
        ondelete='restrict',
    )
    parent_path = fields.Char(index=True)

    # Optional, but good to have
    child_ids = fields.One2many(
        'library.book.category',
        'parent_id',
        string='Subcategories',
    )

    highlighted_id = fields.Reference(
        [('library.book', 'Book'),
         ('res.partner', 'Author')],
        'Category Highlight',
    )
    show = fields.Boolean(string="Show?",default = True)

    book_ids = fields.One2many('library.book','category_id',string = 'Books')

    description1 = fields.Char(string="Description")
    # abc = fields.Char(string="ABC", required=False,)

    # web = fields.Html('Html')

    currency_id = fields.Many2one('res.currency')

    @api.multi
    def write(self, vals):
        if 'description1' in vals:
            description = vals.get('description1')
            list_id = self.book_ids
            for book in list_id:
                book.write({'descr': description})
        # super().write(vals)
        if 'currency_id' in vals:
            currency = vals.get('currency_id')
            list_id = self.book_ids
            for book in list_id:
                book.write({'currency_id': currency})
        super().write(vals)
        return True

