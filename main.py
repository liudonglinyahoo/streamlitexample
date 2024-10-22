import time

import streamlit as st
import requests
import streamlit_authenticator as stauth  # pip install streamlit-authenticator
import pickle
import pandas as pd
from datetime import datetime
from pathlib import Path
# Define constants
DEBUG = False
apiusername = "55Y1IHCUYC2L8DXJODDZ"

def authenticate():
    users = ["GuildLO1", "GuildLO2", "GHYimpact"]
    usernames = ["GuildLO1", "GuildLO2", "GHYimpact"]
    # st.write(users)
    # loading passwords which are hashed
    # if 'authentication_status' not in st.session_state:
    #     st.session_state['authentication_status'] = False  # or whatever initial value you want

    file_path = Path(__file__).parent / "hashed_passwords.pkl"
    # st.write(file_path)
    with file_path.open("rb") as file:
        hashed_passwords = pickle.load(file)
    #st.write(hashed_passwords)
    # Create an Auth object
    #  Authenticate( names,username,hashed_password,json_gen_token_cookie,random_key_to_hash_cokkie_signature,number_of_days_cokkie_can_be_used_for)
    # authenticator = stauth.Authenticate(users, usernames, hashed_passwords, "demo_auth", "rkey1", cookie_expiry_days=10)

    credentials = {"usernames": {}}

    for uname, name, pwd in zip(usernames, users, hashed_passwords):
        user_dict = {"name": name, "password": pwd}
        credentials["usernames"].update({uname: user_dict})

    authenticator = stauth.Authenticate(credentials, "cokkie_name", "random_key", cookie_expiry_days=0.1)
    # can be main or sidebar
    name, authentication_status, username = authenticator.login("Login", "sidebar")
    # st.write("name", name)
    # st.write("authentication_status", authentication_status)
    st.write("You are login as", username)

    if authentication_status == False:
        st.error("Username/password is incorrect")

    if authentication_status == None:

        st.warning("Please enter your username and password")

        header_text = "The Tillt Program"
        header_text1 = "A Sustainable Home Buying Solution that Combines Affordability with Community"

        #
        # st.markdown(f"## {header_text}")
        # st.markdown(f"### {header_text1}")
        # st.image('2.jpg', caption='', width=300)
    if authentication_status:
        return True, username
    else:
        return False, None

def main():
    st.set_page_config(layout="wide")
    # Add a choice prompt to select the app
    authenticated, username = authenticate()
    if authenticated & (username != "GHYimpact"):


        app_choice = st.sidebar.radio("Select:", ("Tillt Affordability Calculator","Tillt Monthly Payment Calculator",
                                                  "Property and Land Value App","Denver land share by zip code",
                                                  "Denver listing examples"  ))

        if app_choice == "Property and Land Value App":
            property_land_value_app(username)
        elif app_choice == "Replicate_Guild_Home_Affordability":
            combined_home_affordability_app("Replicate_Guild_Home_Affordability", False)
        elif app_choice == "Tillt Affordability Calculator":
            combined_home_affordability_app("Tillt Affordability Calculator", True)
        elif app_choice == "Tillt Monthly Payment Calculator":
            home_affordability_payment_app()
        elif app_choice == "Denver land share by zip code":
            property_zip_code()
        elif app_choice == "Denver listing examples":
            property_land_value_app_cached()
    if authenticated & (username == "ghyimpact"):

        app_choice = st.sidebar.radio("Select:", ("Tillt Affordability Calculator","Tillt Monthly Payment Calculator",
                                                  "Property and Land Value App","Denver land share by zip code",
                                                  "Denver listing examples" ,"Update release rate app"  ))

        if app_choice == "Property and Land Value App":
            property_land_value_app()
        elif app_choice == "Replicate_Guild_Home_Affordability":
            combined_home_affordability_app("Replicate_Guild_Home_Affordability", False)
        elif app_choice == "Tillt Affordability Calculator":
            combined_home_affordability_app("Tillt Affordability Calculator", True)
        elif app_choice == "Tillt Monthly Payment Calculator":
            home_affordability_payment_app()
        elif app_choice == "Denver land share by zip code":
            property_zip_code()
        elif app_choice == "Denver listing examples":
            property_land_value_app_cached()
        elif app_choice == "Update release rate app":
            update_releaserate_app()

    timenow = datetime.now()
    st.write('lastupdate20241022', timenow)

