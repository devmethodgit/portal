from database.database import db


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.Text, nullable=False)

    def __str__(self):
        return f"User: id={self.id}, username={self.username}"
