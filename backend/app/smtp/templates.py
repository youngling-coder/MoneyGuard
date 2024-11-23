class EmailTemplates:
    SIGNATURE = """
Sincerely, 
Your MoneyGuard Team
"""

    SIGNUP_EMAIL_VERIFICATION_TEMPLATE = f"""\
Hello and welcome to MoneyGuard!

We are glad to inform you that you've successfully signed up!
Next steps to follow are really simple:\

1. Login into your account
2. Confirm your email using link below
    http://localhost:8000email_confirmation_url
3. Start using our application!

{SIGNATURE}
"""

    EMAIL_VERIFICATION_TEMPLATE = f"""\
The email has been updated successfully!

To confirm new email, click your email verification link below

    http://localhost:8000email_confirmation_url


{SIGNATURE}
"""
    
    RESET_PASSWORD_VERIFICATION_CODE_TEMPATE = f"""
We received a request to reset your password for your MoneyGuard account.
If you made this request, please use the verification code below to proceed:
    CODE: verification_code

If you did not request a password reset, please follow these steps to secure your account:

1. Log in to your account immediately and change your password.
2. Contact our support team if you suspect unauthorized activity.

If you do not have a MoneyGuard account, please ignore this email.  

{SIGNATURE}
"""