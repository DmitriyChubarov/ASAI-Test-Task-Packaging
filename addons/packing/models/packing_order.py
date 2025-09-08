from odoo import models, fields

class PackingOrder(models.Model):
    _name = 'packing.order'
    _description = 'Packing Order'

    name = fields.Char(string='Номер заказа', required=True)
    operator_name = fields.Char(string='ФИО упаковщика')
    detail = fields.Many2many('packing.detail', 'packing_order_detail_rel', 'order_id', 'detail_id', string='Деталь')
    packed_detail = fields.Many2many('packing.detail',  'packing_order_packed_detail_rel', 'order_id', 'detail_id', string='Упакованная деталь')
    state = fields.Selection([
        ('draft', 'В ожидании'),
        ('in_progress', 'В процесее'),
        ('done', 'Собран'),
        ('rejected', 'Отклонено'),
    ], default='draft', string='Статус')
    rejection_reason = fields.Text(string='Причина отклонения')

    def _recompute_state_after_move(self):
        for order in self:
            if order.detail and order.state == 'draft':
                order.state = 'in_progress'
            if not order.detail and order.packed_detail:
                order.state = 'done'

    def action_start_packing(self):
        self.state = 'in_progress'

    def action_reject_order(self):
        self.state = 'rejected'

    def action_import_csv(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Импорт CSV',
            'res_model': 'import.csv.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_order_id': self.id},
        }



