import streamlit as st
from PIL import Image
from collections import Counter
import os
import requests
import datetime
import csv

st.set_page_config(page_title='VisionFund Cyber Leadership Quiz', page_icon=':shield:', layout='centered')

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

screen_width = st.query_params.get("screen_width", [0])[0]

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

st.markdown('### VisionFund MFI — Senior Management Cyber Leadership Quiz')

# ---- Introduction ----
st.write('---')
st.markdown("""
### 🧭 Discover Your Cyber Leadership Style

Cybersecurity is not just an IT concern — it’s a leadership responsibility.  
This quick reflection helps you see **how your decision-making style** supports a strong culture of security and trust.  

There are no right or wrong answers — each style brings value to how VisionFund protects its people and data.  
Answer honestly, and see which **Cyber Leadership Persona** best reflects you.
""")
st.write('---')

# ---- Quiz Questions (Non-Technical Leadership-Focused) ----
questions = [
    ("You receive news that one of your branches is facing a potential security issue affecting customer data. What’s your first action as a leader?",
     ['A) Ask questions to understand the full situation before responding',
      'B) Bring together the right teams to handle communication and response',
      'C) Think through the possible causes and long-term lessons',
      'D) Make a quick decision to contain the issue and reassure others']),
    
    ("An unfamiliar organization emails you asking for partnership details and financial information. You…",
     ['A) Verify the source and confirm if it’s legitimate before replying',
      'B) Notify your communications or compliance team for review',
      'C) Reflect on how similar requests have been handled in the past',
      'D) Choose not to respond and move on quickly']),
    
    ("A staff member reports receiving a suspicious email claiming to be from your office. How do you handle it?",
     ['A) Ask for more details to understand what happened',
      'B) Appreciate the report and encourage others to do the same',
      'C) Think about what this incident says about awareness in the team',
      'D) Tell them to delete it immediately and stay alert']),
    
    ("You’re preparing for a management meeting on cybersecurity awareness. Your approach is to…",
     ['A) Review real examples to ask thoughtful questions',
      'B) Encourage open discussion and teamwork on the topic',
      'C) Focus on what can be improved in current practices',
      'D) Keep it brief and practical with clear next steps'])
]

# ---- Google Apps Script Webhook URL ----
WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbzTZmYJbaGx4oYEo4eXOK5_2IFZMHdd8zE8B9Qbajqc9ibv1b7-7Lr0X1RJkbp7QbYs/exec"

# ---- Quiz Form ----
with st.form('quiz_form'):
    st.write('### Leadership Reflection')
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

    # ---- Persona Map (Leadership-Focused) ----
    persona_map = {
        'A': ('The Thoughtful Leader 🕵️', 
              'You take time to understand before acting. Calm, analytical, and trusted for your balanced judgment.'),
        'B': ('The Collaborator 🛡', 
              'You believe in teamwork and open communication. You build confidence by keeping everyone informed and involved.'),
        'C': ('The Visionary ♟', 
              'You focus on lessons and long-term improvement. You see patterns others miss and guide the organization toward growth.'),
        'D': ('The Decisive Driver 🚀', 
              'You act quickly and confidently in moments of uncertainty. You inspire others through clear direction and momentum.')
    }

    persona_title, persona_desc = persona_map[most_common]

    # ---- Display Persona ----
    st.success(f"Hi {user_name or 'Leader'} — your Cyber Leadership Persona is:")
    st.markdown(f"<div class='persona'><strong>{persona_title}</strong><br/>{persona_desc}</div>", unsafe_allow_html=True)

    # ---- Practical Tips for Leaders ----
    tips = {
        'A': [
            'Continue asking thoughtful questions before taking action — your calm approach builds confidence during pressure.',
            'Balance careful thinking with timely decisions to keep momentum when it matters most.'
        ],
        'B': [
            'Keep encouraging your teams to share information — it builds a culture of transparency and trust.',
            'Recognize and reward people who report issues early; that openness strengthens the whole organization.'
        ],
        'C': [
            'Share insights from past challenges to help others see the bigger picture.',
            'Encourage proactive learning — your forward-thinking mindset shapes better decisions at every level.'
        ],
        'D': [
            'Your decisiveness is a strength — pair it with reflection afterward to capture key lessons.',
            'Model clear communication when making fast calls so others stay aligned and confident.'
        ]
    }

    st.write('**Practical tips for leaders like you:**')
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
