from odoo import api, fields, models


class Writer(models.Model):
    _name = 'library.book.writers'
    _description = 'Writer'
    _order = 'name'

    name = fields.Char(translate=True, required=True)

    book_ids = fields.Many2many(
        'library.book', string='Writered Books')

    create_date = fields.Date('Create date')
    image = fields.Binary('Image')



    @api.model
    def create(self, vals):
        name = vals.get('name')
        new_name = name.title()
        vals['name'] = new_name
        return super(Writer , self).create(vals)

    _sql_constraints = [
        ('library_book_name_writer',
         'UNIQUE (name)',
         'This name already, Name of writer must be unique.')
    ]