from typing import Optional
from sqlmodel import Session, select
from app.models.user import AppUser
from app.utils.security import verify_password


def authenticate_user(user_or_email: str, password: str, session: Session) -> Optional[AppUser]:
    """
    Autentica un usuario verificando sus credenciales.
    Busca el usuario por nombre de usuario o email y verifica la contraseña.

    Args:
        user_or_email: Nombre de usuario o email
        password: Contraseña en texto plano
        session: Sesión de base de datos

    Returns:
        AppUser si las credenciales son correctas, None si no
    """
    # Buscar usuario por nombre de usuario o email
    user = session.exec(
        select(AppUser).where(
            (AppUser.user == user_or_email) | (AppUser.email == user_or_email)
        )
    ).first()

    # Si no existe el usuario, retornar None
    if not user:
        return None

    # Verificar si el usuario está activo
    if user.is_active == 0:
        return None

    # Verificar la contraseña
    if not verify_password(password, user.password):
        return None

    return user