def update_releaserate_app():
    st.write('lastupdate', time.clock())
def property_land_value_app_cached():
    st.title("Property and Land Values examples")
    #load addresses and zip codes from csv file

    #prompt user to select the addresses
    url = "https://s3.amazonaws.com/donglintonyliu.click/merged_zillow_hcloandshare.csv"

    # Read the CSV file into a DataFrame
    df = pd.read_csv(url)
    addresses = list(zip(df['streetName'], df['zipcode'].astype(str)))

    # Print the DataFrame
    st.dataframe(df)
    selected_address = st.selectbox("Select an address:", addresses)
    st.write("You selected:", selected_address)


    street_name, zipcode = selected_address
    # Filter the dataframe based on the streetName and zipcode
    filtered_df = df[(df['streetName'] == street_name) & (df['zipcode'] == int(zipcode))]

    # If the filtered dataframe is not empty, return the values
    if not filtered_df.empty:
        price = filtered_df['price'].iloc[0]
        land_value_mean = filtered_df['Land Value - Value Mean'].iloc[0]
        Land_Share_of_Property = filtered_df['Land_Share_of_Property'].iloc[0]
        Land_finance = filtered_df['Land_finance'].iloc[0]
        land_share =Land_finance/price

        st.write("Price:", price, "Land finance:", Land_finance,"land_share:",land_share)
    else:
        st.write("No data found for the selected address")

    home_price = price
    down_payment_percent = 0.05
    land_lease_rate = 0.0475
    LTV = 1 - down_payment_percent

    interest_rate = st.sidebar.number_input("Interest Rate (%)", min_value=0.0, step=0.1, value=7.5)
    loan_term = st.sidebar.number_input("Loan Term (Years)", min_value=1, max_value=50, step=1, value=30)
    property_tax_rate = st.sidebar.number_input("property_tax_rate (%)", min_value=0.0, step=0.01,
                                                value=1.0) / 100
    PMI_rate = st.sidebar.number_input("PMI rate%", min_value=0.0, step=0.01, value=0.78)
    annual_home_insurance_rate = st.sidebar.number_input("Home insurance rate %", min_value=0.0000,
                                                         step=0.01, value=0.35) / 100

    property_tax_rate_month = property_tax_rate / 12
    home_insurance_rate_monthly = annual_home_insurance_rate / 12

    max_loan_without_land_lease= home_price * LTV
    max_loan_with_land_lease = home_price * (1-land_share) * LTV

    mortgage_insurance_monthly = max_loan_without_land_lease * PMI_rate / 1200
    home_insurance_monthly = home_price * home_insurance_rate_monthly
    property_tax_monthly = home_price * property_tax_rate_month
    monthly_mortgageP_I = compute_monthly_mortgage(max_loan_without_land_lease, interest_rate / 1200, loan_term * 12)
    total_monthly_pay = home_insurance_monthly + property_tax_monthly + monthly_mortgageP_I + mortgage_insurance_monthly

    monthly_lease =home_price * land_share * land_lease_rate / 12
    mortgage_insurance_monthly_l = max_loan_with_land_lease * PMI_rate / 1200
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
    data = {"":["Home Price", "Loan Amount", "down payment", "Total monthly payment", "PMI Monthly", "Home Insurance", "Property Tax Monthly", "Mortgage P&I", "Land Lease Monthly"],
            "Without Land Lease":[int(home_price),int(max_loan_without_land_lease),int(home_price * down_payment_percent),
                                  int(total_monthly_pay),int(mortgage_insurance_monthly),int(home_insurance_monthly),int(property_tax_monthly),int(monthly_mortgageP_I),0],
             "With Land Lease":[int(home_price),int(max_loan_with_land_lease),int(home_price * down_payment_percent),
                                    int(total_monthly_pay_l),int(mortgage_insurance_monthly_l),int(home_insurance_monthly_l),int(property_tax_monthly_l),int(monthly_mortgageP_I_l),int(monthly_lease)
                                ]
            }

    df = pd.DataFrame(data)
    st.write(df.to_html(index=False), unsafe_allow_html=True)

    if st.button("Show Lease Payment Schedule"):

        leasepay_schedule= generate_leasepay_schedule(home_price*land_share,land_lease_rate,0.01, 10)
        df = pd.DataFrame(leasepay_schedule)
        # format df's first two columns to integer

        for col in df.columns[:4]:
            df[col] = df[col].astype(int)

        st.write(df.to_html(index=False), unsafe_allow_html=True)
    else:
        st.write("Please click the button to show lease payment schedule")
    st.write(
        "***Disclaimer: This calculator is offered for illustrative and educational purposes only and it is not intended to replace a professional estimate. Calculator results do not reflect all loan types and are subject to individual program loan limits. All calculations and costs are estimates and therefore, Terrapin Impact Partner does not make any guarantee or warranty (express or implied) that all possible costs have been included. The assumptions made here and the output of the calculator do not constitute a loan offer or solicitation, or financial or legal advice. Please connect with a loan professional for a formal estimate. Every effort is made to maintain accurate calculations; however, Terrapin assumes no liability to any third parties that rely on this information and is not responsible for the accuracy of rates, APRs or any other loan information factored in the calculations.")
