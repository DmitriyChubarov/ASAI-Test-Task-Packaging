from odoo import models, fields

class PackingDetail(models.Model):
    _name = 'packing.detail'
    _description = 'Packing Detail'

    name = fields.Char(string='Название детали', required=True)
    code = fields.Char(string='Номер детали', required=True)
    weight = fields.Float(string='Вес', digits=(6, 2))

    def action_pack_for_order(self):
        order_id = self.env.context.get('order_id')
        if not order_id:
            return
        order = self.env['packing.order'].browse(order_id)
        for detail in self:
            if detail.id not in order.packed_detail.ids:
                order.packed_detail = [(4, detail.id)]
            order.detail = [(3, detail.id)]
        order._recompute_state_after_move()
