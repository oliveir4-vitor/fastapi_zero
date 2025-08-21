from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from fastapi_zero.settings import Settings

engine = create_engine(Settings().DATABASE_URL)

session = Session(engine)


def get_session():
    with Session(engine) as session:
        """
            yield ao invés de return;
            com yield a condição é mantida até ser concluída, estão é encerrada
        """
        yield session