def check_cache(address,zip_code):
    # prompt user to select the addresses
    url = "https://s3.amazonaws.com/donglintonyliu.click/merged_zillow_hcloandshare.csv"

    # Read the CSV file into a DataFrame
    df = pd.read_csv(url)
    filtered_df = df[(df['streetName'] == address) & (df['zipcode'] == int(zip_code))]

    # If the filtered dataframe is not empty, return the values
    if not filtered_df.empty:
        price = filtered_df['price'].iloc[0]
        land_value_mean = filtered_df['Land Value - Value Mean'].iloc[0]
        Land_Share_of_Property = filtered_df['Land_Share_of_Property'].iloc[0]
        Land_finance = filtered_df['Land_finance'].iloc[0]
        land_share =Land_finance/price

        #st.write("Price:", price, "Land finance:", Land_finance,"land_share:",land_share)
        return price, land_share, Land_Share_of_Property,Land_finance
    else:
        st.write("No data found for the selected address")
        return None,None,None,None

def property_land_value_app(username):
    st.title("Property and Land Value Checker")
    st.write("Only single-family, fee-simple, detached homes located in the Denver metro area are eligible. Duplexes, condos and townhomes are ineligible.")
    # Prompt user to enter the password
    password = st.text_input("Enter your password:(email ghyproductteam@ghyimpact.com for password)", type="password")

    address_line_1 = st.text_input("Enter Address Line 1:", "43 S Perry St")
    zip_code = st.text_input("Enter Zip Code:", "80219")

