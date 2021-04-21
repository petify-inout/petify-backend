from petapp import db

class Disease(db.Model):
    id = db.Column(db.Integer , primary_key=True )
    name = db.Column(db.String(20), unique=True, nullable=False)
    description = db.Column(db.Text)
    symptoms = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"User('{self.name}','{self.symptoms}')"