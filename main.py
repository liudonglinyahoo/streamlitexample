import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# Define constants
DEBUG = False
username = "55Y1IHCUYC2L8DXJODDZ"
def main():

    # get date and time to hour and minute now
    timenow = datetime.now()
    st.write('lastupdate', timenow)
    # Add a choice prompt to select the app
    app_choice = st.sidebar.radio("Select:", ("home_price_calculator_land_lease","land lease benefit-payment","Replicate_Guild_Home_Affordability","Property and Land Value App","Denver land share by zip code"))

    if app_choice == "Property and Land Value App":
        property_land_value_app()
    elif app_choice == "Replicate_Guild_Home_Affordability":
        combined_home_affordability_app("Replicate_Guild_Home_Affordability", False)
    elif app_choice == "home_price_calculator_land_lease":
        combined_home_affordability_app("home_price_calculator_land_lease", True)
    elif app_choice == "land lease benefit-payment":
        home_affordability_payment_app()
    elif app_choice == "Denver land share by zip code":
        property_zip_code()


def property_land_value_app():
    st.title("Property and Land Values-App")
    # Prompt user to enter the password
    password = st.text_input("Enter your password:(DL sent email)", type="password")

    address_line_1 = st.text_input("Enter Address Line 1 like 517 N Chugach St:")
    zip_code = st.text_input("Enter Zip Code:")

# Display a Submit button
    if st.button("Submit"):
         # Get the selected address and zip code
        #address, zip_code = selected_address
        address= address_line_1
        zip_code = zip_code
        # Process the selected address
        prop_val = get_property_data('value', address, zip_code, password)
        land_val = get_property_data('land_value', address, zip_code, password)
    # Assuming property and land value APIs return consistent data
        if prop_val and land_val and prop_val[0]['property/value']['api_code']==0 and land_val[0]['property/land_value']['api_code']==0:
            data = {
                'address': address,
                'zip_code': zip_code,
                'land share_calc': round(land_val[0]['property/land_value']['result']['land_value']['value_mean']/prop_val[0]['property/value']['result']['value']['price_mean'],3),
                'land_value_mean': land_val[0]['property/land_value']['result']['land_value']['value_mean'],
                'land_value_upr': land_val[0]['property/land_value']['result']['land_value']['value_upr'],
                'land_value_lwr': land_val[0]['property/land_value']['result']['land_value']['value_lwr'],
                'property_value_mean': prop_val[0]['property/value']['result']['value']['price_mean'],
                'property_value_upr': prop_val[0]['property/value']['result']['value']['price_upr'],
                'property_value_lwr': prop_val[0]['property/value']['result']['value']['price_lwr'],
            }
            df = pd.DataFrame([data])
            st.table(df)
            link = "https://www.google.com/search?q="
            link += address.replace(" ", "+") + "+" + zip_code
            link += "+zillow"
            st.markdown(link, unsafe_allow_html=True)
        else:
            st.write("Error retrieving data. Please try again.")


    else:
        st.write(".")
def property_zip_code():
    st.title("Property land share by zip code")
    # Prompt user to enter the password
    #password = st.text_input("Enter your email as password", type="password")

    # address_line_1 = st.text_input("Enter Address Line 1 like 517 N Chugach St:")
    zip_code = st.text_input("Enter Zip Code in Denver then click submit:")

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

    data_dict = dict(zip(data["zipcode"], data["land_share"]))
    #st.write(data_dict)
    # Display a Submit button
    if st.button("Submit"):

        # Input zipcode
        #st.write(zip_code)
        input_zipcode = int(zip_code) # Replace this with your desired zipcode

        # Find the corresponding landshare using the dictionary
        #st.write(data_dict.get(input_zipcode))
        corresponding_landshare = data_dict.get(input_zipcode)
        if corresponding_landshare is not None:

            if corresponding_landshare >0.35:
                corresponding_landshare = 0.35
                st.write(f"Zip Code: {input_zipcode}, Our program will cover Land Share: {corresponding_landshare}")
            elif corresponding_landshare<0.15:
                st.write(f"Zip Code: {input_zipcode}, the land share is {corresponding_landshare}, which is too low for our program to make a meaningful impact.")
        else:
            st.write(f"Zip Code: {input_zipcode}, we don't have data for this zipcode. Please try another one.")


    else:
        st.write("Click the Submit button to get the estimated land share for a given zipcode.")
    #st.table(data)
