import streamlit as st
import importlib
from streamlit_oauth import OAuth2Component
import requests

CLIENT_ID     = ""
CLIENT_SECRET = ""
REDIRECT_URI  = "http://localhost:8501"

st.set_page_config(page_title="Anime Recommendation System", page_icon="🎥", layout="wide")

# ─── Page Routing ───────────────────────────────────────────────
params = st.experimental_get_query_params()
page   = params.get("page", ["login"])[0]

if page == "deploy_mix":
    import pages.anime_recommender_page  # runs all top-level code in deploy_mix.py
    importlib.reload(pages.anime_recommender_page)
    st.stop()

# ─── Otherwise, show login flow ────────────────────────────
oauth2 = OAuth2Component(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    authorize_endpoint="https://accounts.google.com/o/oauth2/v2/auth",
    token_endpoint="https://oauth2.googleapis.com/token",
)

if "token" not in st.session_state:
    st.session_state.token = None
if "profile" not in st.session_state:
    st.session_state.profile = None

st.title("🔐 Streamlit App with Google Authentication")

if st.session_state.token is None:
    token = oauth2.authorize_button(
        name="Login with Google",
        redirect_uri=REDIRECT_URI,
        scope="openid email profile",
    )

    if token and isinstance(token, dict):
        at = token.get("access_token") or token.get("token", {}).get("access_token")
        st.write("🔍 Raw token:", token)

        if at:
            st.session_state.token = at
            prof = requests.get(
                "https://www.googleapis.com/oauth2/v1/userinfo",
                headers={"Authorization": f"Bearer {at}"}
            ).json()

            if prof:
                st.session_state.profile = prof
                # ← Use the experimental setter
                st.experimental_set_query_params(page="deploy_mix")
                st.rerun()
            else:
                st.error("Failed to fetch profile.")
        else:
            st.error("Login failed: no access_token found.")
    else:
        st.error("Login failed: token invalid or missing.")
