import csv
import base64
from odoo import models, fields, api

class ImportCSVWizard(models.TransientModel):
    _name = 'import.csv.wizard'
    _description = 'Импорт заказа из CSV'

    file = fields.Binary('CSV File', required=True)
    filename = fields.Char('Filename')
    order_id = fields.Many2one('packing.order', string='Заказ', default=lambda self: self.env.context.get('default_order_id'))

    def import_csv(self):
        data = base64.b64decode(self.file)
        reader = csv.DictReader(data.decode('utf-8').splitlines())
        order = self.order_id
        for row in reader:
            detail_code = row.get('code')
            detail = self.env['packing.detail'].search([('code', '=', detail_code)], limit=1)
            if not detail:
                detail = self.env['packing.detail'].create({
                    'name': row.get('name'),
                    'code': detail_code,
                    'weight': float(row.get('weight') or 0),
                })
            if order:
                order.detail = [(4, detail.id)]
        return {'type': 'ir.actions.act_window_close'}
