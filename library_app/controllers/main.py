from odoo import http


class Books(http.Controller):

    @http.route('/library/books', auth='public')
    def list(self, **kwargs):
        Book = http.request.env['library.book']
        books = Book.search([])
        return http.request.render(
            'library_app.book_list_template',
            {'books': books})
