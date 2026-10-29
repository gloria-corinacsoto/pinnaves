from odoo import models,fields, date, api

class Cliente(models.Model):
    _name = "pin_naves"
    _descripcion= "clasepinnaves"

    nombreCliente = fields.char(string="Nombre Cliente", required=True, help="Ingrese el nombre del cliente")
    apellidoCliente = fields.char(string="Apellido Cliente", required=True, help="Ingrese el apellido del cliente") 
    DocumentoIdentidadCliente = fields.Selection([('dni', 'DNI'),('nie', 'NIE'), ('pasaporte', 'Pasaporte')], string="Documento", required=True, help="Seleccione el documento del cliente")
    edadCliente = fields.Integer(string="Edad Cliente", required=True, help="Ingrese la edad del cliente")  
    estadoCivilCliente = fields.Selection([('soltero', 'Soltero'), ('casado', 'Casado'), ('divorciado', 'Divorciado')], string="Estado Civil", required=True, help="Seleccione el estado civil del cliente")    
    edadCliente = fields.Integer(string="Edad Cliente", required=True, help="Ingrese la edad del cliente")
    fechaNacimientoCliente = fields.Date(string="Fecha de Nacimiento", required=True, help="Ingrese la fecha de nacimiento del cliente")
    sexoCliente = fields.Selection([('masculino', 'Masculino'), ('femenino', 'Femenino')], string="Sexo", required=True, help="Seleccione el sexo del cliente") 
    emailCliente = fields.Char(string="Email Cliente", required=True, help="Ingrese el email del cliente")
    telefonoCliente = fields.Char(string="Teléfono Cliente", required=True, help="Ingrese el teléfono del cliente")
    fechaRegistroCliente = fields.Datetime(string="Fecha de Registro", default=fields.Datetime.now, help="Fecha de registro del cliente")   
    