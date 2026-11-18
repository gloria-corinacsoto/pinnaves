{
    'name': 'Gestión de Ventas Pinnaves',
    'summary': 'Módulo creado para el desafío',
    'description': 'Basada en la gestión de ventas de la empresa ficticia Pinnaves',
    'author': "Gloria Corina Colmenarez Soto",
    'website': "https://www.linkedin.com/in/gloria-colmenarez-soto-2a0b4b1b3/",
    'category': 'Sales',
    'version': '1.1',
    # Es la dependencia mínima y siempre está
    'depends': ['base'],

    'data': [
        'security/ir.model.access.csv',
        'views/cliente_views.xml',
        'views/presupuesto_views.xml',
        'views/seguimiento_views.xml',
    ],

    # Datos de prueba: solo se cargan si la base de datos tiene demo activado
    'demo': [
        'demo/demo.xml',
    ],

    'installable': True,
    'application': True,
}