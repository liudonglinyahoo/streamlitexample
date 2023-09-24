import pandas as pd

def generate_amortization_schedule(loan_amount, interest_rate, loan_term):
  """Generates an amortization schedule for a home loan.

  Args:
    loan_amount: The amount of the loan.
    interest_rate: The interest rate of the loan.
    loan_term: The number of years of the loan.

  Returns:
    A Pandas DataFrame of the amortization schedule.
  """

  monthly_payment = calculate_monthly_payment(loan_amount, interest_rate, loan_term)

  amortization_schedule = pd.DataFrame(columns=[
      'Month', 'Principal Remaining', 'Interest Payment', 'Principal Payment','Monthly Payment'
  ])

  principal_remaining = loan_amount
  for month in range(1, loan_term*12 ):
    interest_payment = principal_remaining * interest_rate / 12
    principal_payment = monthly_payment - interest_payment
    principal_remaining -= principal_payment

    amortization_schedule.loc[month] = [
        month, principal_remaining, interest_payment, principal_payment,monthly_payment
    ]

  return amortization_schedule

def calculate_monthly_payment(loan_amount, interest_rate, loan_term):
  """Calculates the monthly payment for a home loan.

  Args:
    loan_amount: The amount of the loan.
    interest_rate: The interest rate of the loan.
    loan_term: The number of years of the loan.

  Returns:
    The monthly payment for the loan.
  """

  monthly_interest_rate = interest_rate / 12
  number_of_payments = loan_term * 12

  monthly_payment = loan_amount * (
      monthly_interest_rate * (1 + monthly_interest_rate) ** number_of_payments) / (
          (1 + monthly_interest_rate) ** number_of_payments - 1)

  return monthly_payment

if __name__ == '__main__':
  loan_amount = 475000

  interest_rate = 0.075
  loan_term = 30

  amortization_schedule = generate_amortization_schedule(loan_amount, interest_rate, loan_term)

  print(amortization_schedule)

