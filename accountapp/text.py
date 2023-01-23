def message(domain, uidb64, token):
    email_body = f"""\
    <html>
      <head></head>
      <body>
        <div>
            <h2>Giganpyo 회원가입</h2>
        </div>
        
        <div>
            <p>지간표 </p>
            <h5>회원인증 메일입니다.</h5>
            <p>다음 링크를 클릭하시면 회원가입이 완료됩니다.</p>
            <a href="http://127.0.0.1:8000/api/user/activate/{uidb64}/{token}">http://127.0.0.1:8000/api/user/activate/{uidb64}/{token}\n\n</a>
        </div>
        
        
      </body>
    </html>
    """
    
    return email_body

from django.core.mail import EmailMessage


def send_verification_email(title="이메일 인증을 완료해주세요", data=None, to=None):
    mail_title      = "[Giganpyo] 이메일 인증을 완료해주세요"
    mail_to         = "jclee0109@gist.ac.kr"
    token           = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoxOX0.gUopTgRypigNOjP5uRZGRxYa8TKL_dyXp5ceEyEw3Uk"
    
    data = message("127.0.0.1:8000", 19, token)
    email = EmailMessage(
        mail_title, 
        data, 
        to = [mail_to])
    email.content_subtype = "html"
    print(email.send())
    return