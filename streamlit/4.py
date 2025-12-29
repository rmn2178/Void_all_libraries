import streamlit as st
from pathlib import Path

# Title and Description
st.title("User Submission Form")
st.write("Please fill out the details below.")

# Initialize a form
with st.form(key="user_info_form"):
    # Text input fields
    name = st.text_input("Full Name")
    email = st.text_input("Email Address")

    # Numeric and Date inputs
    age = st.number_input("Age", min_value=1, max_value=120, value=25)
    date_submitted = st.date_input("Today's Date")

    # Selection inputs
    department = st.selectbox(
        "Department",
        ["Engineering", "Sales", "Marketing", "Design"]
    )

    # Multi-line text area
    feedback = st.text_area("Additional Comments")

    # Every form must have a submit button
    submit_button = st.form_submit_button(label="Submit Form")

# Logic after clicking Submit
if submit_button:
    if name and email:
        st.success(f"Thank you, {name}! Your submission for the {department} department has been received.")

        # Displaying the data back to the user
        st.info("Here is the data you submitted:")
        st.json({
            "Name": name,
            "Email": email,
            "Age": age,
            "Date": str(date_submitted),
            "Department": department,
            "Comments": feedback
        })
    else:
        st.warning("Please enter at least your name and email address.")