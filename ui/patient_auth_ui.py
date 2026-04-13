"""
Patient authentication UI — Google Sign-In gate before Patient ID entry.

Flow:
  1. User clicks "Sign in with Google"
  2. OAuth redirect → callback handled by _handle_google_oauth_callback() in patient_ui
  3. google_access_token stored in session → patient_google_authed = True
  4. Patient ID input shown; on success patient_logged_in = True

Google Sign-In is the ONLY login method. No guest / Patient-ID-only bypass.
"""

import streamlit as st
from agents.scheduling_agent import get_auth_url


def render_patient_google_login():
    """
    Render the Google Sign-In page for patients.
    Returns True if the patient has been Google-authenticated.
    Returns False and renders the login UI if not yet authenticated.
    """
    # Already authenticated in this session?
    if st.session_state.get("patient_google_authed"):
        return True

    # Arrived back from Google OAuth redirect — tokens already exchanged by
    # _handle_google_oauth_callback() at app level before this is called.
    if st.session_state.get("google_access_token"):
        st.session_state["patient_google_authed"] = True
        return True

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

            # st.link_button is Streamlit's native external-link button.
            # It renders as a proper <a> tag handled by Streamlit itself,
            # navigating the top-level window in the same tab — no iframe issues.
            st.markdown("""
            <style>
            [data-testid="stLinkButton"] a {
                display: flex !important;
                align-items: center !important;
                justify-content: center !important;
                gap: 0.75rem !important;
                background: #ffffff !important;
                color: #3c4043 !important;
                border: 1px solid #dadce0 !important;
                border-radius: 8px !important;
                padding: 0.75rem 1.5rem !important;
                font-size: 0.95rem !important;
                font-weight: 500 !important;
                text-decoration: none !important;
                box-shadow: 0 1px 3px rgba(0,0,0,0.2) !important;
                transition: box-shadow 0.2s !important;
                width: 100% !important;
                box-sizing: border-box !important;
            }
            [data-testid="stLinkButton"] a:hover {
                box-shadow: 0 2px 6px rgba(0,0,0,0.3) !important;
                background: #f8f8f8 !important;
                color: #3c4043 !important;
            }
            </style>
            """, unsafe_allow_html=True)

            st.link_button("🔵  Sign in with Google", url=auth_url, use_container_width=True)

        except Exception as e:
            st.error(f"❌ Error setting up Google Sign-In: {e}")

        st.markdown("""
        <p style="color:#6B6080; font-size:0.75rem; text-align:center; margin-top:1.5rem;">
            🔒 Your health data is private and secure.<br>
            Google sign-in also enables Calendar sync for your medication schedule.
        </p>
        """, unsafe_allow_html=True)

    return False
