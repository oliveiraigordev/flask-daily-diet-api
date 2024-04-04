from uuid import uuid1
from sqlalchemy.dialects.postgresql import UUID
from database import db


class Diet(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid1())
    username = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=False)
    datetime = db.Column(db.DateTime, nullable=False)
    is_diet = db.Column(db.Boolean, nullable=False)
