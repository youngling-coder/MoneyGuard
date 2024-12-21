class EmailTemplates:
    SIGNATURE = """
Sincerely, 
Your MoneyGuard Team
"""

    SIGNUP_EMAIL_VERIFICATION_TEMPLATE = f"""\
Welcome to MoneyGuard! We are thrilled to have you on board.  

To get started, please follow these simple steps:

1. Log in to your account.  
2. Confirm your email by clicking the link below:  
    http://localhost:8000email_confirmation_url
3. Begin using MoneyGuard to manage and safeguard your finances!  

{SIGNATURE}
"""

    EMAIL_VERIFICATION_TEMPLATE = f"""\
We have updated your email address as requested.

To complete this process, please confirm your new email by clicking the link below:
    http://localhost:8000email_confirmation_url

If you did not request this update, please follow these steps to secure your account:  

1. Log in to your account immediately and change your email
2. Reset your password to protect your account
3. Contact our support team if you suspect unauthorized activity or have any problems accessing your account.

If you do not have a MoneyGuard account, please ignore this email.  

{SIGNATURE}
"""

    SECURITY_CODE_SESSION_REQUEST_TEMPLATE = f"""\
A verification code was requested for your MoneyGuard account. 
If you made this request, please use the verification code below to proceed:
    
    security_code

If you did not request this code, please choose and follow on of these steps to secure your account:

    1. Log in to your account immediately and change your password.
    2. Contact our support team if you suspect unauthorized activity.

If you do not have a MoneyGuard account, please ignore this email.

{SIGNATURE}
"""
