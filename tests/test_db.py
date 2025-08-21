from dataclasses import asdict

from sqlalchemy import select

from fastapi_zero.models import User


def test_create_user(session, mock_db_time):
    with mock_db_time(model=User) as time:
        new_user = User(
            username='test', email='test@mail.com', password='secret'
        )

        session.add(new_user)
        session.commit()

    # scalar tranforma td que veio do banco em objeto python
    user = session.scalar(select(User).where(User.username == 'test'))

    assert asdict(user) == {
        'id': 1,
        'username': 'test',
        'email': 'test@mail.com',
        'password': 'secret',
        'created_at': time,
        'updated_at': time,
    }