def get_property_data(endpoint, address, zip_code, password):
    base_url = "https://api.housecanary.com/v2/property/"
    auth = (username, password)
    params = {
        'address': address,
        'zipcode': zip_code,
    }

    return api_request('GET', base_url + endpoint, params=params, auth=auth)

def api_request(method, url, headers=None, params=None, auth=None):
    response = requests.request(method, url, headers=headers, params=params, auth=auth)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        st.error(f"Request failed with status code {response.status_code}")
        return None


def compute_monthly_mortgage(P,r,n):
    #st.write("P+R+n", P,r,n)
    return P * (r * (1 + r)**n) / ((1 + r)**n - 1)

def compute_monthly_payments(P_guess, LTV, PMI_rate_per_100k, home_insurance_rate_monthly, property_tax_rate_month, r, n, monthly_debt, land_share=None, land_lease_rate=None):

    #if land_share and land_lease_rate is not provide then property_value = P_guess / LTV, otherwise property_value = (P_guess / LTV) / (1 - land_share )
    property_value = (P_guess / LTV) / (1 - land_share) if land_share else P_guess / LTV
    monthly_PMI = P_guess * PMI_rate_per_100k

    home_insurance_monthly = property_value * home_insurance_rate_monthly
    monthly_property_tax = property_value * property_tax_rate_month
    monthly_mortgage = compute_monthly_mortgage(P_guess, r, n)
    monthly_lease = property_value * land_share * land_lease_rate / (12) if land_share and land_lease_rate else 0
    # st.write("mon###########################################")
    # st.write("property_value", property_value)
    # st.write("puessloan", P_guess)
    # st.write("monthly_lease", monthly_lease)
    # st.write("monthly_mortgage", monthly_mortgage)
    # st.write("monthly_property_tax", monthly_property_tax)
    # st.write("home_insurance_monthly", home_insurance_monthly)
    # st.write("monthly all", monthly_PMI + home_insurance_monthly + monthly_property_tax + monthly_mortgage + monthly_debt + monthly_lease)
    return monthly_PMI + home_insurance_monthly + monthly_property_tax + monthly_mortgage + monthly_debt + monthly_lease


def find_optimal_loan(principal_loan_amount, LTV, PMI_rate_per_100k, home_insurance_rate_monthly, property_tax_rate_month, r, n, monthly_debt, DTI_backend,DTI_front, monthly_income, land_share=None, land_lease_rate=None):
    low = 0
    high = 20 * principal_loan_amount
    if DEBUG:
        st.write("start guess!!!!!!!!!!!!!!!!!!withhigh, landshare", high,land_share)
        print("find_optimal_loan called, inputs are:")
        print("principal_loan_amount, LTV, PMI_rate_per_100k, home_insurance_rate_monthly, property_tax_rate_month, r, n, monthly_debt, DTI_backend,DTI_front, monthly_income, land_share, land_lease_rate")
        print(principal_loan_amount, LTV, PMI_rate_per_100k, home_insurance_rate_monthly, property_tax_rate_month, r, n, monthly_debt, DTI_backend,DTI_front, monthly_income, land_share, land_lease_rate)

    while high - low > 1:
        mid = (high + low) / 2

        if land_share:
            total_monthly_payments = compute_monthly_payments(mid, LTV, PMI_rate_per_100k, home_insurance_rate_monthly, property_tax_rate_month, r, n, monthly_debt, land_share, land_lease_rate)
        else:
            total_monthly_payments = compute_monthly_payments(mid, LTV, PMI_rate_per_100k, home_insurance_rate_monthly, property_tax_rate_month, r, n, monthly_debt)

        if total_monthly_payments <= DTI_backend * monthly_income and (total_monthly_payments-monthly_debt)<=DTI_front*monthly_income:
            low = mid
            if DEBUG:
                st.write("total_monthly_payments,low,mid,high",total_monthly_payments,low,mid,high)
                print("total_monthly_payments,low,mid,high",total_monthly_payments,low,mid,high)
        else:
            high = mid
            if DEBUG:
                st.write("total_monthly_payments!!,low,mid,high", total_monthly_payments, low, mid, high)

    return low

