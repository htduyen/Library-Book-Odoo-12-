# from odoo import api, fields, models
#
#
# class Writer(models.Model):
#     _name = 'library.book.writer'
#     _description = 'Writer'
#     _parent_store = True
#
#     name = fields.Char(translate=True, required=True)
#     # Hierarchy fields
#     book_ids = fields.Many2many(
#         'library.book', string='Writered Books')
#     # writer_ids = fields.Many2many('library.book', string='Authors')
