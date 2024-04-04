from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def db_create(obj):
    db.session.add(obj)
    db.session.commit()
    return True


def db_delete(obj):
    db.session.delete(obj)
    db.session.commit()
    return True