def combined_home_affordability_app(title, land_lease_flag):
    st.title(title)
    # Input parameters based on the type of app
    # You can customize these inputs based on your requirements
    # st.write("calculation details. Start with a guess loan amount,"
    #          "1.calculate monthly mortgage payment, and Mortgage insurance, "
    #          "2.calculate the improvement using loan/LTV, "
    #          "3.then calculate the overall property value using improvement/(1-landshare)"
    #          "4.then calculate property tax and home insurance based on tax rate and insurance rate assumption"
    #          "5. then calculate the lease amount based on land share and land lease rate"
    #         "6. then calculate monthly payment using mortgage payment, property tax, home insurance and lease amount"
    #          "7. then compare the monthly payment with DTI and monthly income to see if it is affordable"
    #             "8. if not, decrease the loan amount and repeat the process until it is affordable")
    if(land_lease_flag):
            land_share = st.sidebar.number_input("Land Share", min_value=0, step=1, value=25)/100
            land_lease_rate = st.sidebar.number_input("Land Lease Rate (%)", min_value=0.0, step=0.05, value=4.75)/100

    annual_income = st.sidebar.number_input("Annual Income", min_value=0, step=500, value=120000)
    monthly_debt = st.sidebar.number_input("Monthly Debt", min_value=0, step=50, value=1200)
    # st.sidebar.write("Monthly Income:", annual_income / 12.0)
    down_payment_percent = st.sidebar.number_input("Down Payment (%)", min_value=0.0, step=0.1, value=5.0) / 100
    LTV = 1 - down_payment_percent
    interest_rate = st.sidebar.number_input("Interest Rate (%)", min_value=0.0, step=0.1, value=7.5)
    loan_term = st.sidebar.number_input("Loan Term (Years)", min_value=1, max_value=50, step=1, value=30)
    DTI_front = st.sidebar.number_input("Front-endDTI (%)", min_value=0.0, step=0.1, value=33.0)
    DTI_back = st.sidebar.number_input("Back-end DTI (%)", min_value=0.0, step=0.1, value=45.0)
    property_tax_rate = st.sidebar.number_input("property_tax_rate (%)", min_value=0.0, step=0.01,
                                                value=1.0) / 100
    PMI_rate = st.sidebar.number_input("PMI_rate ($per 100K)", min_value=0, step=1, value=65)
    annual_home_insurance_rate = st.sidebar.number_input("annual_home_insurance rate per 1000", min_value=0.0000,
                                                         step=0.1, value=3.5) / 1000
    PMI_rate_per_100k = PMI_rate / 100000
    property_tax_rate_month = property_tax_rate / 12
    home_insurance_rate_monthly = annual_home_insurance_rate / 12

    max_loan_without_land_lease = find_optimal_loan(500000, LTV, PMI_rate_per_100k, home_insurance_rate_monthly,
                                                    property_tax_rate_month, interest_rate / 1200, loan_term * 12,
                                                    monthly_debt, DTI_back / 100, DTI_front / 100, annual_income / 12)
    max_home_price_without_land_lease = max_loan_without_land_lease / LTV
    if land_lease_flag == False:
        st.write("without land lease: loan and home price", max_loan_without_land_lease, max_home_price_without_land_lease)
        st.write("PMI_monthly", max_loan_without_land_lease * PMI_rate_per_100k)
        st.write("home insurance", max_home_price_without_land_lease * home_insurance_rate_monthly)
        st.write("monthly_property_tax =", max_home_price_without_land_lease * property_tax_rate_month)
        st.write("monthly_mortgageP&I", compute_monthly_mortgage(max_loan_without_land_lease, interest_rate / 1200, loan_term * 12))
        st.write("loan", max_loan_without_land_lease)

    if land_lease_flag:
        max_loan = find_optimal_loan(500000, LTV, PMI_rate_per_100k, home_insurance_rate_monthly,
                                 property_tax_rate_month, interest_rate / 1200, loan_term * 12, monthly_debt,
                                 DTI_back / 100, DTI_front / 100, annual_income / 12, land_share, land_lease_rate)
        max_home_price_with_piti = (max_loan / LTV) / (1 - land_share)
        #st.write("with lease: loan and home price are", max_loan, max_home_price_with_piti)
        if max_loan > 0:
            affordability = 100 * (
                    max_home_price_with_piti - max_home_price_without_land_lease) / max_home_price_without_land_lease
        else:
            affordability = 0
            st.write("based on your input, you can not afford any loan")

        # st.write("PMI_monthly", max_loan * PMI_rate_per_100k)
        # st.write("home insurance", max_home_price_with_piti * home_insurance_rate_monthly)
        # st.write("monthly_property_tax =", max_home_price_with_piti * property_tax_rate_month)
        # st.write("monthly_lease =", max_home_price_with_piti * land_share * land_lease_rate / 12)
        # st.write("monthly_mortgageP&I", compute_monthly_mortgage(max_loan, interest_rate / 1200, loan_term * 12))
        # st.write("loan", max_loan)

        st.markdown(
            f"<h3>Based on your inputs, with land lease the maximum home price you can afford is ${int(max_home_price_with_piti):,}</h3>",
            unsafe_allow_html=True)
        st.markdown(
            f"<h3>Without land lease the maximum home price you can afford is ${int(max_home_price_without_land_lease):,}</h3>",
            unsafe_allow_html=True)
        st.markdown(
            f"<h3>With GHY land lease program, your purchasing power improved by {round(float(affordability), 2):,} %</h3>",
            unsafe_allow_html=True)
    if land_lease_flag:
        total_monthly_pay = max_loan_without_land_lease * PMI_rate_per_100k + max_home_price_without_land_lease * home_insurance_rate_monthly + max_home_price_without_land_lease * property_tax_rate_month+ compute_monthly_mortgage(max_loan_without_land_lease, interest_rate / 1200, loan_term * 12)
        total_monthly_pay_with_lease = max_loan * PMI_rate_per_100k + max_home_price_with_piti * home_insurance_rate_monthly + max_home_price_with_piti * property_tax_rate_month + max_home_price_with_piti * land_share * land_lease_rate / 12 + compute_monthly_mortgage(max_loan, interest_rate / 1200, loan_term * 12)
        st.write("DTI Front and DTI Back", round(total_monthly_pay_with_lease/(annual_income/12),6), round((total_monthly_pay_with_lease+monthly_debt)/(annual_income/12),6))
        data = [{
            "Condition": "Without Land Lease",
            "Loan Amount": int(max_loan_without_land_lease),
            "Home Price": int(max_home_price_without_land_lease),
            "Total monthly payment": int(total_monthly_pay),
            "PMI Monthly": int(max_loan_without_land_lease * PMI_rate_per_100k),
            "Home Insurance": int(max_home_price_without_land_lease * home_insurance_rate_monthly),
            "Property Tax Monthly": int(max_home_price_without_land_lease * property_tax_rate_month),
            "Mortgage P&I": int( compute_monthly_mortgage(max_loan_without_land_lease, interest_rate / 1200, loan_term * 12)),
            "Land Lease Monthly": 0},
            {"Condition": "With Land Lease",
            "Loan Amount": int(max_loan),
            "Home Price": int(max_home_price_with_piti),
            "Total monthly payment":int(total_monthly_pay_with_lease),
            "PMI Monthly": int(max_loan * PMI_rate_per_100k),
            "Home Insurance": int(max_home_price_with_piti * home_insurance_rate_monthly),
            "Property Tax Monthly": int(max_home_price_with_piti * property_tax_rate_month),
            "Mortgage P&I": int( compute_monthly_mortgage(max_loan, interest_rate / 1200, loan_term * 12)),
            "Land Lease Monthly":  int(max_home_price_with_piti * land_share * land_lease_rate / 12)}
        ]
        df = pd.DataFrame(data)

        st.write(df.to_html(index=False), unsafe_allow_html=True)


    else:
        st.write("something wrong with your input, please check again")
