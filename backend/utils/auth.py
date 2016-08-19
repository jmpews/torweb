from db.mysql_model.user import User


class Auth:
    authorizations = {
    }

    @staticmethod
    def auth_add_poc(user):
        if user.is_checker():
            return True
        return False