# Display a Submit button
    if st.button("Submit"):
         # Get the selected address and zip code
        #address, zip_code = selected_address
        address= address_line_1
        zip_code = zip_code
        # Process the selected address
         # if can find data in cache, return data from cache
        if(username=="ghyimpact"):
            st.write(username)
        else:
            st.write(username)
        price, land_share, Land_Share_of_Property,land_finance = check_cache(address, zip_code)
        if  price and land_share and Land_Share_of_Property and land_finance:
            if Land_Share_of_Property>0.35:
                Land_Share_of_Property = 0.35
            st.write( "Congrats! Address :" ,address,",", zip_code, "is supported by Terrapin Program!")
            st.write("Terrapin is willing to purchase the land at this address at ", Land_Share_of_Property,"of the total property value. Estimated dollar Amount =" ,price*Land_Share_of_Property,"$")
            st.write("Your estimated land lease rate as of today is  ", 5.75, "percent")

        else:
            st.write("trying to get data from another source")
            prop_val = get_property_data('value', address, zip_code, password)
            land_val = get_property_data('land_value', address, zip_code, password)
        # Assuming property and land value APIs return consistent data

            if prop_val and land_val and prop_val[0]['property/value']['api_code']==0 and land_val[0]['property/land_value']['api_code']==0:
                data = {
                    'address': address,
                    'zip_code': zip_code,
                    'land share': round(land_val[0]['property/land_value']['result']['land_value']['value_mean']/prop_val[0]['property/value']['result']['value']['price_mean'],3),
                   'land_value': land_val[0]['property/land_value']['result']['land_value']['value_mean'],
                        # 'land_value_upr': land_val[0]['property/land_value']['result']['land_value']['value_upr'],
                        # 'land_value_lwr': land_val[0]['property/land_value']['result']['land_value']['value_lwr'],
                    'property_value': prop_val[0]['property/value']['result']['value']['price_mean'],
                   # 'property_value_upr': prop_val[0]['property/value']['result']['value']['price_upr'],
                   # 'property_value_lwr': prop_val[0]['property/value']['result']['value']['price_lwr'],
                }
                land_finance =land_val[0]['property/land_value']['result']['land_value']['value_mean']
                st.write("congrats! Address :", address, zip_code, "is supported by Terrapin Program!")
                st.write("Terrapin would like to purchase the land of this address at ", land_finance)
                st.write("You can lease the land at  ", 4.75, "percent")

                df = pd.DataFrame([data])
                df_T = df.T
                #st.table(df_T)
                link = "https://www.google.com/search?q="
                link += address.replace(" ", "+") + "+" + zip_code
                link += "+zillow"
                st.markdown(link, unsafe_allow_html=True)
            else:
                st.write("Error retrieving data. Please contact support")

            # flood_risk_val = get_property_data('flood', address, zip_code, password)
            # if flood_risk_val and flood_risk_val[0]['property/flood']['api_code']==0:
            #     data = {
            #         'address': address,
            #         'zip_code': zip_code,
            #         'flood_risk_date': flood_risk_val[0]['property/flood']['result']['effective_date'],
            #         'flood_risk_zone': flood_risk_val[0]['property/flood']['result']['zone'],
            #         'flood_risk': flood_risk_val[0]['property/flood']['result']['flood_risk']
            #     }
            #     df = pd.DataFrame([data])
            #     df_T = df.T
            #     st.table(df_T)

    else:
        st.write(".")
def load_zipcode_data(zipcode):

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
    # Find the corresponding landshare using the dictionary
    #st.write(data_dict.get(input_zipcode))
    corresponding_landshare = data_dict.get(zipcode)

    if corresponding_landshare is None:
          st.write("Please enter a valid zipcode")
    else:
        corresponding_landshare = float(corresponding_landshare)
        corresponding_landshare = round(corresponding_landshare, 2)
        if corresponding_landshare >0.35:
            corresponding_landshare = 0.35
    return corresponding_landshare
def property_zip_code():
    today = datetime.today().strftime('%Y-%m-%d')

    # Format the title with the current date and lease rate
    lease_rate = 5.75
    st.title(f"Your estimated land lease rate as of {today} is {lease_rate}%")
    # today = datetime.today().strftime('%Y-%m-%d')
    # st.title('As Of ', today)
    # st.title("Your estimated land lease rate as of  5.75 percent")
    st.title("Property land share by zip code")
    # Prompt user to enter the password
    #password = st.text_input("Enter your email as password", type="password")
    zip_code = st.number_input("Any Denver Zip code", min_value=80000, step=1, value=80001)
    st.write('You entered:', zip_code)


    corresponding_landshare = load_zipcode_data(int(zip_code))
    #st.write(corresponding_landshare)
    print(corresponding_landshare)
    if corresponding_landshare is not None:
        corresponding_landshare = float(corresponding_landshare)
        corresponding_landshare = round(corresponding_landshare, 2)
        if corresponding_landshare >0.35:
            corresponding_landshare = 0.35
            st.write(f"Zip Code: {zip_code}, Our program will cover up to : {int(corresponding_landshare*100)} percent of the property value. Exmaple if the property value is 500,000, our program will cover ${int(corresponding_landshare*500000)}.")
        elif corresponding_landshare<0.15:
            st.write(f"Zip Code: {zip_code}, the land share is {corresponding_landshare}, which is too low for our program to make a meaningful impact.")
        else:
            st.write(f"Zip Code: {zip_code}, Our program will cover Land Share up to: {corresponding_landshare*100}", "percent of the property value")

    else:
        st.write(f"Zip Code: {zip_code}, we don't have data for this zipcode. Please try another one.")