def home_affordability_payment_app():
    st.title("Monthly payment Calculator")
    # start from home price as input, use down payment percent to calculate loan amount
    # use loan amount to calculate monthly payment
    # use monthly payment and income to calculate DTIs

    home_price = st.sidebar.number_input("Home Price", min_value=0, step=10000, value=500000)
    down_payment_percent = st.sidebar.number_input("Down Payment (%)", min_value=0.0, step=0.1, value=5.0) / 100
    land_share = st.sidebar.number_input("Land Share", min_value=0, step=1, value=25)/100
    land_lease_rate = st.sidebar.number_input("Land Lease Rate (%)", min_value=0.0, step=0.05, value=4.75)/100
    LTV = 1 - down_payment_percent
    interest_rate = st.sidebar.number_input("Interest Rate (%)", min_value=0.0, step=0.1, value=7.5)
    loan_term = st.sidebar.number_input("Loan Term (Years)", min_value=1, max_value=50, step=1, value=30)
    property_tax_rate = st.sidebar.number_input("property_tax_rate (%)", min_value=0.0, step=0.01,
                                                value=1.0) / 100
    PMI_rate = st.sidebar.number_input("PMI_rate ($per 100K)", min_value=0, step=1, value=65)
    annual_home_insurance_rate = st.sidebar.number_input("annual_home_insurance rate per 1000", min_value=0.0000,
                                                         step=0.1, value=3.5) / 1000

    annual_income = st.sidebar.number_input("Annual Income", min_value=0, step=500, value=120000)
    monthly_debt = st.sidebar.number_input("Monthly Debt", min_value=0, step=50, value=1200)

    PMI_rate_per_100k = PMI_rate / 100000
    property_tax_rate_month = property_tax_rate / 12
    home_insurance_rate_monthly = annual_home_insurance_rate / 12

    max_loan_without_land_lease= home_price * LTV
    max_loan_with_land_lease = home_price * (1-land_share) * LTV

    mortgage_insurance_monthly = max_loan_without_land_lease * PMI_rate_per_100k
    home_insurance_monthly = home_price * home_insurance_rate_monthly
    property_tax_monthly = home_price * property_tax_rate_month
    monthly_mortgageP_I = compute_monthly_mortgage(max_loan_without_land_lease, interest_rate / 1200, loan_term * 12)
    total_monthly_pay = home_insurance_monthly + property_tax_monthly + monthly_mortgageP_I + mortgage_insurance_monthly

    monthly_lease =home_price * land_share * land_lease_rate / 12
    mortgage_insurance_monthly_l = max_loan_with_land_lease * PMI_rate_per_100k
    home_insurance_monthly_l = home_price * home_insurance_rate_monthly
    property_tax_monthly_l = home_price * property_tax_rate_month
    monthly_mortgageP_I_l = compute_monthly_mortgage(max_loan_with_land_lease, interest_rate / 1200, loan_term * 12)
    total_monthly_pay_l = home_insurance_monthly_l + property_tax_monthly_l + monthly_mortgageP_I_l + mortgage_insurance_monthly_l + monthly_lease
    monthly_pay_saving_p = 100 * (
        total_monthly_pay- total_monthly_pay_l  ) / total_monthly_pay
    monthly_pay_saving = -(total_monthly_pay_l - total_monthly_pay)

    st.markdown(
        f"<h3>Based on your inputs, with land lease program, your initial monthly payment saving is ${int(monthly_pay_saving):,} ({monthly_pay_saving_p/100:.2%} )see table below for details:</h3>",
        unsafe_allow_html=True
    )

    #st.write("Initial monthly_pay_saving and percentage( %)", monthly_pay_saving, monthly_pay_saving_p )
    #st.write("DTI Front and DTI Back", round(tota/(annual_income/12),6), round((total_monthly_pay_with_lease+monthly_debt)/(annual_income/12),6))
    data = [{
            "Condition": "Without Land Lease",
            "Home Price": int(home_price),
            "Loan Amount": int(max_loan_without_land_lease),
            "down payment": int(home_price * down_payment_percent),
            "Total monthly payment": int(total_monthly_pay),
            "PMI Monthly": int(mortgage_insurance_monthly),
            "Home Insurance": int(home_insurance_monthly),
            "Property Tax Monthly": int(property_tax_monthly),
            "Mortgage P&I": int( monthly_mortgageP_I),
            "Land Lease Monthly": 0},
            {"Condition": "With Land Lease",
            "Home Price": int(home_price),
            "Loan Amount": int(max_loan_with_land_lease),
            "down payment": int(max_loan_with_land_lease * down_payment_percent),
            "Total monthly payment":int(total_monthly_pay_l),
            "PMI Monthly": int(mortgage_insurance_monthly_l),
            "Home Insurance": int(home_insurance_monthly_l),
            "Property Tax Monthly": int(property_tax_monthly_l),
            "Mortgage P&I": int( monthly_mortgageP_I_l),
            "Land Lease Monthly":  int(monthly_lease)}
        ]
    df = pd.DataFrame(data)
    st.write(df.to_html(index=False), unsafe_allow_html=True)
if __name__ == "__main__":
    main()
