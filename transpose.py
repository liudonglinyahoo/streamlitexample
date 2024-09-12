

import pandas as pd
import streamlit as st
# Create a sidebar container

df = pd.DataFrame({"Name": ["Alice", "Bob", "Carol"], "Age": [25, 30, 35]})

# Transpose the data frame
df_transposed = df.T

# Print the transposed data frame
print(df_transposed)
print(df)
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
corresponding_landshare = data_dict.get(80001)
print(corresponding_landshare)
if corresponding_landshare is None:
    print("None!!!")

import pandas as pd

data1 = {
        "Condition": ["Loan Amount", "Home Price", "Total monthly payment", "PMI Monthly", "Home Insurance",
                      "Property Tax Monthly", "Mortgage P&I", "Land Lease Monthly"],
        "Without Land Lease": [373879, 393557, 3299, 243, 114, 327, 2614, 0],
        "With Land Lease": [281867, 456466, 3299, 183, 133, 380, 1970, 632]
    }

dfa = pd.DataFrame(data1)

print(dfa)
st.write(dfa)

tab1, tab2, tab3 = st.tabs(["Cat", "Dog", "Owl"])

with tab1:
   st.header("A cat")
   st.image("https://static.streamlit.io/examples/cat.jpg", width=200)

with tab2:
   st.header("A dog")
   st.image("https://static.streamlit.io/examples/dog.jpg", width=200)

with tab3:
   st.header("An owl")
   st.image("https://static.streamlit.io/examples/owl.jpg", width=200)
# Transpose the data frame
# transposed_data = data.T
# print(data)
# # Print the transposed data frame
# print(transposed_data)

# Direct URL to the public CSV file in S3
#url = "https://s3.amazonaws.com/donglintonyliu.click/HCloandshare.csv"
url = "https://s3.amazonaws.com/donglintonyliu.click/merged_zillow_hcloandshare.csv"
# Read the CSV file into a DataFrame
df1 = pd.read_csv(url)
st.write(df1)
st.dataframe(df1)
# Print the DataFrame
print(df1)
#addresses = [('517 N Chugach St', '99645'), ('12731 Schooner Dr', '99515')]
# Extract addresses and zipcodes as a list of tuples
addresses = list(zip(df1['streetName'], df1['zipcode'].astype(str)))

addresses[:5]  # Display the first 5 addresses to check the result

# Display the dropdown for the user to select an address
selected_address = st.selectbox("Select an address:", addresses)
