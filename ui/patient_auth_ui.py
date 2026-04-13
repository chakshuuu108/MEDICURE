"""
Patient authentication UI — Google Sign-In gate before Patient ID entry.
"""

import streamlit as st
from agents.scheduling_agent import get_auth_url


def render_patient_google_login():
    if st.session_state.get("patient_google_authed"):
        return True

    if st.session_state.get("google_access_token"):
        st.session_state["patient_google_authed"] = True
        return True

    # If user clicked the button on previous rerun, redirect now via meta refresh
    if st.session_state.get("_do_google_redirect"):
        auth_url = st.session_state.pop("_do_google_redirect")
        st.markdown(
            f'<meta http-equiv="refresh" content="0; url={auth_url}">',
            unsafe_allow_html=True,
        )
        st.stop()

    # ── Sign-In UI ────────────────────────────────────────────────────────────
    st.markdown("""
    <div style="max-width: 480px; margin: 3rem auto; text-align: center;">
        <div style="font-size: 3.5rem; margin-bottom: 0.8rem;">🏥</div>
        <h1 style="font-size: 2rem; font-weight: 800;
            background: linear-gradient(135deg, #A78BFA, #7C3AED);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            margin-bottom: 0.4rem;">Patient Portal</h1>
        <p style="color: #A89FC8; font-size: 1rem; margin-bottom: 2rem;">
            Sign in with Google to securely access your health dashboard
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        try:
            from core.config import GOOGLE_OAUTH_CLIENT_ID
            if not GOOGLE_OAUTH_CLIENT_ID:
                st.error("❌ GOOGLE_OAUTH_CLIENT_ID is missing from secrets!")
                return False

            auth_url = get_auth_url()

            # Style the native st.button to look like Google Sign-In
            st.markdown("""
            <style>
            div[data-testid="stButton"] > button {
                background: #ffffff !important;
                color: #3c4043 !important;
                border: 1px solid #dadce0 !important;
                border-radius: 8px !important;
                padding: 10px 24px !important;
                font-size: 15px !important;
                font-weight: 500 !important;
                font-family: 'Roboto', Arial, sans-serif !important;
                box-shadow: 0 1px 3px rgba(0,0,0,0.2) !important;
                width: 100% !important;
            }
            div[data-testid="stButton"] > button:hover {
                box-shadow: 0 2px 8px rgba(0,0,0,0.3) !important;
                background: #f8f8f8 !important;
            }
            </style>
            """, unsafe_allow_html=True)

            # Render the Google logo above the button using st.markdown
            st.markdown("""
            <div style="display:flex; align-items:center; justify-content:center;
                        gap:10px; margin-bottom:-1.5rem; pointer-events:none;">
                <svg width="20" height="20" viewBox="0 0 18 18" xmlns="http://www.w3.org/2000/svg">
                  <path fill="#4285F4" d="M16.51 8H8.98v3h4.3c-.18 1-.74 1.48-1.6 2.04v2.01h2.6a7.8 7.8 0 002.38-5.88c0-.57-.05-.66-.15-1.18z"/>
                  <path fill="#34A853" d="M8.98 17c2.16 0 3.97-.72 5.3-1.94l-2.6-2a4.8 4.8 0 01-7.18-2.54H1.83v2.07A8 8 0 008.98 17z"/>
                  <path fill="#FBBC05" d="M4.5 10.52a4.8 4.8 0 010-3.04V5.41H1.83a8 8 0 000 7.18l2.67-2.07z"/>
                  <path fill="#EA4335" d="M8.98 4.18c1.17 0 2.23.4 3.06 1.2l2.3-2.3A8 8 0 001.83 5.4L4.5 7.49a4.77 4.77 0 014.48-3.31z"/>
                </svg>
            </div>
            """, unsafe_allow_html=True)

            if st.button("      Sign in with Google", use_container_width=True):
                # Store auth_url and rerun — on next run meta refresh fires
                st.session_state["_do_google_redirect"] = auth_url
                st.rerun()

        except Exception as e:
            st.error(f"❌ Error setting up Google Sign-In: {e}")

        st.markdown("""
        <p style="color:#6B6080; font-size:0.75rem; text-align:center; margin-top:1.5rem;">
            🔒 Your health data is private and secure.<br>
            Google sign-in also enables Calendar sync for your medication schedule.
        </p>
        """, unsafe_allow_html=True)

    return False
