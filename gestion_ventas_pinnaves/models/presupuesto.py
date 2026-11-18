from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Presupuesto(models.Model):
    _name = "pin_naves.presupuesto"
    _description = "Presupuesto Pin Naves"
    _rec_name = "nombrePresupuesto"

    # Relaciones
    cliente_id = fields.Many2one('pin_naves.cliente', string="Cliente", required=True, ondelete='cascade',
                                 help="Seleccione el cliente asociado al presupuesto")
    seguimiento_ids = fields.One2many('pin_naves.seguimiento', 'presupuesto_id', string="Seguimientos",
                                      help="Lista de seguimientos asociados al presupuesto")

    # Campos principales
    nombrePresupuesto = fields.Char(string="Nombre Presupuesto", required=True, help="Ingrese el nombre del presupuesto")
    descripcionPresupuesto = fields.Text(string="Descripción Presupuesto", required=True, help="Ingrese la descripción del presupuesto")
    fechaCreacionPresupuesto = fields.Datetime(string="Fecha de Creación", default=fields.Datetime.now, help="Fecha de creación del presupuesto")
    fechaVencimientoPresupuesto = fields.Date(string="Fecha de Vencimiento", required=True, help="Ingrese la fecha de vencimiento del presupuesto")
    estadoPresupuesto = fields.Selection([('pendiente', 'Pendiente'), ('aprobado', 'Aprobado'), ('rechazado', 'Rechazado')],
                                         string="Estado Presupuesto", default='pendiente', help="Estado del presupuesto")
    prioridadPresupuesto = fields.Selection([('baja', 'Baja'), ('media', 'Media'), ('alta', 'Alta')],
                                            string="Prioridad", default='media', help="Prioridad del presupuesto")
    aplicaIvaPresupuesto = fields.Boolean(string="Aplicar IVA (21%)", default=True, help="Si está marcado, el total incluye el 21% de IVA")

    # Campo BINARY para la imagen
    imagenPresupuesto = fields.Binary(string="Imagen / Plano", attachment=True)

    # Datos que escribe el usuario: SIN compute
    precioUnitarioPresupuesto = fields.Float(string="Precio Unitario", required=True, help="Ingrese el precio unitario del presupuesto")
    cantidadPresupuesto = fields.Integer(string="Cantidad", required=True, default=1, help="Ingrese la cantidad del presupuesto")

    # Campos calculados: CON compute
    importePresupuesto = fields.Float(string="Importe Presupuesto", compute="_compute_importe_presupuesto", store=True,
                                      help="Precio unitario x cantidad")
    totalPresupuesto = fields.Float(string="Total Presupuesto", compute="_compute_total_presupuesto", store=True,
                                    help="Importe más IVA si corresponde")
    diasRestantesPresupuesto = fields.Integer(string="Días restantes", compute="_compute_dias_restantes",
                                              help="Días que faltan para el vencimiento")

    # ---------- COMPUTE ----------
    @api.depends('precioUnitarioPresupuesto', 'cantidadPresupuesto')
    def _compute_importe_presupuesto(self):
        for record in self:
            record.importePresupuesto = record.precioUnitarioPresupuesto * record.cantidadPresupuesto

    @api.depends('importePresupuesto', 'aplicaIvaPresupuesto')
    def _compute_total_presupuesto(self):
        for record in self:
            if record.aplicaIvaPresupuesto:
                record.totalPresupuesto = record.importePresupuesto * 1.21
            else:
                record.totalPresupuesto = record.importePresupuesto

    @api.depends('fechaVencimientoPresupuesto')
    def _compute_dias_restantes(self):
        hoy = fields.Date.today()
        for record in self:
            if record.fechaVencimientoPresupuesto:
                record.diasRestantesPresupuesto = (record.fechaVencimientoPresupuesto - hoy).days
            else:
                record.diasRestantesPresupuesto = 0

    # ---------- CONSTRAINS ----------
    @api.constrains('cantidadPresupuesto', 'precioUnitarioPresupuesto')
    def _check_valores(self):
        for record in self:
            if record.cantidadPresupuesto <= 0:
                raise ValidationError("La cantidad debe ser mayor que 0.")
            if record.precioUnitarioPresupuesto < 0:
                raise ValidationError("El precio no puede ser negativo.")

    @api.constrains('fechaCreacionPresupuesto', 'fechaVencimientoPresupuesto')
    def _check_fechas(self):
        for record in self:
            if record.fechaCreacionPresupuesto and record.fechaVencimientoPresupuesto:
                if record.fechaVencimientoPresupuesto < record.fechaCreacionPresupuesto.date():
                    raise ValidationError("La fecha de vencimiento no puede ser anterior a la fecha de creación.")

    # ---------- ONCHANGE ----------
    @api.onchange('cliente_id')
    def _onchange_cliente_id(self):
        if self.cliente_id and not self.nombrePresupuesto:
            self.nombrePresupuesto = f"Presupuesto de {self.cliente_id.nombreCompletoCliente}"

    # ---------- ACCIONES (botones) ----------
    def action_aprobar(self):
        for record in self:
            record.estadoPresupuesto = 'aprobado'

    def action_rechazar(self):
        for record in self:
            record.estadoPresupuesto = 'rechazado'