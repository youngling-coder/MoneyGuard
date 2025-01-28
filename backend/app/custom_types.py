from enum import Enum


class TransactionType(Enum):
    income = "income"
    expense = "expense"


class TransactionCategory(Enum):
    income = "Income"
    savings_investments = "Savings & Investments"
    bills_utilities = "Bills & Utilities"
    rent_mortgage = "Rent & Mortgage"
    groceries_dining = "Groceries & Dining"
    transportation = "Transportation"
    shopping_personal = "Shopping & Personal Expenses"
    health_wellness = "Health & Wellness"
    entertainment_leisure = "Entertainment & Leisure"
    debt_loans = "Debt & Loans"
    other = "Other"


class Gender(Enum):
    male = "male"
    female = "female"
