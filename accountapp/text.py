def message(domain, uidb64, token):
    email_body = f"{domain}/user/activate/{uidb64}/{token}"
    
    return email_body
