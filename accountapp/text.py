def message(domain, uidb64, token):
    email_body = f"https://www.giganpyo.com/user/activate/{uidb64}/{token}"
    
    return email_body
