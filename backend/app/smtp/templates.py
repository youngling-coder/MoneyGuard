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