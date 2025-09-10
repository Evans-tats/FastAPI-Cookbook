from .. operations import add_user
from .. Schema import UserSchema, showUserSchema
from ..db_model import User

def test_add_user_to_DB(session):
    user = add_user(
        session=session,
        user=UserSchema(
            username="johnwick",
            email="johnwick007@gmail.com",
            password="helloimunderthewater")
        )
    assert (session.query(User).filter(User.username==user.username).first())
