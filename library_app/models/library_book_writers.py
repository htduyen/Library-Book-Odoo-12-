from odoo import api, fields, models, _


class Writer(models.Model):
    _name = 'library.book.writers'
    _description = 'Writer'
    _order = 'name'

    name = fields.Char(translate=True, required=True)

    book_ids = fields.Many2many(
        'library.book', string='Writered Books')

    create_date = fields.Date('Create date', default = fields.Date.today())

    image = fields.Binary('Image')

    descr = fields.Html('Description')

    birthday = fields.Date('Birthday')

    code_writer = fields.Char(string='Code Writer', required=True, copy=False, readonly=True,
                   index=True, default=lambda self: _('New'))

    @api.model
    def create(self, vals):
        vals['code_writer'] = self.env['ir.sequence'].next_by_code('increment_code_writer') or _('New')
        res = super().create(vals)
        return res

    book_type = fields.Selection(
        [('comic', 'Comic book'),
         ('drama', 'Drama'),
         ('romance', 'Romance'),
         ('cookbook', 'Cookbook'),
         ('graphic', 'Graphic novel'),
         ('action', 'Action and adventure'),
         ('horror', 'Horror')],
        'Type book',
        default='cookbook')

    slogan = fields.Html('Slogan')

    state = fields.Selection(string="Active", selection=[('active', 'active'), ('inactive', 'inactive'), ], required=False, )

    # @api.model
    # def create(self, vals):
    #     name = vals.get('name')
    #     new_name = name.title()
    #     vals['name'] = new_name
    #     return super().create(vals)

    _sql_constraints = [
        ('library_book_name_writer',
         'UNIQUE (name)',
         'This name already, Name of writer must be unique.')
    ]