from sqlalchemy.orm import Session


class BaseUnitOfWork:
    def __init__(self, session: Session):
        self.session = session

    def save_changes(self):
        self.session.commit()
