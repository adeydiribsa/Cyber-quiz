import streamlit as st
from PIL import Image
from collections import Counter
import os
import requests
import datetime
import csv
import json

st.set_page_config(page_title='VisionFund Cyber Persona Quiz', page_icon=':shield:', layout='centered')

primary_color = '#FF6600'

# ---- Responsive CSS ----
st.markdown(f"""
<style>
.stApp {{background-color: white;}}
.title {{
    color: {primary_color};
    font-size:36px;
    font-weight:600;
    word-wrap: break-word;
    text-align: left;
}}
.persona {{
    background-color:#FFF5E6;
    padding:20px;
    border-radius:12px;
    font-size:16px;
    word-wrap: break-word;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    margin-bottom: 20px;
}}
.tip-card {{
    background-color:#FFF8F0;
    border-left: 4px solid {primary_color};
    padding:12px;
    margin-bottom:8px;
    border-radius:8px;
    font-size:14px;
}}
.footer {{
    color: {primary_color};
    font-size:12px;
    text-align:center;
    margin-top:20px;
}}

@media only screen and (max-width: 600px) {{
    .title {{font-size:24px; text-align:center;}}
    .persona {{font-size:14px; padding:15px;}}
    .tip-card {{font-size:13px; padding:10px;}}
}}
</style>
""", unsafe_allow_html=True)

# ---- Header ----
try:
    logo = Image.open('logo.jpg')
except Exception:
    logo = None

# Use new API
screen_width = st.query_params.get("screen_width", [0])[0]

# Simple mobile stack (or desktop columns)
if logo:
    if int(screen_width) < 600:
        st.image(logo, width=100)
        st.markdown('<div class="title">YOU Make the Difference in Cybersecurity</div>', unsafe_allow_html=True)
    else:
        col1, col2 = st.columns([1,3])
        with col1:
            st.image(logo, width=120)
        with col2:
            st.markdown('<div class="title">YOU Make the Difference in Cybersecurity</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="title">YOU Make the Difference in Cybersecurity</div>', unsafe_allow_html=True)

st.markdown('### VisionFund MFI — Cyber Persona Quiz')
st.write('---')

# ---- Quiz Questions ----
questions = [
    ('You get a Teams call from "IT Support" telling you your account is compromised and you must log in right now using the link they send. You…', 
     ['A) Ask questions and dig deeper before acting', 
      'B) Calmly follow procedure and notify the right people', 
      'C) Try to trick the scammer into revealing their intent', 
      'D) Immediately disconnect, block, and move on']),
    ("A 'supplier' emails you about an urgent unpaid invoice with a link to pay immediately. You…",
     ['A) Double-check payment records before acting', 
      'B) Alert your team right away', 
      'C) Investigate the email’s metadata', 
      'D) Delete it instantly and block the sender']),
    ("A text message claims to be from your bank with a fraud alert and a link to 'verify your account.' You…",
     ['A) Call the bank directly using the number on your card', 
      'B) Take a screenshot and report it', 
      'C) Search online for the scam wording', 
      'D) Delete and block instantly']),
    ("It’s April, six months after Cybersecurity Awareness Month, and you see an email that feels suspicious. You…",
     ['A) Investigate thoroughly before acting', 
      'B) Share a warning with your team', 
      'C) Archive it and track similar attempts', 
      'D) Delete it and move on'])
]

# ---- Google Apps Script Webhook URL ----
WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbz5PkadsuYGR5WxobVnQ8OiOZYFZhFbpadX46wJrULQy-YrzTGuQlJXKhPztXZBgy_S/exec"

# ---- Quiz Form ----
with st.form('quiz_form'):
    st.write('### Quiz Questions')
    user_name = st.text_input('Your name (optional)')
    dept = st.text_input('Department (optional)')
    answers = []
    for i, (q, opts) in enumerate(questions, start=1):
        ans = st.radio(f'Q{i}. {q}', options=opts, key=f'q{i}')
        answers.append(ans[0])
    submitted = st.form_submit_button('Submit')

# ---- Submission Logic ----
if submitted:
    counts = Counter(answers)
    order = ['A','B','C','D']
    most_common = sorted(order, key=lambda x: (-counts[x], order.index(x)))[0]

    persona_map = {
        'A': ('The Detective 🕵️', 'You question and verify before acting. Strong investigator and cautious by nature.'),
        'B': ('The Guardian 🛡', 'You protect others by reporting and coordinating. Team-focused and dependable.'),
        'C': ('The Strategist ♟', 'You think like an attacker to anticipate threats. Analytical and proactive.'),
        'D': ('The Scout 🚀', 'You act quickly to neutralize threats. Fast responder who values immediate action.')
    }

    persona_title, persona_desc = persona_map[most_common]

    # ---- Display Persona ----
    st.success(f"Hi {user_name or 'Participant'} — your primary Cyber Persona is:")
    st.markdown(f"<div class='persona'><strong>{persona_title}</strong><br/>{persona_desc}</div>", unsafe_allow_html=True)

    # ---- Practical Tips ----
    tips = {
        'A': ['Keep verifying sources and encourage others to question suspicious requests.', 
              'Share tips on investigating messages.'],
        'B': ['Keep reporting and be a role model for your team.', 
              'Help colleagues know how to escalate suspicious items.'],
        'C': ['Use your analytical skills to improve team defenses.', 
              'Share patterns you observe in phishing attempts.'],
        'D': ['Balance quick action with verification to avoid accidental disruption.', 
              'Document incidents to help the team learn.']
    }
    st.write('**Practical tips:**')
    for t in tips[most_common]:
        st.markdown(f"<div class='tip-card'>{t}</div>", unsafe_allow_html=True)

    # ---- Prepare payload for Google Sheet ----
    payload = {
        "name": user_name,
        "department": dept,
        "q1": answers[0],
        "q2": answers[1],
        "q3": answers[2],
        "q4": answers[3],
        "persona": persona_title
    }

    # ---- Attempt Google Sheet submission ----
    success = False
    try:
        response = requests.post(WEBHOOK_URL, json=payload, timeout=5)
        if response.status_code == 200:
            st.success("✅ Your response has been recorded successfully in VisionFund’s secure Google Sheet.")
            success = True
        else:
            st.warning("⚠️ Could not reach Google Sheet. Saving locally.")
    except Exception:
        st.warning("⚠️ Could not connect to Google Sheet. Saving your response locally.")

    # ---- Fallback: save to local CSV ----
    if not success:
        save_path = 'responses.csv'
        header = ['timestamp','name','department','q1','q2','q3','q4','persona']
        row = [datetime.datetime.utcnow().isoformat(), user_name, dept] + answers + [persona_title]
        write_header = not os.path.exists(save_path)
        with open(save_path, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if write_header:
                writer.writerow(header)
            writer.writerow(row)
        st.info("💾 Your response has been saved locally as a fallback.")

    # ---- Admin download ----
    if st.checkbox('Show admin options'):
        st.markdown('**Admin: Download all responses**')
        try:
            with open('responses.csv','r',encoding='utf-8') as f:
                st.download_button('Download CSV', data=f.read(), file_name='responses.csv', mime='text/csv')
        except Exception:
            st.error('No local responses yet.')

# ---- Footer ----
st.markdown('<div class="footer">VisionFund MFI — YOU Make the Difference in Cybersecurity</div>', unsafe_allow_html=True)
