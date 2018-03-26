from validate_email import validate_email


def check_name(name):
    if len(name) > 20:
        return False
    return True


def check_number(number):
    if not number.isdigit() or len(number) > 15:
        return False
    return True


def check_address(address):
    if len(address) > 140:
        return False
    return True


def check_email(email):
    if not validate_email(email) or len(email) > 80:
        return False
    return True
