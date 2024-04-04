from uuid import uuid1
from flask_login import UserMixin
from sqlalchemy.dialects.postgresql import UUID
from database import db


class User(db.Model, UserMixin):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid1())
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    role = db.Column(db.String(80), nullable=False, default='user')
