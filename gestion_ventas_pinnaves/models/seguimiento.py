from odoo import models, fields, api

class seguimiento(models.Model):
    _name = "pin_naves_seguimiento"
    _descripcion= "clasepinnaves_seguimiento"

    cliente_id = fields.Many2one('pin_naves', string="Cliente", required=True, help="Seleccione el cliente asociado al seguimiento")
    presupuesto_id = fields.Many2one('pin_naves_presupuesto', string="Presupuesto", required=True, help="Seleccione el presupuesto asociado al seguimiento")
    fechaContacto = fields.Datetime(string="Fecha de Contacto", required=True, help="Ingrese la fecha de contacto con el cliente")
    fechaAInscripcion = fields.Datetime(string="Fecha de Inscripción", default=fields.Datetime.now, help="Fecha de inscripción del cliente")
    medioContacto = fields.Selection([('telefono', 'Teléfono'), ('email', 'Email'), ('reunion', 'Reunión'), ('redes_sociales', 'Redes Sociales')], string="Medio de Contacto", required=True, help="Seleccione el medio de contacto con el cliente") 
    estadoSeguimiento = fields.Selection([('pendiente', 'Pendiente'), ('en_proceso', 'En Proceso'), ('completado', 'Completado')], string="Estado Seguimiento", default='pendiente', help="Seleccione el estado del seguimiento")
    estadocliente = fields.Selection([('interesado', 'Interesado'), ('no_interesado', 'No Interesado')], string="Estado Cliente", required=True, help="Seleccione el estado del cliente")   
    notasSeguimiento = fields.Text(string="Notas de Seguimiento", help="Ingrese las notas del seguimiento")
