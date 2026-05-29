import streamlit as st
import json
import time
from utils.llm_client import LLMClient
from utils.prompt_builder import build_prompt

st.set_page_config(
    page_title="IRIS AI",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="collapsed"
)


EXAMPLES = {
    "KeyError":
"""Traceback (most recent call last):
  File "app.py", line 5, in <module>
    print(user['email'])
KeyError: 'email'""",

    "TypeError":
"""Traceback (most recent call last):
  File "calc.py", line 3, in <module>
    result = "Total: " + 42
TypeError: can only concatenate str (not "int") to str""",

    "NameError":
"""Traceback (most recent call last):
  File "script.py", line 7, in <module>
    send_email(mesage)
NameError: name 'mesage' is not defined""",

    "IndexError":
"""Traceback (most recent call last):
  File "main.py", line 4, in <module>
    print(items[5])
IndexError: list index out of range""",

    "AttributeError":
"""Traceback (most recent call last):
  File "process.py", line 9, in <module>
    data.sort()
AttributeError: 'NoneType' object has no attribute 'sort'"""
}


if "input_text" not in st.session_state:
    st.session_state.input_text = ""



st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

:root{
    --bg:#050816;
    --card:#0B1023;
    --glass:rgba(255,255,255,0.04);
    --border:rgba(255,255,255,0.08);
    --primary:#00E0B8;
    --secondary:#00B8FF;
    --text:#E8ECFF;
    --muted:#9AA4C7;
}

html, body, [class*="css"]{
    font-family:'Space Grotesk', sans-serif;
    background:var(--bg);
    color:white;
}

.stApp{
    background:
    radial-gradient(circle at top,
    rgba(0,224,184,0.12),
    transparent 30%),
    radial-gradient(circle at bottom right,
    rgba(0,184,255,0.10),
    transparent 25%),
    var(--bg);
}

#MainMenu,
footer,
header{
    visibility:hidden;
}

.block-container{
    padding-top:1rem;
    max-width:1200px;
}

/* HERO */

.hero{
    text-align:center;
    padding-top:3rem;
    padding-bottom:2rem;
}

.hero-badge{
    display:inline-block;
    padding:10px 22px;
    border-radius:999px;
    background:rgba(0,224,184,0.08);
    border:1px solid rgba(0,224,184,0.15);
    color:var(--primary);
    font-size:11px;
    letter-spacing:0.18em;
    text-transform:uppercase;
    margin-bottom:2rem;
    backdrop-filter:blur(12px);
}

.hero h1{
    font-size:5rem;
    line-height:0.95;
    font-weight:700;
    letter-spacing:-4px;
    margin-bottom:1.5rem;
    color:white;
}

.hero span{
    background:linear-gradient(
        135deg,
        var(--primary),
        var(--secondary)
    );
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
}

.hero p{
    color:var(--muted);
    max-width:760px;
    margin:auto;
    font-size:1.12rem;
    line-height:1.9;
}

/* GLASS CARD */

.glass-card{
    background:rgba(255,255,255,0.03);
    border:1px solid rgba(255,255,255,0.07);
    border-radius:30px;
    padding:2rem;
    backdrop-filter:blur(18px);
    box-shadow:
    0 0 0 1px rgba(255,255,255,0.02),
    0 20px 80px rgba(0,0,0,0.45);
}

/* LABELS */

.label{
    color:var(--primary);
    font-size:11px;
    font-weight:700;
    letter-spacing:0.20em;
    text-transform:uppercase;
    margin-bottom:1rem;
}

/* TEXTAREA */

.stTextArea textarea{
    background:#0B1023 !important;
    border:1px solid rgba(255,255,255,0.08) !important;
    border-radius:22px !important;
    color:#F2F5FF !important;
    font-family:'JetBrains Mono', monospace !important;
    font-size:14px !important;
    line-height:1.7 !important;
    padding:1.2rem !important;
    transition:0.25s ease !important;
}

.stTextArea textarea:focus{
    border:1px solid rgba(0,224,184,0.35) !important;
    box-shadow:0 0 0 4px rgba(0,224,184,0.08);
}

/* BUTTONS */

.stButton > button{
    width:100%;
    border:none;
    border-radius:16px;
    transition:0.25s ease;
    font-weight:600;
}

/* QUICK EXAMPLE BUTTONS */

.example-btn button{
    background:rgba(255,255,255,0.04) !important;
    border:1px solid rgba(255,255,255,0.06) !important;
    color:white !important;
    height:54px;
    backdrop-filter:blur(10px);
}

.example-btn button:hover{
    border:1px solid rgba(0,224,184,0.5) !important;
    color:var(--primary) !important;
    transform:translateY(-2px);
    box-shadow:0 10px 25px rgba(0,224,184,0.12);
}

