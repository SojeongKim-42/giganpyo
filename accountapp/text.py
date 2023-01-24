def message(domain, uidb64, token):
    email_body = f"http://127.0.0.1:8000/api/user/activate/{uidb64}/{token}"
    
    return email_body