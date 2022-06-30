from itsdangerous import URLSafeTimedSerializer
from datetime import datetime

def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer("sfrfdslfdmsjcmxvcçxömvcx")
    now = datetime.now()
    email+="-"+now.strftime("%d/%m/%Y %H:%M:%S")
    return serializer.dumps(email, salt="sfrfdfdsfd?+%+=^?dslfdmsjcmxvcçxömvcx")


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer("sfrfdslfdmsjcmxvcçxömvcx")
    try:
        email = serializer.loads(
            token,
            salt="sfrfdfdsfd?+%+=^?dslfdmsjcmxvcçxömvcx",
            max_age=expiration
        )
    except:
        return False
    return email