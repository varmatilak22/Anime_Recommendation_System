import streamlit as st
import importlib
from streamlit_oauth import OAuth2Component
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# ─── Configuration ───────────────────────────────────────────────
CLIENT_ID=os.getenv("CLIENT_ID")
CLIENT_SECRET=os.getenv("CLIENT_SECRET")
REDIRECT_URI  = "http://localhost:8501"

st.set_page_config(page_title="ANIFLIX Login", layout="centered")

params = st.query_params
page = params.get("page", "login")

if page == "anime_recommender_page":
    import pages.anime_recommender_page
    importlib.reload(pages.anime_recommender_page)
    st.stop()

# ─── OAuth2 Component ────────────────────────────────────────────
oauth2 = OAuth2Component(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    authorize_endpoint="https://accounts.google.com/o/oauth2/v2/auth",
    token_endpoint="https://oauth2.googleapis.com/token",
    # auth_params={"prompt": "select_account"}
    
)

if "token" not in st.session_state:
    st.session_state.token = None
if "profile" not in st.session_state:
    st.session_state.profile = None

# ─── Custom CSS ──────────────────────────────────────────────────
st.markdown("""
    <style>
    body {
        background-color: #000;
        color: #fff;
         display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }
    
    .logo {
        font-size: 4rem;
        font-weight: bold;
        color: #E50914;
        margin-bottom: 30px;
        font-family: 'Arial Black', sans-serif;
        letter-spacing: 2px;
        text-align:center;
    }
    .button {
        width: 100%;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# ─── Centered Login UI ───────────────────────────────────────────
st.markdown('<div class="centered">', unsafe_allow_html=True)
st.markdown('<div class="logo">ANIFLIX</div>', unsafe_allow_html=True)
st.markdown('<div class="login-box">', unsafe_allow_html=True)

st.text_input("Email", key="email_input")
st.text_input("Password", type="password", key="pass_input")

if st.button("Login with Email", type="primary", use_container_width=True):
    st.success("✅ Placeholder Email login")

# ─── OAuth Buttons ───────────────────────────────────────────────
st.markdown("##### Or sign in with:")
token = oauth2.authorize_button(
    name="Login with Google",
    redirect_uri=REDIRECT_URI,
    scope="openid email profile",
    use_container_width=True,
     #extra_params={"prompt": "select_account"}
)


# Optionally add placeholders for other OAuth (Microsoft, Apple)
st.button("Continue with Microsoft", type="secondary", use_container_width=True)
st.button("Continue with Apple", type="secondary", use_container_width=True)

st.markdown("</div></div>", unsafe_allow_html=True)

# ─── Handle Token ────────────────────────────────────────────────
if token and isinstance(token, dict):
    access_token = token.get("access_token") or token.get("token", {}).get("access_token")

    if access_token:
        st.session_state.token = access_token
        prof = requests.get(
            "https://www.googleapis.com/oauth2/v1/userinfo",
            headers={"Authorization": f"Bearer {access_token}"}
        ).json()

        if prof:
            st.session_state.profile = prof
            st.query_params.page = "anime_recommender_page"
            st.rerun()
        else:
            st.error("❌ Failed to fetch Google profile.")
