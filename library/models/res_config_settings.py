from odoo import fields, models, api, _



class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'


    penalty_amount = fields.Float(config_parameter='library.penalty_amount')
    max_day = fields.Integer(config_parameter='library.max_day')


