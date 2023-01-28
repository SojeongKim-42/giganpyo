def message(domain, uidb64, token):
    email_body = f"https://api.giganpyo.com/api/user/activate/{uidb64}/{token}"
    
    return email_body
