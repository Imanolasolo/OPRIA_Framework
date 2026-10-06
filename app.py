import streamlit as st
from urllib.parse import quote_plus
from content import CONTENT
from translations import TRANSLATIONS
from database import init_db, save_contact, save_business_check


# ---------------------------------------------------------
# CONFIG
# ---------------------------------------------------------

st.set_page_config(
    page_title="OPRIA — Business Growth & Management System",
    page_icon="◉",
    layout="wide",
    initial_sidebar_state="collapsed",
)

init_db()

WHATSAPP_NUMBER = "593993513082"

if "language" not in st.session_state:
    st.session_state.language = "en"


# ---------------------------------------------------------
# HELPERS
# ---------------------------------------------------------

def t(key):
    return TRANSLATIONS[st.session_state.language].get(key, key)


def switch_language():
    st.session_state.language = (
        "es" if st.session_state.language == "en" else "en"
    )


def build_whatsapp_url(name, company, email, message):
    intro = (
        "Hola, te escribo desde OPRIA."
        if st.session_state.language == "es"
        else "Hello, I am writing from OPRIA."
    )

    lines = [intro, ""]

    if name:
        lines.append(f"Nombre: {name}" if st.session_state.language == "es" else f"Name: {name}")

    if company:
        lines.append(f"Empresa: {company}" if st.session_state.language == "es" else f"Company: {company}")

    if email:
        lines.append(f"Email: {email}")

    if message:
        lines.append(message)

    text = "\n".join(lines)
    return f"https://wa.me/{WHATSAPP_NUMBER}?text={quote_plus(text)}"


# ---------------------------------------------------------
# STYLE
# ---------------------------------------------------------

