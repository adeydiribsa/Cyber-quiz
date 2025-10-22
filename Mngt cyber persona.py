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

st.markdown('### VisionFund MFI — Senior Management Cybersecurity Awareness Quiz')

# ---- Introduction ----
st.write('---')
st.markdown("""
### 🧭 Discover Your Cyber Leadership Style
  
This short reflection helps you see **how your leadership style** supports a strong culture of security awareness and trust.  

There are no right or wrong answers — each style contributes to VisionFund’s resilience and protection of people and data.  
Answer honestly and discover your **Cyber Leadership Persona**.
""")
st.write('---')

# ---- Quiz Questions ----
questions = [
    ("You are informed that the organization may face a cyber-related disruption affecting operations or customers. What is your first step as a senior leader?",
     ['A) Assess the situation carefully, gather facts from relevant teams, and consider potential impacts before acting',
      'B) Call an immediate leadership meeting to align on response strategy and communication plans',
      'C) Review organizational policies and risk management frameworks to guide next steps',
      'D) Make quick decisions to contain potential disruption while monitoring updates']),
    
    ("A key vendor or partner reports a potential risk affecting their services or data management. As a senior leader, how do you respond?",
     ['A) Request an overview of the situation and validate the information before making decisions',
      'B) Escalate immediately to relevant management teams to coordinate response and communication',
      'C) Evaluate potential impact on operations, reputation, and compliance before taking action',
      'D) Temporarily adjust business processes or service dependencies while awaiting confirmation']),
    
    ("A staff member reports receiving a suspicious email claiming to be from your office. How do you handle it?",
     ['A) Ask for more details to understand what happened',
      'B) Appreciate the report and encourage others to do the same',
      'C) Think about what this incident says about team awareness',
      'D) Tell them to delete it immediately and stay alert']),
    
    ("You’re preparing for a management meeting on cybersecurity awareness. Your approach is to…",
     ['A) Review real examples to ask thoughtful questions',
      'B) Encourage open discussion and teamwork on the topic',
      'C) Focus on improving current practices',
      'D) Keep it brief and practical with clear next steps'])
]

# ---- Google Apps Script Webhook URL ----
WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbwpnBWfB3bhVwvNyhRqxqV9TCnesQDuurVtLLQfk42Bkcd4zIYxByGDP8TcFVzLYJtw/exec"

# ---- Quiz Form ----
with st.form('quiz_form'):
    st.write('### Leadership Reflection')
    user_name = st.text_input('Your name (optional)')
    dept = st.text_input('Department (optional)')
    answers = []

    # Titles for each question
    question_titles = [
        "Q1: Cyber Risk Oversight",
        "Q2: Vendor / Third-Party Risk",
        "Q3: Staff Report Handling",
        "Q4: Cyber Awareness Meeting"
    ]

    for i, (q, opts) in enumerate(questions, start=0):
        # Bold only the question title
        st.markdown(f"**{question_titles[i]}**: {q}", unsafe_allow_html=True)
        ans = st.radio("", options=opts, key=f'q{i+1}', index=0, horizontal=False)
        answers.append(ans)
        # Add spacing after each question
        st.markdown("<br>", unsafe_allow_html=True)

    submitted = st.form_submit_button('Submit')




# ---- Submission Logic ----
if submitted:
    counts = Counter(answers)
    order = ['A','B','C','D']
    most_common = sorted(order, key=lambda x: (-counts[x], order.index(x)))[0]

    # ---- Persona Map (Cybersecurity Awareness) ----
    persona_map = {
        'A': ('The Insightful Leader 🕵️', 
              'You carefully assess cybersecurity risks before acting. Your thoughtful approach ensures decisions protect people, data, and operations.'),
        'B': ('The Connector 🛡', 
              'You foster collaboration and communication around cyber risks. Your team trusts you to coordinate awareness and encourage reporting of suspicious activities.'),
        'C': ('The Strategist ♟', 
              'You focus on long-term cyber resilience. You anticipate potential threats and guide the organization to strengthen policies and awareness initiatives.'),
        'D': ('The Action-Oriented Driver 🚀', 
              'You act quickly to address potential cyber threats. Your decisiveness helps contain risks and reinforces a culture of immediate reporting and proactive action.')
    }

    persona_title, persona_desc = persona_map[most_common]

    # ---- Display Persona ----
    st.success(f"Hi {user_name or 'Leader'} — your Cyber Leadership Persona is:")
    st.markdown(f"<div class='persona'><strong>{persona_title}</strong><br/>{persona_desc}</div>", unsafe_allow_html=True)

    # ---- Practical Tips (Cybersecurity Awareness) ----
    tips = {
        'A': [
            'Before reacting to cyber incidents, assess the situation carefully and verify information — this reduces risk of missteps.',
            'Encourage your team to question suspicious requests or emails; model cautious decision-making.'
        ],
        'B': [
            'Promote open communication about cyber risks — create a safe space for reporting suspicious activities.',
            'Recognize and reinforce team members who follow security best practices; this fosters a culture of accountability.'
        ],
        'C': [
            'Share insights on past incidents to educate the team and improve awareness.',
            'Support proactive cybersecurity training and policies; help the organization anticipate future threats.'
        ],
        'D': [
            'Respond promptly to potential threats while communicating clearly with the team to maintain trust.',
            'After urgent actions, review outcomes to capture key lessons for continuous improvement.'
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
