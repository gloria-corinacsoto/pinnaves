from odoo import models, fields, api
from odoo.exceptions import ValidationError  


class Seguimiento(models.Model):
    _name = "pin_naves.seguimiento"
    _description = "Seguimiento Pin Naves"

    cliente_id = fields.Many2one('pin_naves.cliente', string="Cliente", required=True)
    presupuesto_id = fields.Many2one('pin_naves.presupuesto', string="Presupuesto", required=True)
    fechaContacto = fields.Datetime(string="Fecha de Contacto", required=True)
    fechaInscripcion = fields.Datetime(string="Fecha de Inscripción", default=fields.Datetime.now)
    medioContacto = fields.Selection([('telefono', 'Teléfono'), ('email', 'Email'), ('reunion', 'Reunión'), ('redes_sociales', 'Redes Sociales')], string="Medio de Contacto", required=True)
    estadoSeguimiento = fields.Selection([('pendiente', 'Pendiente'), ('en_proceso', 'En Proceso'), ('completado', 'Completado')], string="Estado Seguimiento", default='pendiente')
    estadoCliente = fields.Selection([('interesado', 'Interesado'), ('no_interesado', 'No Interesado')], string="Estado Cliente", required=True)
    notasSeguimiento = fields.Text(string="Notas de Seguimiento")
    dias_transcurridos = fields.Integer(string="Días desde el Contacto", compute="_compute_dias_transcurridos")

    # (Date): 
    fechaProximoContacto = fields.Date(string="Próximo Contacto", default=fields.Date.today)
    # (Binary):
    imagenSeguimiento = fields.Binary(string="Imagen / Captura", attachment=True)
    # (Boolean):
    esUrgente = fields.Boolean(string="Urgente", default=False)
    # (Integer): 
    duracionMinutos = fields.Integer(string="Duración (minutos)", default=0)

   
   
    @api.depends('fechaContacto')
    def _compute_dias_transcurridos(self):
        for record in self:
            if record.fechaContacto:
                record.dias_transcurridos = (fields.Datetime.now() - record.fechaContacto).days
            else:
                record.dias_transcurridos = 0

   
    # .date() convierte el Datetime en Date para poder compararlos.
    @api.constrains('fechaContacto', 'fechaProximoContacto')
    def _check_fecha_proximo_contacto(self):
        for record in self:
            if record.fechaContacto and record.fechaProximoContacto:
                if record.fechaProximoContacto < record.fechaContacto.date():
                    raise ValidationError("El próximo contacto no puede ser anterior a la fecha de contacto.")

    
    # Protege la coherencia de las dos relaciones Many2one.
    @api.constrains('cliente_id', 'presupuesto_id')
    def _check_cliente_presupuesto(self):
        for record in self:
            if record.cliente_id and record.presupuesto_id:
                if record.presupuesto_id.cliente_id != record.cliente_id:
                    raise ValidationError("El presupuesto seleccionado no pertenece a ese cliente.")

    # al elegir presupuesto, se rellena solo el cliente.
    @api.onchange('presupuesto_id')
    def _onchange_presupuesto_id(self):
        if self.presupuesto_id:
            self.cliente_id = self.presupuesto_id.cliente_id
        else:
            self.cliente_id = False

   
    def action_marcar_completado(self):
        for record in self:
            record.estadoSeguimiento = 'completado'
        return True

    
    def action_poner_en_proceso(self):
        for record in self:
            record.estadoSeguimiento = 'en_proceso'
        return True