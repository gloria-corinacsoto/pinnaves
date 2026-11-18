import re
from odoo import models, fields, api
from datetime import date
from odoo.exceptions import ValidationError


class Cliente(models.Model):
    _name = "pin_naves.cliente"
    _description = "Cliente Pin Naves"
    _rec_name = "nombreCompletoCliente"

    # Relaciones (lado "uno")
    presupuesto_ids = fields.One2many('pin_naves.presupuesto', 'cliente_id', string="Presupuestos")
    seguimiento_ids = fields.One2many('pin_naves.seguimiento', 'cliente_id', string="Seguimientos")

    # Campos principales
    nombreCliente = fields.Char(string="Nombre Cliente", required=True)
    apellidoCliente = fields.Char(string="Apellido Cliente", required=True)
    nombreCompletoCliente = fields.Char(string="Nombre Completo", compute="_compute_nombre_completo", store=True)
    documentoIdentidadCliente = fields.Selection([('dni', 'DNI'), ('nie', 'NIE'), ('pasaporte', 'Pasaporte')], string="Documento", required=True)
    fechaNacimientoCliente = fields.Date(string="Fecha de Nacimiento", required=True)
    edadCliente = fields.Integer(string="Edad Cliente", compute="_compute_edad")
    estadoCivilCliente = fields.Selection([('soltero', 'Soltero'), ('casado', 'Casado'), ('divorciado', 'Divorciado')], string="Estado Civil", required=True)
    sexoCliente = fields.Selection([('masculino', 'Masculino'), ('femenino', 'Femenino')], string="Sexo", required=True)
    emailCliente = fields.Char(string="Email Cliente", required=True)
    telefonoCliente = fields.Char(string="Teléfono Cliente", required=True)
    fechaRegistroCliente = fields.Datetime(string="Fecha de Registro", default=fields.Datetime.now)
    medioContactoCliente = fields.Selection([('telefono', 'Teléfono'), ('email', 'Email'), ('reunion', 'Reunión'), ('redes_sociales', 'Redes Sociales')], string="Medio de Contacto", required=True)
    observacionesCliente = fields.Text(string="Observaciones")
    aceptaComunicacionesCliente = fields.Boolean(string="Acepta comunicaciones", default=True)
    presupuestosCount = fields.Integer(string="Nº Presupuestos", compute="_compute_presupuestos_count")

    imagenCliente = fields.Binary(string="Imagen / Foto", attachment=True)

    @api.depends('nombreCliente', 'apellidoCliente')
    def _compute_nombre_completo(self):
        for cliente in self:
            if cliente.nombreCliente and cliente.apellidoCliente:
                cliente.nombreCompletoCliente = f"{cliente.nombreCliente} {cliente.apellidoCliente}"
            else:
                cliente.nombreCompletoCliente = "No especificado"

    @api.depends('fechaNacimientoCliente')
    def _compute_edad(self):
        for cliente in self:
            if cliente.fechaNacimientoCliente:
                hoy = date.today() 
                nac = cliente.fechaNacimientoCliente
                cliente.edadCliente = hoy.year - nac.year - ((hoy.month, hoy.day) < (nac.month, nac.day))
            else:
                cliente.edadCliente = 0

    @api.depends('presupuesto_ids')
    def _compute_presupuestos_count(self):
        for cliente in self:
            cliente.presupuestosCount = len(cliente.presupuesto_ids)

    
    @api.constrains('fechaNacimientoCliente')
    def _check_fecha_nacimiento(self):
        for cliente in self:
            if cliente.fechaNacimientoCliente and cliente.fechaNacimientoCliente > fields.Date.today():
                raise ValidationError("La fecha de nacimiento no puede ser futura.")

    @api.constrains('emailCliente')
    def _check_email(self):
        for cliente in self:
            if cliente.emailCliente and not re.match(r"[^@\s]+@[^@\s]+\.[^@\s]+$", cliente.emailCliente):
                raise ValidationError("El email no tiene un formato válido.")

  
    @api.onchange('emailCliente')
    def _onchange_email(self):
        if self.emailCliente:
            self.emailCliente = self.emailCliente.strip().lower()

   
    def action_ver_presupuestos(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Presupuestos',
            'res_model': 'pin_naves.presupuesto',
            'view_mode': 'list,form',
            'domain': [('cliente_id', '=', self.id)],
            'context': {'default_cliente_id': self.id},
        }