import streamlit as st
import requests
import pandas as pd
import json
from datetime import date, datetime

debug = False

username = "55Y1IHCUYC2L8DXJODDZ"
def main():

    # get date and time to hour and minute now
    timenow = datetime.now()
    today = date.today()
    print("Today's date:", today)
    st.write('lastupdate', timenow)
    # Add a choice prompt to select the app
    app_choice = st.sidebar.radio("Select an App:", ("home_price_calculator_land_lease","Replicate_Guild_Home_Affordability","Property and Land Value App"))

    if app_choice == "Property and Land Value App":
        property_land_value_app()
    elif app_choice == "Replicate_Guild_Home_Affordability":
        Replicate_Guild_Home_Affordability()
    elif app_choice == "home_price_calculator_land_lease":
        home_price_calculator_with_land_lease_app()
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

def Replicate_Guild_Home_Affordability():
    st.title("Replicate_Guild_Home_Affordability:")
    link = "https://www.guildmortgage.com/mortgage-calculators/pre-qualification-calculator/"

    st.markdown(link, unsafe_allow_html=True)

    annual_income = st.sidebar.number_input("Annual Income", min_value=0, step=10000, value=120000)
    st.sidebar.write("Monthly Income:", annual_income / 12.0)
    down_payment_percent= st.sidebar.number_input("down payment percent", min_value=0, step=1, value=5)/100
    LTV = 1 - down_payment_percent
    monthly_debt = st.sidebar.number_input("Monthly Debt", min_value=0, step=1000, value=1200)
    interest_rate = st.sidebar.number_input("Interest Rate (%)", min_value=0.0, step=0.1, value=7.5)
    loan_term = st.sidebar.number_input("Loan Term (Years)", min_value=1, max_value=50, step=1, value=30)
    DTI_back = st.sidebar.number_input("DTI (%)", min_value=0.0, step=0.1, value=45.0)
    property_tax_rate = st.sidebar.number_input("property_tax_rate (%)", min_value=0.0, step=0.01, value=0.0833314*12)/100
    PMI_rate = st.sidebar.number_input("PMI_rate ($per 100K)", min_value=0, step=1, value=65)
    annual_home_insurance_rate = st.sidebar.number_input("annual_home_insurance rate per 1000", min_value=0.0000, step=0.1, value=3.5)/1000
    PMI_rate_per_100k = PMI_rate / 100000
    property_tax_rate_month = property_tax_rate/12
    home_insurance_rate_monthly = annual_home_insurance_rate/12

    #home_price_before_piti = calculate_home_price(annual_income, down_payment, interest_rate, loan_term,DTI_back,monthly_debt)
    #max_home_price_with_piti = calculate_home_price_with_PITI(home_price_before_piti,annual_income, down_payment, interest_rate, loan_term, DTI_back, monthly_debt,property_tax_rate,PMI_rate,annual_home_insurance)
    max_loan = find_optimal_loan(500000, LTV, PMI_rate_per_100k, home_insurance_rate_monthly,
                         property_tax_rate_month, interest_rate/1200, loan_term*12, monthly_debt, DTI_back/100, annual_income/12)
    max_home_price_with_piti=max_loan/LTV
    monthly_payment = compute_monthly_payments(max_loan,LTV,PMI_rate_per_100k,home_insurance_rate_monthly,property_tax_rate_month,interest_rate/1200,loan_term*12,monthly_debt)
    #st.write("monthlypayment", monthly_payment)
    # st.write("PMI_monthly",  max_loan * PMI_rate_per_100k)
    # st.write("home insuarance", max_home_price_with_piti * home_insurance_rate_monthly)
    # st.write("monthly_property_tax =", max_home_price_with_piti * property_tax_rate_month)
    # st.write("monthly_mortgageP&I" , compute_monthly_mortgage(max_loan, interest_rate/1200, loan_term*12))
    #st.write("maxloand",max_loan)
    # Display Home Price Calculator Result on the right-side panel
    st.markdown(f"<h2>Based on your inputs, the maximum home price you can afford is ${int(max_home_price_with_piti):,}</h2>",
                unsafe_allow_html=True)
    st.markdown(f"<h2>Based on your inputs, the maximum home loan you can afford is ${int(max_loan):,}</h2>",
                unsafe_allow_html=True)
    st.markdown(f"<h2>Calculation methodology: Use DTI to figure out max monthly mortgage payment then calc loan, then plus down payment</h2>",
                unsafe_allow_html=True)
    st.markdown(f"<h2>we considered PMI, Property Tax and home insurance</h2>",
                unsafe_allow_html=True)

