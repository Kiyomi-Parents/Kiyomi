from sqlalchemy.orm import Session


class BaseUnitOfWork:
    _session: Session

    def __init__(self, session: Session):
        self._session = session

    async def save_changes(self):
        async with self._session.begin():
            await self._session.commit()