st.markdown(
    """
    <style>

    .stApp {
        background: #0b0b0b;
        color: #f2f2f2;
    }

    section[data-testid="stSidebar"] {
        display: none;
    }

    .block-container {
        max-width: 1100px;
        padding-top: 2rem;
        padding-bottom: 5rem;
    }

    .opria-logo {
        font-size: 2rem;
        font-weight: 800;
        letter-spacing: 0.15em;
    }

    .hero-title {
        font-size: clamp(3rem, 7vw, 6.5rem);
        line-height: 0.95;
        font-weight: 800;
        letter-spacing: -0.05em;
        margin-top: 5rem;
        margin-bottom: 2rem;
    }

    .hero-subtitle {
        font-size: 1.35rem;
        line-height: 1.6;
        max-width: 760px;
        color: #bdbdbd;
    }

    .section-title {
        font-size: 2.5rem;
        font-weight: 750;
        margin-top: 5rem;
        margin-bottom: 1rem;
    }

    .red {
        color: #ff3b30;
    }

    .small-label {
        color: #888;
        font-size: 0.8rem;
        letter-spacing: 0.15em;
        text-transform: uppercase;
    }

    div[data-testid="stExpander"] {
        border: 1px solid #292929;
        border-radius: 8px;
        background: #111111;
        margin-bottom: 0.6rem;
    }

    div[data-testid="stExpander"] details summary p {
        font-size: 1.05rem;
        font-weight: 600;
    }

    .framework-number {
        font-size: 0.8rem;
        color: #777;
        letter-spacing: 0.1em;
    }

    .framework-name {
        font-size: 1.8rem;
        font-weight: 700;
    }

    .footer {
        margin-top: 6rem;
        padding-top: 2rem;
        border-top: 1px solid #292929;
        color: #666;
        text-align: center;
    }

    div[data-testid="stRadio"] [role="radiogroup"] label,
    div[data-testid="stRadio"] [role="radiogroup"] label p,
    div[data-testid="stRadio"] [role="radiogroup"] span {
        color: #f5f5f5 !important;
        opacity: 1 !important;
    }

    div[data-testid="stRadio"] [role="radiogroup"] label:hover,
    div[data-testid="stRadio"] [role="radiogroup"] label:hover p,
    div[data-testid="stRadio"] [role="radiogroup"] label:hover span {
        color: #ffffff !important;
    }

    .st-key-language_switch button {
        background: linear-gradient(135deg, #ffb703 0%, #fb8500 100%);
        color: #111111;
        border: 1px solid #ffd166;
        font-weight: 800;
    }

    .st-key-language_switch button:hover {
        background: linear-gradient(135deg, #ffd166 0%, #ffb703 100%);
        color: #111111;
        border-color: #ffe08a;
    }

    .contact-intro,
    div[data-testid="stForm"] label,
    div[data-testid="stForm"] label p,
    div[data-testid="stForm"] label span {
        color: #ffffff !important;
        opacity: 1 !important;
    }

    div[data-testid="stFormSubmitButton"] button {
        background: linear-gradient(135deg, #2dd4bf 0%, #0ea5e9 100%);
        color: #081018;
        border: 1px solid #67e8f9;
        font-weight: 800;
    }

    div[data-testid="stFormSubmitButton"] button:hover {
        background: linear-gradient(135deg, #5eead4 0%, #38bdf8 100%);
        color: #081018;
        border-color: #a5f3fc;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------

header_left, header_right = st.columns([5, 1])

with header_left:
    st.markdown(
        '<div class="opria-logo">OPRIA</div>',
        unsafe_allow_html=True,
    )

with header_right:
    language_label = "🇪🇸 ES" if st.session_state.language == "en" else "🇬🇧 EN"

    if st.button(language_label, key="language_switch", type="primary", width="stretch"):
        switch_language()
        st.rerun()


# ---------------------------------------------------------
# HERO
# ---------------------------------------------------------

st.markdown(
    f"""
    <div class="hero-title">
        {t("hero_title")}
    </div>

    <div class="hero-subtitle">
        {t("hero_subtitle")}
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")

if st.button(
    t("hero_button"),
    type="primary",
    use_container_width=False,
):
    st.session_state["show_framework"] = True


# ---------------------------------------------------------
# PROBLEM
# ---------------------------------------------------------

with st.expander(t("problem_title"), expanded=False):
    for item in CONTENT["problem"]:
        with st.expander(item[st.session_state.language], expanded=False):
            key = item["key"]
            st.write(CONTENT["problem_detail"][key][st.session_state.language])


# ---------------------------------------------------------
# FRAMEWORK
# ---------------------------------------------------------

with st.expander(t("framework_title"), expanded=False):
    st.write(t("framework_intro"))

    for index, item in enumerate(CONTENT["framework"], start=1):

        with st.expander(
            f"{index:02d}  {item['name'][st.session_state.language]}",
            expanded=False,
        ):
            st.markdown(
                f"""
                <div class="framework-number">
                    {index:02d}
                </div>

                <div class="framework-name">
                    {item['name'][st.session_state.language]}
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.write(
                item["description"][st.session_state.language]
            )

            bullets = item["bullets"][st.session_state.language]

            for bullet in bullets:
                st.markdown(f"- {bullet}")


# ---------------------------------------------------------
# WHAT CHANGES
# ---------------------------------------------------------

with st.expander(t("changes_title"), expanded=False):
    for item in CONTENT["changes"]:
        with st.expander(item["title"][st.session_state.language], expanded=False):
            st.write(
                item["description"][st.session_state.language]
            )


# ---------------------------------------------------------
# OPRIA OS
# ---------------------------------------------------------

with st.expander(t("os_title"), expanded=False):
    with st.expander(t("os_what"), expanded=False):
        st.write(t("os_what_answer"))

    with st.expander(t("os_technology"), expanded=False):
        st.write(t("os_technology_answer"))

    with st.expander(t("os_existing"), expanded=False):
        st.write(t("os_existing_answer"))


# ---------------------------------------------------------
# BUSINESS CHECK
# ---------------------------------------------------------

with st.expander(t("check_title"), expanded=False):
    st.write(t("check_intro"))

    questions = CONTENT["business_check"]

    answers = []

    group_size = 4

    for group_start in range(0, len(questions), group_size):
        group = questions[group_start : group_start + group_size]
        group_end = group_start + len(group)

        with st.expander(
            f"Bloque de preguntas {group_start + 1:02d}-{group_end:02d}",
            expanded=False,
        ):
            for index, question in enumerate(group, start=group_start):

                with st.expander(
                    f"{index + 1:02d}  {question['question'][st.session_state.language]}",
                    expanded=False,
                ):

                    answer = st.radio(
                        "",
                        question["options"][st.session_state.language],
                        key=f"check_{index}",
                    )

                    answers.append(answer)


    st.write("")

    if st.button(
        t("check_button"),
        type="primary",
        width="stretch",
    ):

        score = 0

        for index, answer in enumerate(answers):
            options = questions[index]["options"][st.session_state.language]

            if answer == options[0]:
                score += 2
            elif answer == options[1]:
                score += 1

        st.session_state["check_score"] = score
        st.session_state["check_answers"] = answers


    if "check_score" in st.session_state:

        score = st.session_state["check_score"]

        st.success(
            f"{t('check_result')} {score}/20"
        )

        with st.expander(t("check_interpretation")):

            if score >= 15:
                st.write(t("check_high"))
            elif score >= 8:
                st.write(t("check_medium"))
            else:
                st.write(t("check_low"))


# ---------------------------------------------------------
# CONTACT
# ---------------------------------------------------------

with st.expander(t("contact_title"), expanded=False):
    st.markdown(
        f'<div class="contact-intro">{t("contact_intro")}</div>',
        unsafe_allow_html=True,
    )
    st.caption(t("contact_privacy"))

    with st.form("contact_form"):

        name = st.text_input(t("name"))
        company = st.text_input(t("company"))
        email = st.text_input(t("email"))
        message = st.text_area(t("message"))

        submitted = st.form_submit_button(
            t("contact_button"),
            type="primary",
            use_container_width=True,
        )

        if submitted:

            if not name or not email:

                st.error(t("contact_required"))

            else:

                save_contact(
                    name=name,
                    company=company,
                    email=email,
                    message=message,
                    language=st.session_state.language,
                    source="landing",
                )

                st.success(t("contact_success"))
                st.link_button(
                    t("contact_whatsapp"),
                    build_whatsapp_url(name, company, email, message),
                    use_container_width=True,
                )


# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.markdown(
    f"""
    <div class="footer">
        OPRIA — Business Growth & Management System<br>
        {t("footer")}
    </div>
    """,
    unsafe_allow_html=True,
)