def home_price_calculator_with_land_lease_app():
    st.title("home_price_calculator_with_land_lease")
    # st.write("calculation details. Start with a guess loan amount,"
    #          "1.calculate monthly mortgage payment, and Mortgage insurance, "
    #          "2.calculate the improvement using loan/LTV, "
    #          "3.then calculate the overall property value using improvement/(1-landshare)"
    #          "4.then calculate property tax and home insurance based on tax rate and insurance rate assumption"
    #          "5. then calculate the lease amount based on land share and land lease rate"
    #         "6. then calculate monthly payment using mortgage payment, property tax, home insurance and lease amount"
    #          "7. then compare the monthly payment with DTI and monthly income to see if it is affordable"
    #             "8. if not, decrease the loan amount and repeat the process until it is affordable")
    land_share = st.sidebar.number_input("Land Share", min_value=0, step=1, value=25)
    annual_income = st.sidebar.number_input("Annual Income", min_value=0, step=500, value=120000)
    monthly_debt = st.sidebar.number_input("Monthly Debt", min_value=0, step=50, value=1200)
    #st.sidebar.write("Monthly Income:", annual_income / 12.0)
    down_payment_percent = st.sidebar.number_input("Down Payment (%)", min_value=0.0, step=0.1, value=5.0)/100
    LTV = 1 - down_payment_percent
    interest_rate = st.sidebar.number_input("Interest Rate (%)", min_value=0.0, step=0.1, value=7.5)
    land_lease_rate = st.sidebar.number_input("Land Lease (%)", min_value=0.0, step=0.05, value=4.75)
    loan_term = st.sidebar.number_input("Loan Term (Years)", min_value=1, max_value=50, step=1, value=30)
    DTI_back = st.sidebar.number_input("DTI (%)", min_value=0.0, step=0.1, value=45.0)
    property_tax_rate = st.sidebar.number_input("property_tax_rate (%)", min_value=0.0, step=0.01, value=0.0833314*12)/100
    PMI_rate = st.sidebar.number_input("PMI_rate ($per 100K)", min_value=0, step=1, value=65)
    annual_home_insurance_rate = st.sidebar.number_input("annual_home_insurance rate per 1000", min_value=0.0000, step=0.1, value=3.5)/1000
    PMI_rate_per_100k = PMI_rate / 100000
    property_tax_rate_month = property_tax_rate / 12
    home_insurance_rate_monthly = annual_home_insurance_rate / 12

    max_loan_without_land_lease = find_optimal_loan(500000, LTV, PMI_rate_per_100k, home_insurance_rate_monthly,
                         property_tax_rate_month, interest_rate/1200, loan_term*12, monthly_debt, DTI_back/100, annual_income/12)
    max_home_price_without_land_lease = max_loan_without_land_lease/LTV
    st.write("without lease, loan and home price", max_loan_without_land_lease,max_home_price_without_land_lease)
    max_loan = find_optimal_loan(500000, LTV, PMI_rate_per_100k, home_insurance_rate_monthly,
                                    property_tax_rate_month, interest_rate / 1200, loan_term * 12, monthly_debt,
                                    DTI_back / 100, annual_income / 12, land_share, land_lease_rate)
    max_home_price_with_piti = (max_loan / LTV)/(1-land_share/100)
    st.write("with lease: loan and home price are", max_loan, max_home_price_with_piti)
    if max_loan > 0:
        affordability = 100*(max_home_price_with_piti-max_home_price_without_land_lease)/max_home_price_without_land_lease
    else:
        affordability = 0

    st.write("PMI_monthly",  max_loan * PMI_rate_per_100k)
    st.write("home insurance", max_home_price_with_piti * home_insurance_rate_monthly)
    st.write("monthly_property_tax =", max_home_price_with_piti * property_tax_rate_month)
    st.write("monthly_lease =", max_home_price_with_piti * land_share*land_lease_rate/100/100/12)
    st.write("monthly_mortgageP&I" , compute_monthly_mortgage(max_loan, interest_rate/1200, loan_term*12))
    st.write("loan", max_loan)

    # Display Home Price Calculator Result on the right-side panel
    if(max_loan <=0):
        st.write("Sorry, you cannot afford a home with your current income and debt level")

    st.markdown(f"<h3>Based on your inputs, with land lease the maximum home price you can afford is ${int(max_home_price_with_piti):,}</h3>",unsafe_allow_html=True)
    st.markdown(f"<h3>Without land lease the maximum home price you can afford is ${int(max_home_price_without_land_lease):,}</h3>",
        unsafe_allow_html = True)
    st.markdown(f"<h3>With GHY land lease program, your purchasing power improved by {round(float(affordability),2):,} %</h3>",
        unsafe_allow_html=True)

