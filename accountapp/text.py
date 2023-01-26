def message(domain, uidb64, token):
    email_body = f"http://http://ec2-54-180-104-168.ap-northeast-2.compute.amazonaws.com/api/user/activate/{uidb64}/{token}"
    
    return email_body