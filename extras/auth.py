import streamlit as st
from streamlit_oauth import OAuth2Component
import requests

# ---- SET YOUR GOOGLE CLOUD CREDENTIALS HERE ----
CLIENT_ID = ""
CLIENT_SECRET = ""
REDIRECT_URI = "http://localhost:8501"  # Or your deployed URL

# ---- INITIALIZE OAUTH2 ----
oauth2 = OAuth2Component(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    authorize_endpoint="https://accounts.google.com/o/oauth2/v2/auth",
    token_endpoint="https://oauth2.googleapis.com/token",
)

# ---- SESSION STATE HANDLING ----
if "token" not in st.session_state:
    st.session_state.token = None
if "profile" not in st.session_state:
    st.session_state.profile = None

# ---- SCOPES (as a space-separated string) ----
scopes = "openid email profile"

st.title("🔐 Streamlit App with Google Authentication")

# ---- LOGIN FLOW ----
if st.session_state.token is None:
    token = oauth2.authorize_button(
        name="Login with Google",
        redirect_uri=REDIRECT_URI,  # <-- Add redirect_uri here
        scope=scopes  # <-- Pass scope as a string here
    )

    if token:
        # Check if the token is properly returned and access_token is nested
        if "token" in token and "access_token" in token["token"]:
            access_token = token["token"]["access_token"]
            st.session_state.token = access_token
            st.write("Access Token:", access_token)  # Debugging: Check if access token is correct

            # Fetch user profile info using the access token
            headers = {"Authorization": f"Bearer {access_token}"}
            try:
                profile_info = requests.get("https://www.googleapis.com/oauth2/v1/userinfo", headers=headers).json()
                # Check if profile_info is valid
                if profile_info:
                    st.session_state.profile = profile_info
                    st.rerun()  # Re-run the script to refresh the state
                else:
                    st.error("Failed to fetch profile information. Please try again.")
            except Exception as e:
                st.error(f"Error fetching profile: {e}")
        else:
            st.error("No access token received. Please try again.")

# ---- AFTER LOGIN ----
else:
    profile = st.session_state.profile
    if profile:
        st.success(f"Welcome {profile.get('name', 'User')}! 👋")
        st.image(profile.get('picture', ''), width=100)
        st.write(f"**Email:** {profile.get('email', 'N/A')}")
    else:
        st.error("Profile data is missing. Please log in again.")

    # ---- Logout ----
    if st.button("Logout"):
        st.session_state.token = None
        st.session_state.profile = None
        st.rerun()