from django.http import JsonResponse


def UserDoesNotExist(status: int = 400, email=None):
    message = "등록된 회원이 존재하지 않습니다. 회원가입을 먼저 진행해주세요."
    location = ""
    param = ""
    value = email
    error = "UserDoesNotExist"
    msg = "User Does Not Exist"

    detail = {"location": location,
              "param": param,
              "value": value,
              "error": error,
              "msg": msg}

    errors = {
        "message": message,
        "detail": detail
    }
    print(errors)
    return JsonResponse(errors, status=status)


def UserAlreadyExist(status: int = 400, email=None, social_provider=None):
    message = f"이미 {social_provider}로 가입된 유저입니다. {social_provider}로그인을 진행해주세요."
    location = ""
    param = ""
    value = email
    error = "UserAlreadyExist"
    msg = "User Already Exist"

    detail = {"location": location,
              "param": param,
              "value": value,
              "error": error,
              "msg": msg}

    errors = {
        "message": message,
        "detail": detail
    }
    print(errors)
    return JsonResponse(errors, status=status)


def SocialLoginFailed(status: int = 400, social_provider=None):
    message = f"{social_provider}로그인에 실패하였습니다. 로그인을 다시 진행해주세요."
    location = ""
    param = ""
    value = social_provider
    error = "SocialLoginFailed"
    msg = "Social Login Failed"

    detail = {"location": location,
              "param": param,
              "value": value,
              "error": error,
              "msg": msg}

    errors = {
        "message": message,
        "detail": detail
    }
    print(errors)
    return JsonResponse(errors, status=status)

def AccountWithdrawalPermissionError(status: int = 403):
    message = "계정 탈퇴는 본인만 할 수 있습니다."
    location = ""
    param = ""
    value = ""
    error = "AccountWithdrawalFailed"
    msg = "Account Withdrawal is Failed"

    detail = {"location": location,
              "param": param,
              "value": value,
              "error": error,
              "msg": msg}

    errors = {
        "message": message,
        "detail": detail
    }
    print(errors)
    return JsonResponse(errors, status=status)