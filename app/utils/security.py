import bcrypt

def hash_password(password: str) -> str:
    """
    Hash de una contraseña usando bcrypt.
    Bcrypt tiene un límite de 72 bytes, por lo que truncamos la contraseña si es necesaria.
    """
    # Convertir la contraseña a bytes y truncar a 72 bytes (límite de bcrypt)
    password_bytes = password.encode('utf-8')[:72]

    # Generar el hash
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)

    # Retornar como string
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica que una contraseña coincida con su hash.
    """
    # Truncar la contraseña a 72 bytes (límite de bcrypt)
    password_bytes = plain_password.encode('utf-8')[:72]
    hashed_bytes = hashed_password.encode('utf-8')

    # Verificar la contraseña
    return bcrypt.checkpw(password_bytes, hashed_bytes)
