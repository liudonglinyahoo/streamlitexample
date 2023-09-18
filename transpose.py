import pandas as pd

# Sample data frame
data = pd.DataFrame({
    'Name': ["Alice", "Bob", "Charlie"],
    'Age': [25, 30, 22],
    'Score': [95, 89, 78]
})

# Transpose the data frame
transposed_data = data.T
print(data)
# Print the transposed data frame
print(transposed_data)
