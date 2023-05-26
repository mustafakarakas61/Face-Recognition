import bcrypt


def hash_password(password):
    # Şifreyi hash'e dönüştürme
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    return hashed_password.decode('utf-8')


def check_password(password, hashed_password):
    # Girilen şifrenin hash değerini kontrol etme
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