def get_property_data(endpoint, address, zip_code, password):
    base_url = "https://api.housecanary.com/v2/property/"
    auth = (apiusername, password)
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

def compute_monthly_payments(P_guess, LTV, PMI_rate, home_insurance_rate_monthly, property_tax_rate_month, r, n, monthly_debt, land_share=None, land_lease_rate=None):

    #if land_share and land_lease_rate is not provide then property_value = P_guess / LTV, otherwise property_value = (P_guess / LTV) / (1 - land_share )
    property_value = (P_guess / LTV) / (1 - land_share) if land_share else P_guess / LTV
    monthly_PMI = P_guess * PMI_rate/1200

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


def find_optimal_loan(principal_loan_amount, LTV, PMI_rate, home_insurance_rate_monthly, property_tax_rate_month, r, n, monthly_debt, DTI_backend,DTI_front, monthly_income, land_share=None, land_lease_rate=None):
    low = 0
    high = 20 * principal_loan_amount
    if DEBUG:
        st.write("start guess!!!!!!!!!!!!!!!!!!withhigh, landshare", high,land_share)
        print("find_optimal_loan called, inputs are:")
        print("principal_loan_amount, LTV, PMI_rate, home_insurance_rate_monthly, property_tax_rate_month, r, n, monthly_debt, DTI_backend,DTI_front, monthly_income, land_share, land_lease_rate")
        print(principal_loan_amount, LTV, PMI_rate, home_insurance_rate_monthly, property_tax_rate_month, r, n, monthly_debt, DTI_backend,DTI_front, monthly_income, land_share, land_lease_rate)

    while high - low > 1:
        mid = (high + low) / 2

        if land_share:
            total_monthly_payments = compute_monthly_payments(mid, LTV, PMI_rate, home_insurance_rate_monthly, property_tax_rate_month, r, n, monthly_debt, land_share, land_lease_rate)
        else:
            total_monthly_payments = compute_monthly_payments(mid, LTV, PMI_rate, home_insurance_rate_monthly, property_tax_rate_month, r, n, monthly_debt)

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
    #          "8. if not, decrease the loan amount and repeat the process until it is affordable")
    if(land_lease_flag):
        if(title=="Tillt Affordability Calculator"):
            zipcode = st.sidebar.number_input("Zipcode", min_value=0, step=1, value=80002)
            if(load_zipcode_data(zipcode) is not None):
                    land_share =load_zipcode_data(int(zipcode))
                    st.sidebar.write("In this zip code", int(zipcode),"Tillt program can support land value up to", int(land_share*100), "percent of property value")
                    st.sidebar.write("Land Lease Rate (%)", 4.75)
                    land_lease_rate =4.75/100
            else:
                st.write("Sorry, the property in this zipcode is not supported yet. Please try another zipcode")

                return
        else:
            land_share = st.sidebar.number_input("Land Share", min_value=0, step=1, value=25)/100
            land_lease_rate = st.sidebar.number_input("Land Lease Rate (%)", min_value=0.0, step=0.05, value=4.75)/100
    st.sidebar.write("Please enter/update home buyer's information")
    with st.sidebar:
        col1, col2 = st.columns(2)

        with col1:

            annual_income = col1.number_input("Annual Income1", min_value=0, step=500, value=120000)
        with col2:
            monthly_debt = col2.number_input("Monthly Debt1", min_value=0, step=50, value=1200)
    with st.sidebar:
        with col1:
            interest_rate = col1.number_input("Interest Rate (%)", min_value=0.0, step=0.1, value=7.5)

        with col2:
            loan_term =col2.number_input("Loan Term (Years)", min_value=1, max_value=50, step=1, value=30)


    with st.sidebar:
        with col1:
            DTI_front = col1.number_input("Max Front-end DTI (%)", min_value=0.0, step=0.1, value=33.0)
        with col2:
            DTI_back = col2.number_input("Max Back-end DTI (%)", min_value=0.0, step=0.1, value=45.0)
    #annual_income = st.sidebar.number_input("Annual Income", min_value=0, step=500, value=120000)
    #monthly_debt = st.sidebar.number_input("Monthly Debt", min_value=0, step=50, value=1200)
    # st.sidebar.write("Monthly Income:", annual_income / 12.0)
    with st.sidebar:
        with col1:
            down_payment_percent = col1.number_input("Down Payment (%)", min_value=0.0, step=0.1, value=5.0) / 100
        with col2:
            property_tax_rate = col2.number_input("property_tax_rate (%)", min_value=0.0, step=0.01,
                                                    value=1.0) / 100
    with st.sidebar:
        with col1:
            PMI_rate = col1.number_input("PMI_rate ($per 100K)", min_value=0.0, step=0.1, value=0.78)
        with col2:
            annual_home_insurance_rate = col2.number_input("Home Insurance Rate %", min_value=0.0000,
                                                             step=0.01, value=0.35) / 100



    LTV = 1 - down_payment_percent
    property_tax_rate_month = property_tax_rate / 12
    home_insurance_rate_monthly = annual_home_insurance_rate / 12

    max_loan_without_land_lease = find_optimal_loan(500000, LTV, PMI_rate, home_insurance_rate_monthly,
                                                    property_tax_rate_month, interest_rate / 1200, loan_term * 12,
                                                    monthly_debt, DTI_back / 100, DTI_front / 100, annual_income / 12)
    max_home_price_without_land_lease = max_loan_without_land_lease / LTV
    if land_lease_flag == False:
        st.write("without land lease: loan and home price", max_loan_without_land_lease, max_home_price_without_land_lease)
        st.write("PMI_monthly", max_loan_without_land_lease * PMI_rate / 1200)
        st.write("home insurance", max_home_price_without_land_lease * home_insurance_rate_monthly)
        st.write("monthly_property_tax =", max_home_price_without_land_lease * property_tax_rate_month)
        st.write("monthly_mortgageP&I", compute_monthly_mortgage(max_loan_without_land_lease, interest_rate / 1200, loan_term * 12))
        st.write("loan", max_loan_without_land_lease)

    if land_lease_flag:
        max_loan = find_optimal_loan(500000, LTV, PMI_rate, home_insurance_rate_monthly,
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


        st.title("")

        # variable_output = st.text_input("Enter some text", value="Streamlit is awesome")
        # number = int(max_home_price_with_piti)
        # numbers = str()
        # variable_output = "$" +str({int(max_home_price_with_piti):,})
        # font_size = st.slider("Enter a font size", 1, 300, value=30)
        #
        # html_str = f"""
        # <style>
        # p.a {{
        #   font: bold {font_size}px Courier;
        # }}
        # </style>
        # <p class="a">{variable_output}</p>
        # """

        # st.markdown(html_str, unsafe_allow_html=True)
        st.markdown(
            f"<h3>Based on your inputs (on the left side), your maximum affordable home price with the Tillt land lease program is ${int(max_home_price_with_piti):,} </h3>",
            unsafe_allow_html=True)

        st.markdown(
            f"<h3>In the absence of a land lease, using only a traditional 30-year fixed rate mortgage, your maximum available home price is ${int(max_home_price_without_land_lease):,}</h3>",
            unsafe_allow_html=True)
        st.markdown(
            f"<h3>With the Tillt land lease program, your purchasing power has increased by {round(float(affordability), 2):,}%</h3>",
            unsafe_allow_html=True) 
    if land_lease_flag:
        total_monthly_pay = max_loan_without_land_lease * PMI_rate/1200 + max_home_price_without_land_lease * home_insurance_rate_monthly + max_home_price_without_land_lease * property_tax_rate_month+ compute_monthly_mortgage(max_loan_without_land_lease, interest_rate / 1200, loan_term * 12)
        total_monthly_pay_with_lease = max_loan * PMI_rate/1200 + max_home_price_with_piti * home_insurance_rate_monthly + max_home_price_with_piti * property_tax_rate_month + max_home_price_with_piti * land_share * land_lease_rate / 12 + compute_monthly_mortgage(max_loan, interest_rate / 1200, loan_term * 12)

        data1 = {
            "": ["Home Price Affordable($)","Loan Amount($)",  "Total Monthly Payment($)", "Monthly Mortgage Insurance($)", "Monthly Home Insurance($)",
                          "Monthly Property Tax($)", "Monthly Mortgage Principal&Interest($)", "Monthly Land Lease(S)"],
            "Without Land Lease": [int(max_home_price_without_land_lease),
                                   int(max_loan_without_land_lease),
                                   int(total_monthly_pay),
                                   int(max_loan_without_land_lease * PMI_rate/1200),
                                   int(max_home_price_without_land_lease*home_insurance_rate_monthly),
                                   int(max_home_price_without_land_lease*property_tax_rate_month),
                                   int( compute_monthly_mortgage(max_loan_without_land_lease, interest_rate / 1200, loan_term * 12)),
                                   0],
            "With Land Lease": [int(max_home_price_with_piti),
                                int(max_loan),
                                int(total_monthly_pay_with_lease),
                                int(max_loan * PMI_rate/1200),
                                int(max_home_price_with_piti * home_insurance_rate_monthly),
                                int(max_home_price_with_piti * property_tax_rate_month),
                                int(compute_monthly_mortgage(max_loan, interest_rate / 1200, loan_term * 12)),
                                int(max_home_price_with_piti * land_share * land_lease_rate / 12)
                                ]
        }
        df1 = pd.DataFrame(data1)

        st.write(df1.to_html(index=False), unsafe_allow_html=True)


    else:
        st.write("something wrong with your input, please check again")

    cpi = st.number_input("CPI assumption % for current year", min_value=0.0, step=0.1, value=2.0)
    st.markdown(
            f"<h3>Illustrative 10-year Lease Payment Schedule with CPI assumption {cpi:,} percent</h3>",
            unsafe_allow_html=True)
    # st.write("Lease Payment Schedule for first 10 years")

         #calculate monthly payment increase every 6 months and land price increase every 6 months
    leasepay_schedule = generate_leasepay_schedule(land_share*max_home_price_with_piti, land_lease_rate, cpi/200, 10)
    df = pd.DataFrame(leasepay_schedule)
    #format df's first two columns to integer

    for col in df.columns[0:2]:
         df[col] = df[col].astype(int)

    for col in df.columns[3:5]:
        df[col] = df[col].astype(int)

    st.write(df.to_html(index=False), unsafe_allow_html=True)
    st.write("Calculated Front-end and Back-end DTI based on inputs",
             round(total_monthly_pay_with_lease / (annual_income / 12), 6),
             round((total_monthly_pay_with_lease + monthly_debt) / (annual_income / 12), 6))

    st.write("***Disclaimer: This calculator is offered for illustrative and educational purposes only and it is not intended to replace a professional estimate. Calculator results do not reflect all loan types and are subject to individual program loan limits. All calculations and costs are estimates and therefore, Terrapin Impact Partner does not make any guarantee or warranty (express or implied) that all possible costs have been included. The assumptions made here and the output of the calculator do not constitute a loan offer or solicitation, or financial or legal advice. Please connect with a loan professional for a formal estimate. Every effort is made to maintain accurate calculations; however, Terrapin assumes no liability to any third parties that rely on this information and is not responsible for the accuracy of rates, APRs or any other loan information factored in the calculations.")


def generate_leasepay_schedule(land_value, lease_rate, CPI_halfyear, years):
    leasepay_schedule = pd.DataFrame(columns=[
        'Month', 'Right to Purchase Land $ ', 'Lease Rate (%)', 'Monthly Lease Payment $', 'Payment Adjustment $', 'Adjustment %'])

    for p in range(0, years*2):
        month =p*6

        if month == 0:
            last_month_lease_payment = land_value * lease_rate / 12
            new_land_value=land_value
        else:
            last_month_lease_payment = leasepay_schedule.loc[month-6, 'Monthly Lease Payment $']
            new_land_value = land_value * (1 + CPI_halfyear) ** p
        monthly_lease_payment = new_land_value * lease_rate / 12
        increase_dollar = monthly_lease_payment - last_month_lease_payment
        increase_percent = CPI_halfyear * 100
        #st.write(month, new_land_value, monthly_lease_payment, last_month_lease_payment,increase_dollar, increase_percent)
        leasepay_schedule.loc[month] = [month, new_land_value, lease_rate*100, monthly_lease_payment, increase_dollar, increase_percent]

    return leasepay_schedule
def home_affordability_payment_app():
    st.title("Monthly Payment Calculator")
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
    PMI_rate = st.sidebar.number_input("PMI rate%", min_value=0.0, step=0.01, value=0.78)
    annual_home_insurance_rate = st.sidebar.number_input("Home insurance rate %", min_value=0.0000,
                                                         step=0.01, value=0.35) / 100

    annual_income = st.sidebar.number_input("Annual Income", min_value=0, step=500, value=120000)
    monthly_debt = st.sidebar.number_input("Monthly Debt", min_value=0, step=50, value=1200)

    property_tax_rate_month = property_tax_rate / 12
    home_insurance_rate_monthly = annual_home_insurance_rate / 12

    max_loan_without_land_lease= home_price * LTV
    max_loan_with_land_lease = home_price * (1-land_share) * LTV

    mortgage_insurance_monthly = max_loan_without_land_lease * PMI_rate / 1200
    home_insurance_monthly = home_price * home_insurance_rate_monthly
    property_tax_monthly = home_price * property_tax_rate_month
    monthly_mortgageP_I = compute_monthly_mortgage(max_loan_without_land_lease, interest_rate / 1200, loan_term * 12)
    total_monthly_pay = home_insurance_monthly + property_tax_monthly + monthly_mortgageP_I + mortgage_insurance_monthly

    monthly_lease =home_price * land_share * land_lease_rate / 12
    mortgage_insurance_monthly_l = max_loan_with_land_lease * PMI_rate / 1200
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
    data = {"":["Home Price", "Loan Amount", "down payment", "Total monthly payment", "PMI Monthly", "Home Insurance", "Property Tax Monthly", "Mortgage P&I", "Land Lease Monthly"],
            "Without Land Lease":[int(home_price),int(max_loan_without_land_lease),int(home_price * down_payment_percent),
                                  int(total_monthly_pay),int(mortgage_insurance_monthly),int(home_insurance_monthly),int(property_tax_monthly),int(monthly_mortgageP_I),0],
             "With Land Lease":[int(home_price),int(max_loan_with_land_lease),int(home_price * down_payment_percent),
                                    int(total_monthly_pay_l),int(mortgage_insurance_monthly_l),int(home_insurance_monthly_l),int(property_tax_monthly_l),int(monthly_mortgageP_I_l),int(monthly_lease)
                                ]
            }

    df = pd.DataFrame(data)
    st.write(df.to_html(index=False), unsafe_allow_html=True)

    if st.button("Show Lease Payment Schedule"):

        leasepay_schedule= generate_leasepay_schedule(home_price*land_share,land_lease_rate,0.01, 10)
        df = pd.DataFrame(leasepay_schedule)
        # format df's first two columns to integer

        for col in df.columns[:4]:
            df[col] = df[col].astype(int)

        st.write(df.to_html(index=False), unsafe_allow_html=True)
    else:
        st.write("Please click the button to show lease payment schedule")
    st.write(
        "***Disclaimer: This calculator is offered for illustrative and educational purposes only and it is not intended to replace a professional estimate. Calculator results do not reflect all loan types and are subject to individual program loan limits. All calculations and costs are estimates and therefore, Terrapin Impact Partner does not make any guarantee or warranty (express or implied) that all possible costs have been included. The assumptions made here and the output of the calculator do not constitute a loan offer or solicitation, or financial or legal advice. Please connect with a loan professional for a formal estimate. Every effort is made to maintain accurate calculations; however, Terrapin assumes no liability to any third parties that rely on this information and is not responsible for the accuracy of rates, APRs or any other loan information factored in the calculations.")


if __name__ == "__main__":
    main()
