
import streamlit as st
import requests

st.set_page_config(
    page_title="MediShare",
    page_icon="💊",
    layout="wide"
)

# FastAPI backend URL
API_URL = st.secrets.get(
    "API_URL",
    "http://127.0.0.1:8000"
).rstrip("/")

st.title("💊 MediShare")
st.subheader("Medicine Donation Portal")

st.write(
    "Donate eligible medicines and help people "
    "in need through our donation platform."
)

# Backend connection
with st.sidebar:
    st.header("Backend Connection")

    if st.button("Check Backend"):
        try:
            response = requests.get(
                f"{API_URL}/health",
                timeout=20
            )

            if response.status_code == 200:
                st.success("FastAPI connected!")
                st.json(response.json())
            else:
                st.error(
                    f"Backend returned {response.status_code}"
                )

        except requests.RequestException as e:
            st.error(f"Connection failed: {e}")


tab1, tab2, tab3, tab4 = st.tabs([
    "Donate Medicine",
    "View Donations",
    "Update Status",
    "Delete Donation"
])


# POST - Add donation
with tab1:
    st.header("Donate Medicine")

    with st.form("donation_form"):
        donor = st.text_input("Donor Name")
        medicine = st.text_input("Medicine Name")
        quantity = st.number_input(
            "Quantity", min_value=1, step=1
        )
        expiry = st.date_input("Expiry Date")
        location = st.text_input("Location")
        contact = st.text_input("Contact Number")
        description = st.text_area("Description")

        submit = st.form_submit_button("Submit Donation")

        if submit:
            data = {
                "donor_name": donor,
                "medicine_name": medicine,
                "quantity": quantity,
                "expiry_date": expiry.isoformat(),
                "location": location,
                "contact": contact,
                "description": description
            }

            try:
                response = requests.post(
                    f"{API_URL}/donations",
                    json=data,
                    timeout=20
                )

                if response.status_code == 201:
                    st.success("Donation submitted successfully!")
                    st.json(response.json())
                else:
                    st.error(response.text)

            except requests.RequestException as e:
                st.error(f"Connection error: {e}")


# GET - View donations
with tab2:
    st.header("All Donations")

    if st.button("Load Donations"):
        try:
            response = requests.get(
                f"{API_URL}/donations",
                timeout=20
            )

            if response.status_code == 200:
                result = response.json()

                st.metric(
                    "Total Donations",
                    result["total"]
                )

                if result["donations"]:
                    st.dataframe(
                        result["donations"],
                        use_container_width=True
                    )
                else:
                    st.info("No donations available.")

            else:
                st.error(response.text)

        except requests.RequestException as e:
            st.error(f"Connection error: {e}")


# PUT - Update donation
with tab3:
    st.header("Update Donation Status")

    donation_id = st.text_input(
        "Donation ID",
        key="update_id"
    )

    status = st.selectbox(
        "Select Status",
        ["Pending", "Approved", "Rejected", "Collected"]
    )

    if st.button("Update Status"):
        if not donation_id.strip():
            st.warning("Enter a donation ID.")
        else:
            try:
                response = requests.put(
                    f"{API_URL}/donations/{donation_id}",
                    json={"status": status},
                    timeout=20
                )

                if response.status_code == 200:
                    st.success("Status updated successfully!")
                    st.json(response.json())
                else:
                    st.error(response.text)

            except requests.RequestException as e:
                st.error(f"Connection error: {e}")


# DELETE - Delete donation
with tab4:
    st.header("Delete Donation")

    delete_id = st.text_input("Donation ID to delete")

    if st.button("Delete Donation"):
        if not delete_id.strip():
            st.warning("Enter a donation ID.")
        else:
            try:
                response = requests.delete(
                    f"{API_URL}/donations/{delete_id}",
                    timeout=20
                )

                if response.status_code == 200:
                    st.success("Donation deleted successfully!")
                else:
                    st.error(response.text)

            except requests.RequestException as e:
                st.error(f"Connection error: {e}")


st.divider()
st.caption("MediShare | Medicine Donation Portal")
