from odoo import api, fields, models, _
from odoo.exceptions import Warning
from odoo.exceptions import ValidationError
from odoo.addons import decimal_precision as dp
# from odoo.tools.translate import _


class Book(models.Model):
    _name = 'library.book'
    _description = 'Book'
    _order = 'name, date_published desc'
    # _parent_store = True
    # Text fields
    name = fields.Char(
        'Title',
        default=None,
        index=True,
        help='Book cover title',
        readonly=False,
        required=True,
        translate=False,
        search='_search_function',
        filter_domain="[('name','ilike',self)]",
    )
    isbn = fields.Char('ISBN')
    book_type = fields.Selection(
        [('paper','Paperback'),
         ('hard','Hardcover'),
         ('electronic','Electronic'),
         ('other', 'Other')],
        'Type')
    notes = fields.Text('Internal Notes')
    descr = fields.Char('Description',)

    # @api.depends('category_id.description')
    # def _compute_categ_desc(self):
    #     for book in self:
    #         book.descr = book.category_id.description

    # Numeric fields
    copies = fields.Integer(default=1, size =4)
    avg_rating = fields.Float('Average Rating', (16, 4))

    @api.onchange('avg_rating')
    def _onchange_avg_rating(self):
        for book in self:
            rate = book.avg_rating
            str_rate = rate.str()
            if len(str_rate) > 4:
                raise ValidationError(_('Length this field is less than 4'))



    currency_id = fields.Many2one('res.currency')
    price = fields.Monetary('Price', 'currency_id')

    gia = fields.Float(
        'Gia', default=0.0, digits=dp.get_precision('Book Price'),
        required=True, help="The price to purchase a product")
    # Date fields
    date_published = fields.Date('Date Published')
    last_borrow_date = fields.Datetime(
        'Last Borrowed On',
        default=lambda self: fields.Datetime.now(),
    )
    
    def _default_last_borrow_date(self):
        return fields.Datetime.now()

    # Other fields
    active = fields.Boolean('Active?', default=True)
    image = fields.Binary('Cover')

    # Relational fields
    publisher_id = fields.Many2one('res.partner',  string='Publisher', search='_search_function')
    author_ids = fields.Many2many('res.partner', string='Authors')

    # new line
    writer_ids = fields.Many2many('library.book.writers', string='Writer',search='_search_function',
                          domain="[('state','=','active')]", index=True)

    count = fields.Integer(string ='Count')
    state = fields.Selection(string="State",
                             selection=[('con', 'Con'),
                                        ('het', 'Het'),
                                        ('saphet', 'Sap Het')],)


    @api.model
    def doi_trangthai(self, count):
        # Code before create: should use the `vals` dict
        if 0 < count < 10:
            self.state = 'saphet'
        elif count == 0:
            self.state = 'het'
        elif count < 0:
            raise ValidationError(_('Count is not'.format(self.count)))
        else:
            self.state = 'con'
        return True
    @api.onchange('count')
    def change_state(self):
        # for book in self:
        #     if 0 < book.count < 10:
        #         self.state = 'saphet'
        #     elif book.count == 0:
        #         self.state = 'het'
        #     elif book.count < 0:
        #         raise ValidationError(_('Count is not'.format(self.count)))
        #     else:
        #         self.state = 'con'
        self.doi_trangthai(self.count)



    @api.multi
    def _check_isbn(self):
        """Check one Book's ISBN"""
        self.ensure_one()
        digits = [int(x) for x in self.isbn if x.isdigit()]
        if len(digits) == 13:
            ponderators = [1, 3] * 6
            total = sum(a * b for a, b in zip(digits[:12], ponderators))
            remain = total % 10
            check = 10 - remain if remain != 0 else 0
            return digits[-1] == check

    @api.multi
    def button_check_isbn(self):
        for book in self:
            if not book.isbn:
                raise Warning(
                    _('Please provide an ISBN13 for %s') % book.name)
            if book.isbn and not book._check_isbn():
                raise Warning(
                    _('%s is an invalid ISBN') % book.isbn)
            if book.isbn and book._check_isbn():
                raise Warning(_('%s is an valid ISBN') % book.isbn)
        return True

    #Check ISBN
    @api.onchange('isbn')
    def _onchange_isbn_valid(self):
        for book in self:
            if book.isbn and not book._check_isbn():
                raise ValidationError(_('{0} is an invalid ISBN').format(book.isbn))

    category_id = fields.Many2one('library.book.category', string='Category')

    publisher_country_id = fields.Many2one(
        'res.country',
        string='Publisher Country',
        compute='_compute_publisher_country',
        inverse='_inverse_publisher_country',
        search='_search_publisher_country',
    )

    @api.depends('publisher_id.country_id')
    def _compute_publisher_country(self):
        for book in self:
            book.publisher_country_id = book.publisher_id.country_id


    @api.depends('publisher_country_id')
    def _inverse_publisher_country(self):
        for book in self:
            if book.publisher_id:
                book.publisher_id.country_id = book.publisher_country_id

    def _search_publisher_country(self, operator, value):
        return [('publisher_id.country_id', operator, value)]


    publisher_country_related = fields.Many2one(
        'res.country',
        string='Publisher Country (related)',
        related='publisher_id.country_id',
    )
    categ_show_related = fields.Boolean(
        string ='Categ relate',
        # store = True,
        related='category_id.show'
    )

    _sql_constraints = [
        ('library_book_name_date_uq',
         'UNIQUE (name, date_published)',
         'Book title and publication date must be unique.'),
        ('library_book_check_date',
         'CHECK (date_published <= current_date)',
         'Publication date must not be in the future.'),
    ]

    @api.model
    def create(self, vals):
        name = vals.get('name')
        new_name = name.title()
        vals['name'] = new_name
        return super().create(vals)

    @api.constrains('isbn')
    def _constrain_isbn_valid(self):
        for book in self:
            if book.isbn and not book._check_isbn():
                raise ValidationError(
                    _('%s is an invalid ISBN') % book.isbn)

    #/176