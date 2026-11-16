class UsuarioYaExiste(Exception):
    """Excepción lanzada cuando se intenta crear un usuario que ya existe."""
    pass


class CredencialesInvalidas(Exception):
    """Excepción lanzada cuando las credenciales proporcionadas son inválidas."""
    pass

class UsuarioInactivo(Exception):
    """Excepción lanzada cuando se intenta autenticar un usuario que está inactivo."""
    pass