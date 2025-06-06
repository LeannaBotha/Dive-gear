import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="Dive Gear Tracker", layout="centered")

st.title("🤿 Dive Gear Tracker")

# Initialize session state for gear inventory
if "gear" not in st.session_state:
    st.session_state["gear"] = []

# Add new gear
st.header("Add New Gear")
with st.form("add_gear"):
    name = st.text_input("Gear Name")
    gear_type = st.selectbox("Type", ["BCD", "Regulator", "Mask", "Fins", "Wetsuit", "Computer", "Tank", "Other"])
    acquired = st.date_input("Date Acquired", value=date.today())
    condition = st.selectbox("Condition", ["Excellent", "Good", "Needs Service", "Retired"])
    submit = st.form_submit_button("Add Gear")

    if submit:
        if name:
            st.session_state["gear"].append({
                "Name": name,
                "Type": gear_type,
                "Date Acquired": acquired,
                "Condition": condition,
                "Serviced": "No"
            })
            st.success(f"{name} added to your gear inventory.")
        else:
            st.error("Please enter a gear name.")

# Display gear inventory
st.header("Your Gear Inventory")

if st.session_state["gear"]:
    df = pd.DataFrame(st.session_state["gear"])
    st.dataframe(df, use_container_width=True)

    # Service or retire gear
    st.subheader("Update Gear Status")
    selected_gear = st.selectbox("Select gear to update", df["Name"])
    action = st.radio("Action", ["Mark as Serviced", "Mark as Retired"])

    if st.button("Update Status"):
        gear_list = st.session_state["gear"]
        for gear in gear_list:
            if gear["Name"] == selected_gear:
                if action == "Mark as Serviced":
                    gear["Serviced"] = "Yes"
                    st.success(f"{selected_gear} marked as serviced.")
                elif action == "Mark as Retired":
                    gear["Condition"] = "Retired"
                    st.success(f"{selected_gear} marked as retired.")
        st.session_state["gear"] = gear_list

    # Download as CSV
    st.subheader("Download Inventory")
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("Download as CSV", csv, "dive_gear_inventory.csv", "text/csv")
else:
    st.info("No dive gear added yet.")

st.caption("Made with Streamlit • © 2025 Your Name")