def compute_monthly_mortgage(P,r,n):
    #st.write("P+R+n", P,r,n)
    return P * (r * (1 + r)**n) / ((1 + r)**n - 1)

def compute_monthly_payments(P_guess, LTV, PMI_rate_per_100k, home_insurance_rate_monthly, property_tax_rate_month, r, n, monthly_debt, land_share=None, land_lease_rate=None):

    #if land_share and land_lease_rate: is not provide than property_value = P_guess / LTV, otherwise property_value = (P_guess / LTV) / (1 - land_share / 100)
    property_value = (P_guess / LTV) / (1 - land_share / 100) if land_share else P_guess / LTV
    monthly_PMI = P_guess * PMI_rate_per_100k

    home_insurance_monthly = property_value * home_insurance_rate_monthly
    monthly_property_tax = property_value * property_tax_rate_month
    monthly_mortgage = compute_monthly_mortgage(P_guess, r, n)
    monthly_lease = property_value * land_share * land_lease_rate / (100 * 100 * 12) if land_share and land_lease_rate else 0
    # st.write("mon###########################################")
    # st.write("property_value", property_value)
    # st.write("puessloan", P_guess)
    # st.write("monthly_lease", monthly_lease)
    # st.write("monthly_mortgage", monthly_mortgage)
    # st.write("monthly_property_tax", monthly_property_tax)
    # st.write("home_insurance_monthly", home_insurance_monthly)
    # st.write("monthly all", monthly_PMI + home_insurance_monthly + monthly_property_tax + monthly_mortgage + monthly_debt + monthly_lease)
    return monthly_PMI + home_insurance_monthly + monthly_property_tax + monthly_mortgage + monthly_debt + monthly_lease


def find_optimal_loan(principal_loan_amount, LTV, PMI_rate_per_100k, home_insurance_rate_monthly, property_tax_rate_month, r, n, monthly_debt, DTI_backend, monthly_income, land_share=None, land_lease_rate=None):
    low = 0
    high = 20 * principal_loan_amount
    if debug:
        st.write("start guess!!!!!!!!!!!!!!!!!!withhigh, landshare", high,land_share)
    while high - low > 1:
        mid = (high + low) / 2

        if land_share:
            total_monthly_payments = compute_monthly_payments(mid, LTV, PMI_rate_per_100k, home_insurance_rate_monthly, property_tax_rate_month, r, n, monthly_debt, land_share, land_lease_rate)
        else:
            total_monthly_payments = compute_monthly_payments(mid, LTV, PMI_rate_per_100k, home_insurance_rate_monthly, property_tax_rate_month, r, n, monthly_debt)

        if total_monthly_payments <= DTI_backend * monthly_income:
            low = mid
            if debug:
                st.write("total_monthly_payments,low,mid,high",total_monthly_payments,low,mid,high)
        else:
            high = mid
            if debug:
                st.write("total_monthly_payments!!,low,mid,high", total_monthly_payments, low, mid, high)

    return low

if __name__ == "__main__":
    main()