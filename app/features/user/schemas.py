from sqlmodel import SQLModel


class ChangePasswordSchema(SQLModel):
    old_password: str
    new_password: str
    confirm_new_password: str
