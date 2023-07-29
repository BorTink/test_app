from app import db
from loguru import logger

class Courses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    topic = db.Column(db.String(150))
    field = db.Column(db.String(150))
    university = db.Column(db.String(150))

    def __repr__(self):
        return f"<courses {self.id}"

if __name__ == "__main__":
    print(1)
    logger.info('DSGSGDSG')
    print(Courses.query.all())