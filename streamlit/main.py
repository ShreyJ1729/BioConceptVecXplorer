import streamlit as st
import requests
import pandas as pd

def process_input(user_input):
    url = f'/process_input'
    data = {"user_input": user_input}
    r = requests.post(url, json=data)
    options = r.json()
    return options

def select_option(options):
    selected_option = st.selectbox("Select a similar concept:", options)
    if selected_option:
        st.write("You selected:", selected_option)
    return selected_option

def get_free_var_search(extracted_string, threshold):
    url = f'/free_var_search'
    data = {"extracted_string": extracted_string, "threshold": threshold}
    r = requests.post(url, json=data)
    df = pd.DataFrame(r.json())
    return df

# Set up the Streamlit page
st.title("BioConceptVec Exploration App")

# Get the user's input
user_input = st.text_input("Enter a concept:")

if user_input:
    options = process_input(user_input)
    if options:
        option = select_option(options)
        if option:
            start_index = option.find(":") + 1
            end_index = option.find("|")
            extracted_string = option[start_index:end_index].strip()
            st.write(extracted_string)
            # Make an input box from 0.0 to 1.0 by increments of 0.1 multiselect
            threshold = st.multiselect("Select a threshold:", [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7])
            if threshold:
                threshold = threshold[0]
                df = get_free_var_search(extracted_string, threshold)

                # Display a download button
                st.download_button(
                    label="Download CSV",
                    data=df.to_csv(index=False),
                    file_name="res.csv",
                    mime="text/csv",
                )

                # Show the dataframe
                st.dataframe(df)
