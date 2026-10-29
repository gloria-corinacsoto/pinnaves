from odoo import models, fields, api

class Presupuesto(models.Model):
    _name = "pin_naves_presupuesto"
    _descripcion= "clasepinnaves_presupuesto"

    cliente_id = fields.Many2one('pin_naves', string="Cliente", required=True, help="Seleccione el cliente asociado al presupuesto")
    nombrePresupuesto = fields.Char(string="Nombre Presupuesto", required=True, help="Ingrese el nombre del presupuesto")
    descripcionPresupuesto = fields.Text(string="Descripción Presupuesto", required=True, help="Ingrese la descripción del presupuesto")
    fechaCreacionPresupuesto = fields.Datetime(string="Fecha de Creación", default=fields.Datetime.now, help="Fecha de creación del presupuesto")
    fechaVencimientoPresupuesto = fields.Date(string="Fecha de Vencimiento", required=True, help="Ingrese la fecha de vencimiento del presupuesto")
    estadoPresupuesto = fields.Selection([('pendiente', 'Pendiente'), ('aprobado', 'Aprobado'), ('rechazado', 'Rechazado')], string="Estado Presupuesto", default='pendiente', help="Seleccione el estado del presupuesto")
    precioUnitarioPresupuesto = fields.Float(string="Precio Unitario", required=True, help="Ingrese el precio unitario del presupuesto")
    cantidadPresupuesto = fields.Integer(string="Cantidad", required=True, help="Ingrese la cantidad del presupuesto")
    importePresupuesto = fields.Float(string="Importe Presupuesto", compute="_compute_importe_presupuesto", store=True, help="Ingrese el importe del presupuesto")
    totalPresupuesto = fields.Float(string="Total Presupuesto", compute="_compute_total_presupuesto", store=True, help="Total del presupuesto calculado automáticamente")

    def _compute_importe_presupuesto(self):
        for record in self:
            record.importePresupuesto = record.precioUnitarioPresupuesto * record.cantidadPresupuesto

    def _compute_total_presupuesto(self):
        for record in self:
            record.totalPresupuesto = record.importePresupuesto