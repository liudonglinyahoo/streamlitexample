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

  data = {
    "zipcode": [
      80002, 80003, 80004, 80005, 80007, 80010, 80011, 80012, 80013, 80014,
      80015, 80016, 80017, 80018, 80019, 80020, 80021, 80022, 80023, 80024,
      80030, 80031, 80033, 80101, 80102, 80103, 80104, 80105, 80106, 80107,
      80108, 80109, 80110, 80111, 80112, 80113, 80116, 80117, 80118, 80120,
      80121, 80122, 80123, 80124, 80125, 80126, 80127, 80128, 80129, 80130,
      80131, 80133, 80134, 80135, 80136, 80137, 80138, 80203, 80204, 80205,
      80206, 80207, 80209, 80210, 80211, 80212, 80214, 80215, 80216, 80218,
      80219, 80220, 80221, 80222, 80223, 80224, 80226, 80227, 80228, 80229,
      80230, 80231, 80232, 80233, 80234, 80235, 80236, 80237, 80238, 80239,
      80241, 80246, 80247, 80249, 80260, 80401, 80403, 80420, 80421, 80422,
      80425, 80427, 80432, 80433, 80436, 80438, 80439, 80440, 80444, 80448,
      80449, 80452, 80453, 80454, 80456, 80457, 80465, 80470, 80474, 80475,
      80476, 80516, 80601, 80602, 80603, 80640, 80642, 80643, 80654, 80701,
      80808, 80816, 80820, 80827, 80828, 80830, 80831, 80832, 80833, 80835,
      80863,
    ],
    "land_share": [
      0.411896214, 0.343772257, 0.33664536, 0.308370597, 0.24347658,
      0.265561984, 0.248660774, 0.272727682, 0.26583726, 0.261937331,
      0.318265346, 0.240099053, 0.243944945, 0.174892608, 0.206807416,
      0.522201484, 0.374053258, 0.171264172, 0.288532221, 0.311670567,
      0.340940837, 0.309168915, 0.357008735, 0.254239261, 0.14028867,
      0.199407862, 0.289841374, 0.18501942, 0.298642402, 0.231852605,
      0.239877938, 0.242359589, 0.370612564, 0.25782581, 0.311908028,
      0.478324499, 0.429345183, 0.275836071, 0.210794386, 0.437044379,
      0.441404011, 0.368237358, 0.37981128, 0.260266937, 0.207087398,
      0.25722095, 0.301579456, 0.277136389, 0.253936191, 0.383393894,
      0.297149822, 0.076976949, 0.328698409, 0.330711192, 0.165776898,
      0.285707237, 0.296303099, 0.436513364, 0.468611251, 0.430302778,
      0.520430862, 0.473431607, 0.484749966, 0.56211148, 0.575832878,
      0.564970984, 0.462012688, 0.354626528, 0.288787416, 0.470571927,
      0.415921665, 0.500957783, 0.299219057, 0.602384606, 0.438150486,
      0.526328898, 0.34101271, 0.321230612, 0.313220514, 0.257846878,
      0.466169261, 0.544636606, 0.326883215, 0.22507757, 0.219915261,
      0.323850083, 0.35726532, 0.567182436, 0.483207513, 0.330916913,
      0.19256377, 0.525855855, 0.254407388, 0.512692531, 0.304111114,
      0.313295227, 0.261790874, 0.169588707, 0.139690147, 0.137416513,
      0.262784593, 0.059390831, 0.098055481, 0.21672374, 0.183671738,
      0.170285505, 0.216172423, 0.178721227, 0.119979439, 0.20550885,
      0.10821816, 0.082695533, 0.176591992, 0.245796513, 0.122771649,
      0.198715047, 0.298886922, 0.203099634, 0.143579872, 0.14649499,
      0.185779553, 4.816726988, 0.250105495, 0.228403415, 0.216908543,
      0.244362498, 0.243612114, 0.164364784, 0.383802884, 2.69226826,
      0.372658258, 0.134048598, 0.229229047, 0.150155472, 0.2761794,
      0.281359746, 0.252857682, 0.276704061, 0.167148418, 0.176916033,
      0.091761308,
    ]
  }

    # Organize the data as a dictionary for faster lookups
  data_dict = dict(zip(data["zipcode"], data["land_share"]))

    # Input zipcode
  input_zipcode = 80123  # Replace this with your desired zipcode

    # Find the corresponding landshare using the dictionary
  corresponding_landshare = data_dict.get(input_zipcode)

  if corresponding_landshare is not None:
      print(f"Zip Code: {input_zipcode}, Corresponding Land Share: {corresponding_landshare}")
  else:
      print(f"Zip Code {input_zipcode} not found in the data.")

  # print(amortization_schedule)