/* ANALYZE BUTTON */

.analyze-btn button{
    background:linear-gradient(
        135deg,
        var(--primary),
        var(--secondary)
    ) !important;

    color:black !important;
    height:64px;
    margin-top:1rem;
    font-size:15px;
    font-weight:700;
    letter-spacing:0.12em;
}

.analyze-btn button:hover{
    transform:translateY(-3px);
    box-shadow:0 0 40px rgba(0,224,184,0.30);
}

/* RESULT CARDS */

.result-card{
    background:rgba(255,255,255,0.03);
    border:1px solid rgba(255,255,255,0.08);
    border-radius:26px;
    padding:1.6rem;
    backdrop-filter:blur(12px);
    height:100%;
}

.result-title{
    color:var(--primary);
    font-size:11px;
    font-weight:700;
    letter-spacing:0.18em;
    text-transform:uppercase;
    margin-bottom:1rem;
}

.result-text{
    color:#DDE5FF;
    line-height:1.9;
    font-size:15px;
}

/* CODE BLOCK */

[data-testid="stCodeBlock"]{
    border-radius:22px;
    overflow:hidden;
    border:1px solid rgba(255,255,255,0.08);
}

/* SCROLLBAR */

::-webkit-scrollbar{
    width:8px;
}

::-webkit-scrollbar-thumb{
    background:rgba(255,255,255,0.12);
    border-radius:10px;
}

/* MOBILE */

@media(max-width:768px){

.hero h1{
    font-size:3rem;
    letter-spacing:-2px;
}

.hero p{
    font-size:1rem;
}

}

</style>
""", unsafe_allow_html=True)


st.markdown("""
<div class="hero">

<div class="hero-badge">
AI-powered Python debugging
</div>

<h1>
Debug Python errors<br>
<span>in seconds.</span>
</h1>

<p>
Paste any Python traceback and instantly get the meaning,
root causes, recommended fixes, and corrected code examples.
</p>

</div>
""", unsafe_allow_html=True)


st.markdown('<div class="glass-card">', unsafe_allow_html=True)


st.markdown(
    '<div class="label">Quick Examples</div>',
    unsafe_allow_html=True
)

cols = st.columns(5)

for i, key in enumerate(EXAMPLES.keys()):

    with cols[i]:

        st.markdown(
            '<div class="example-btn">',
            unsafe_allow_html=True
        )

        if st.button(key, key=key):
            st.session_state.input_text = EXAMPLES[key]

        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )

st.markdown("<br>", unsafe_allow_html=True)


st.markdown(
    '<div class="label">Python Traceback</div>',
    unsafe_allow_html=True
)

error_input = st.text_area(
    "traceback",
    value=st.session_state.input_text,
    height=240,
    placeholder="Paste your Python traceback here...",
    label_visibility="collapsed"
)


st.markdown(
    '<div class="analyze-btn">',
    unsafe_allow_html=True
)

analyze = st.button("⬡ ANALYZE ERROR")

st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)


if analyze:

    if not error_input.strip():

        st.warning("Please paste a traceback.")

    else:

        llm = LLMClient()

        with st.spinner("Analyzing traceback..."):

            start = time.time()

            prompt = build_prompt(error_input)

            response = llm.get_response(prompt)

            end = time.time()

        try:

            if isinstance(response, str):
                data = json.loads(response)
            else:
                data = response

            st.markdown("<br><br>", unsafe_allow_html=True)

            col1, col2 = st.columns(2)

            with col1:

                st.markdown(f"""
                <div class="result-card">
                    <div class="result-title">Meaning</div>
                    <div class="result-text">
                        {data.get("meaning", "")}
                    </div>
                </div>
                """, unsafe_allow_html=True)

                causes_html = ""

                for c in data.get("causes", []):

                    causes_html += f"""
                    <div style="margin-bottom:14px;">
                        • {c}
                    </div>
                    """

                st.markdown(f"""
                <div class="result-card" style="margin-top:1rem;">
                    <div class="result-title">Root Causes</div>
                    <div class="result-text">
                        {causes_html}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with col2:

                st.markdown(f"""
                <div class="result-card">
                    <div class="result-title">Recommended Fix</div>
                    <div class="result-text">
                        {data.get("fix", "")}
                    </div>
                </div>
                """, unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)

                st.code(
                    data.get("example", ""),
                    language="python"
                )

            st.markdown("<br>", unsafe_allow_html=True)

            st.caption(
                f"⚡ Response generated in {round(end-start,2)}s • Powered by Groq LPU"
            )

        except Exception:

            st.error("Failed to parse response.")
            st.write(response)