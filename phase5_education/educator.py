"""
EarthMender AI — Phase 5: Education Module (Flashcard Redesign)
================================================================
Dark themed, card-based UI:
  1. Waste Sorting Guide — swipeable category cards
  2. Recycling Tips      — material flashcards with icon + did-you-know
  3. Quiz                — full-screen flashcard quiz with flip animation feel
"""

import streamlit as st
import random
from phase5_education.quiz_data import QUIZ_QUESTIONS

# ── EDUCATION CSS ─────────────────────────────────────────────────────────────
EDUCATION_CSS = """
<style>
.edu-page { background:#0a1410; padding:0 16px 20px; }

/* Category cards */
.edu-cat-card {
  border-radius:16px; padding:20px 18px; margin-bottom:12px;
  border:0.5px solid rgba(255,255,255,0.08); position:relative; overflow:hidden;
}
.edu-cat-header { display:flex; align-items:center; gap:12px; margin-bottom:14px; }
.edu-cat-icon {
  width:48px; height:48px; border-radius:14px;
  display:flex; align-items:center; justify-content:center; font-size:24px; flex-shrink:0;
}
.edu-cat-title { font-size:15px; font-weight:700; color:#eee; font-family:'Inter',sans-serif; }
.edu-cat-sub   { font-size:11px; color:#777; margin-top:2px; font-family:'Inter',sans-serif; }
.edu-item-list { list-style:none; padding:0; margin:0; }
.edu-item-list li {
  font-size:12px; color:#aaa; padding:6px 0;
  border-bottom:0.5px solid rgba(255,255,255,0.05);
  font-family:'Inter',sans-serif; display:flex; align-items:flex-start; gap:8px;
}
.edu-item-list li:last-child { border-bottom:none; }
.edu-item-dot { width:5px; height:5px; border-radius:50%; margin-top:6px; flex-shrink:0; }
.edu-where {
  background:rgba(255,255,255,0.06); border-radius:10px;
  padding:10px 12px; margin-top:12px; font-size:11px; color:#888;
  font-family:'Inter',sans-serif;
}
.edu-where-label { font-size:10px; color:#555; margin-bottom:4px; font-weight:600; }
.edu-tip {
  background:rgba(255,193,7,0.08); border-radius:10px;
  padding:10px 12px; margin-top:8px; font-size:11px; color:#ffd54f;
  border:0.5px solid rgba(255,193,7,0.15); font-family:'Inter',sans-serif;
}

/* Recycling tip flashcards */
.tip-card {
  border-radius:18px; padding:22px 20px; margin-bottom:14px;
  border:0.5px solid rgba(255,255,255,0.07);
  position:relative; overflow:hidden;
}
.tip-card-header {
  display:flex; align-items:center; justify-content:space-between; margin-bottom:16px;
}
.tip-card-title { font-size:16px; font-weight:700; color:#eee; font-family:'Inter',sans-serif; }
.tip-card-num {
  font-size:11px; color:#555; font-family:'Inter',sans-serif;
  background:rgba(255,255,255,0.06); padding:4px 10px; border-radius:20px;
}
.tip-item {
  display:flex; align-items:flex-start; gap:10px;
  padding:8px 0; border-bottom:0.5px solid rgba(255,255,255,0.05);
  font-family:'Inter',sans-serif;
}
.tip-item:last-of-type { border-bottom:none; }
.tip-check {
  width:20px; height:20px; border-radius:50%; flex-shrink:0;
  display:flex; align-items:center; justify-content:center; margin-top:1px;
}
.tip-text { font-size:12px; color:#ccc; line-height:1.6; }
.tip-fact {
  border-radius:12px; padding:12px 14px; margin-top:14px;
  border:0.5px solid rgba(255,255,255,0.06);
}
.tip-fact-label { font-size:10px; font-weight:700; margin-bottom:4px; }
.tip-fact-text  { font-size:12px; color:#ccc; font-family:'Inter',sans-serif; line-height:1.5; }

/* Quiz flashcard */
.quiz-splash {
  border-radius:20px; padding:36px 24px; text-align:center;
  background:#1a2e20; border:0.5px solid rgba(255,255,255,0.08);
  margin:8px 0 16px;
}
.quiz-splash-icon { font-size:52px; margin-bottom:12px; }
.quiz-splash-title { font-size:22px; font-weight:800; color:#eee; font-family:'Inter',sans-serif; margin-bottom:8px; }
.quiz-splash-sub   { font-size:13px; color:#666; font-family:'Inter',sans-serif; margin-bottom:4px; }

.quiz-card {
  border-radius:20px; padding:28px 22px; margin:8px 0 16px;
  background:#1a2e20; border:0.5px solid rgba(255,255,255,0.08);
  min-height:180px;
}
.quiz-card-num {
  font-size:11px; color:#4caf50; font-weight:700;
  font-family:'Inter',sans-serif; margin-bottom:16px;
  display:flex; align-items:center; justify-content:space-between;
}
.quiz-question {
  font-size:17px; font-weight:600; color:#eee;
  font-family:'Inter',sans-serif; line-height:1.6;
}

.quiz-feedback-correct {
  border-radius:16px; padding:18px 20px;
  background:rgba(76,175,80,0.12); border:1px solid rgba(76,175,80,0.3);
  margin:8px 0 16px;
}
.quiz-feedback-wrong {
  border-radius:16px; padding:18px 20px;
  background:rgba(244,67,54,0.1); border:1px solid rgba(244,67,54,0.25);
  margin:8px 0 16px;
}
.quiz-fb-header { font-size:15px; font-weight:700; margin-bottom:8px; font-family:'Inter',sans-serif; }
.quiz-fb-explain { font-size:13px; color:#aaa; line-height:1.6; font-family:'Inter',sans-serif; }

.quiz-result {
  border-radius:20px; padding:36px 24px; text-align:center;
  margin:8px 0 16px; border:0.5px solid rgba(255,255,255,0.08);
}
.quiz-result-icon  { font-size:56px; margin-bottom:12px; }
.quiz-result-grade { font-size:24px; font-weight:800; font-family:'Inter',sans-serif; margin-bottom:4px; }
.quiz-result-score { font-size:16px; color:#aaa; font-family:'Inter',sans-serif; margin-bottom:12px; }
.quiz-result-msg   { font-size:13px; color:#666; font-family:'Inter',sans-serif; }

.progress-track {
  background:rgba(255,255,255,0.08); border-radius:4px; height:4px;
  margin:0 0 20px; overflow:hidden;
}
.progress-fill { height:4px; border-radius:4px; background:#4caf50; transition:width 0.3s; }
</style>
"""

# ── DATA ──────────────────────────────────────────────────────────────────────
SORTING_GUIDE = [
    {
        "title":   "♻️ Recyclable Waste",
        "color":   "#1a7a4a",
        "bg":      "rgba(26,122,74,0.12)",
        "icon_bg": "rgba(76,175,80,0.2)",
        "dot":     "#4caf50",
        "items": [
            "Plastic drink bottles — Eva, Pepsi, La Casera, Voltic",
            "Water sachets — individual and outer bundles (keep dry)",
            "Polythene bags — Shoprite, black bags, Milo/biscuit nylons",
            "Clean disposables — uncontaminated cups (rinse first)",
            "Cardboard and paper boxes (dry and flat)",
            "Glass bottles and jars (rinsed clean)",
            "Aluminium cans, tins, scrap metal",
        ],
        "where": "Wecyclers · RecyclePoints kiosks · Local scrap dealers",
        "tip":   "💡 Clean and dry is the rule — wet or contaminated items are rejected.",
    },
    {
        "title":   "🍃 Organic / Compostable",
        "color":   "#558b2f",
        "bg":      "rgba(85,139,47,0.1)",
        "icon_bg": "rgba(139,195,74,0.2)",
        "dot":     "#8bc34a",
        "items": [
            "Food scraps and plate leftovers",
            "Fruit and vegetable peels",
            "Eggshells and nutshells",
            "Garden leaves and grass clippings",
            "Used tea bags and coffee grounds",
        ],
        "where": "Home compost pit · Backyard composting · Organic waste bin",
        "tip":   "💡 Composting at home cuts your household waste by up to 30%.",
    },
    {
        "title":   "🗑️ General Waste",
        "color":   "#607d8b",
        "bg":      "rgba(96,125,139,0.1)",
        "icon_bg": "rgba(96,125,139,0.2)",
        "dot":     "#90a4ae",
        "items": [
            "Black polythene bags (optical sorters can't process them)",
            "Food-contaminated disposables and used cutlery",
            "Styrofoam / polystyrene (no facility accepts this yet)",
            "Soiled paper, tissue, and napkins",
            "Multi-layer packaging (crisp bags, juice boxes)",
        ],
        "where": "LAWMA bins (Lagos) · AEPB (Abuja) · PSP collector",
        "tip":   "💡 Keep bagged and sealed — loose waste blocks gutters and causes flooding.",
    },
    {
        "title":   "⚠️ Hazardous / E-Waste",
        "color":   "#c62828",
        "bg":      "rgba(198,40,40,0.1)",
        "icon_bg": "rgba(244,67,54,0.2)",
        "dot":     "#ef5350",
        "items": [
            "Old phones, batteries, laptops, chargers",
            "Broken bulbs and fluorescent tubes",
            "Paint cans and chemical containers",
            "Used engine oil jerry cans",
            "Medical waste, syringes, sharps",
        ],
        "where": "Hinckley Nigeria e-waste · Manufacturer take-back schemes",
        "tip":   "💡 NEVER dump in gutters — toxins leach into groundwater for decades.",
    },
]

RECYCLING_TIPS = [
    {
        "title": "🍶 Plastic Bottles",
        "sub":   "Eva, Pepsi, Voltic, La Casera...",
        "color": "#4caf50",
        "bg":    "rgba(76,175,80,0.08)",
        "fact_bg":"rgba(76,175,80,0.08)",
        "fact_color":"#a5d6a7",
        "tips": [
            "Rinse before recycling — food residue contaminates entire batches",
            "Remove the cap (different plastic) — recycle separately",
            "Crush flat to save storage space before your trip to a recycler",
            "#1 PET and #2 HDPE are the most accepted types in Nigeria",
            "RecyclePoints kiosks at filling stations pay cash per kg",
        ],
        "fact": "Recycling one PET bottle saves enough energy to power your phone for 25 minutes.",
    },
    {
        "title": "💧 Water Sachets",
        "sub":   "Pure water nylons",
        "color": "#2196f3",
        "bg":    "rgba(33,150,243,0.08)",
        "fact_bg":"rgba(33,150,243,0.08)",
        "fact_color":"#90caf9",
        "tips": [
            "Collect 20+ sachets before going — payment is per kg",
            "Keep dry and clean — wet sachets are rejected at facilities",
            "Cut open and shake out water before storing",
            "RecyclePoints pay cash or MTN/Airtel airtime per bag",
            "Set up a collection bag at home, school, or office",
        ],
        "fact": "Nigeria consumes an estimated 60 million water sachets every single day.",
    },
    {
        "title": "🛍️ Polythene Bags",
        "sub":   "All nylon types",
        "color": "#ff9800",
        "bg":    "rgba(255,152,0,0.08)",
        "fact_bg":"rgba(255,152,0,0.08)",
        "fact_color":"#ffcc80",
        "tips": [
            "ALL nylons go together — Shoprite, black, branded, bread nylons",
            "Never burn — the fumes are highly toxic and damage lungs",
            "Collect clean and dry — wet nylons are rejected",
            "Wecyclers runs kerbside pickup in Lagos — register free",
            "Black polythene is hardest to recycle — minimise purchase",
        ],
        "fact": "A single polythene bag takes up to 1,000 years to break down in a landfill.",
    },
    {
        "title": "🥤 Disposables",
        "sub":   "Cups, takeaway packs, cutlery",
        "color": "#9c27b0",
        "bg":    "rgba(156,39,176,0.08)",
        "fact_bg":"rgba(156,39,176,0.08)",
        "fact_color":"#ce93d8",
        "tips": [
            "Rinse cups and packs before disposal — food contaminates batches",
            "Uncontaminated disposables can go to your PSP/LAWMA collector",
            "Avoid single-use cutlery — carry a reusable spoon daily",
            "Styrofoam cannot be recycled in Nigeria — push vendors to switch",
            "Hard plastic cups (#5 PP) are more recyclable than styrofoam",
        ],
        "fact": "A styrofoam cup takes over 500 years to break down and leaches chemicals as it does.",
    },
    {
        "title": "🛢️ Waste Containers",
        "sub":   "Dustbins, drums, jerry cans",
        "color": "#795548",
        "bg":    "rgba(121,85,72,0.1)",
        "fact_bg":"rgba(121,85,72,0.1)",
        "fact_color":"#bcaaa4",
        "tips": [
            "Seal containers to prevent soil and groundwater contamination",
            "Report overflowing bins via EarthMender AI — operators are notified",
            "Never burn or bury containers that held chemicals or oil",
            "Metal jerry cans have scrap value — contact a local Ọlọbẹ dealer",
            "Plastic drums (#2 HDPE) can often be cleaned and reused",
        ],
        "fact": "One improperly disposed chemical drum can contaminate thousands of litres of groundwater.",
    },
]


# ── RENDER FUNCTIONS ──────────────────────────────────────────────────────────
def render_sorting_guide():
    st.markdown(EDUCATION_CSS, unsafe_allow_html=True)
    st.markdown('<div class="edu-page">', unsafe_allow_html=True)
    st.markdown("""
    <div style="padding:16px 0 8px;">
      <div style="font-size:15px;font-weight:700;color:#eee;font-family:'Inter',sans-serif;">
        🗂️ Waste Sorting Guide
      </div>
      <div style="font-size:12px;color:#666;margin-top:4px;font-family:'Inter',sans-serif;">
        Know exactly where your waste belongs — Nigerian context throughout
      </div>
    </div>
    """, unsafe_allow_html=True)

    for cat in SORTING_GUIDE:
        items_html = "".join(
            f'<li><span class="edu-item-dot" style="background:{cat["dot"]};"></span>'
            f'{item}</li>'
            for item in cat["items"]
        )
        st.markdown(f"""
        <div class="edu-cat-card" style="background:{cat['bg']};">
          <div class="edu-cat-header">
            <div class="edu-cat-icon" style="background:{cat['icon_bg']};">
              {cat['title'].split()[0]}
            </div>
            <div>
              <div class="edu-cat-title">{cat['title']}</div>
              <div class="edu-cat-sub">{len(cat['items'])} item types</div>
            </div>
          </div>
          <ul class="edu-item-list">{items_html}</ul>
          <div class="edu-where">
            <div class="edu-where-label">WHERE TO TAKE IT</div>
            {cat['where']}
          </div>
          <div class="edu-tip">{cat['tip']}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


def render_recycling_tips():
    st.markdown(EDUCATION_CSS, unsafe_allow_html=True)
    st.markdown('<div class="edu-page">', unsafe_allow_html=True)
    st.markdown("""
    <div style="padding:16px 0 8px;">
      <div style="font-size:15px;font-weight:700;color:#eee;font-family:'Inter',sans-serif;">
        🔄 Recycling Tips by Material
      </div>
      <div style="font-size:12px;color:#666;margin-top:4px;font-family:'Inter',sans-serif;">
        Practical advice for every waste class in EarthMender AI
      </div>
    </div>
    """, unsafe_allow_html=True)

    for i, tip in enumerate(RECYCLING_TIPS, 1):
        tips_html = "".join(
            f'<div class="tip-item">'
            f'<div class="tip-check" style="background:rgba({",".join(str(int(tip["color"].lstrip("#")[j:j+2],16)) for j in (0,2,4))},0.2);">'
            f'<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="{tip["color"]}" stroke-width="3" stroke-linecap="round"><polyline points="20 6 9 17 4 12"/></svg>'
            f'</div>'
            f'<div class="tip-text">{t}</div>'
            f'</div>'
            for t in tip["tips"]
        )
        st.markdown(f"""
        <div class="tip-card" style="background:{tip['bg']};">
          <div class="tip-card-header">
            <div>
              <div class="tip-card-title">{tip['title']}</div>
              <div style="font-size:11px;color:#666;font-family:'Inter',sans-serif;margin-top:2px;">{tip['sub']}</div>
            </div>
            <div class="tip-card-num">{i}/{len(RECYCLING_TIPS)}</div>
          </div>
          {tips_html}
          <div class="tip-fact" style="background:{tip['fact_bg']};">
            <div class="tip-fact-label" style="color:{tip['color']};">💡 DID YOU KNOW?</div>
            <div class="tip-fact-text">{tip['fact']}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


def render_quiz():
    st.markdown(EDUCATION_CSS, unsafe_allow_html=True)
    st.markdown('<div class="edu-page">', unsafe_allow_html=True)

    # Init quiz state
    for k, v in [
        ("quiz_started", False), ("quiz_questions", []),
        ("quiz_index", 0), ("quiz_score", 0),
        ("quiz_done", False), ("quiz_answered", False),
        ("quiz_feedback_correct", None), ("quiz_feedback_explain", ""),
    ]:
        if k not in st.session_state:
            st.session_state[k] = v

    # ── SPLASH ────────────────────────────────────────────────────────────────
    if not st.session_state.quiz_started:
        st.markdown("""
        <div class="quiz-splash">
          <div class="quiz-splash-icon">🧠</div>
          <div class="quiz-splash-title">Waste Knowledge Quiz</div>
          <div class="quiz-splash-sub">12 True/False questions</div>
          <div class="quiz-splash-sub" style="color:#4caf50;font-weight:600;margin-top:6px;">
            Can you score 10 or more? 🏆
          </div>
        </div>
        """, unsafe_allow_html=True)

        # Score legend cards
        cols = st.columns(3)
        for col, (emoji, label, color, bg) in zip(cols, [
            ("🏆","10–12","#81c784","rgba(76,175,80,0.12)"),
            ("👍","7–9",  "#ffd54f","rgba(255,193,7,0.12)"),
            ("📚","0–6",  "#ef9a9a","rgba(244,67,54,0.1)"),
        ]):
            col.markdown(f"""
            <div style="background:{bg};border-radius:14px;padding:14px 8px;
                 text-align:center;border:0.5px solid rgba(255,255,255,0.07);">
              <div style="font-size:26px;">{emoji}</div>
              <div style="font-size:14px;font-weight:700;color:{color};
                   font-family:'Inter',sans-serif;margin-top:4px;">{label}</div>
            </div>
            """, unsafe_allow_html=True)

        st.write("")
        if st.button("🚀 Start Quiz", type="primary", use_container_width=True):
            st.session_state.update({
                "quiz_started":   True,
                "quiz_questions": random.sample(QUIZ_QUESTIONS, len(QUIZ_QUESTIONS)),
                "quiz_index":     0,
                "quiz_score":     0,
                "quiz_done":      False,
                "quiz_answered":  False,
            })
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        return

    # ── RESULTS ───────────────────────────────────────────────────────────────
    if st.session_state.quiz_done:
        score = st.session_state.quiz_score
        total = len(st.session_state.quiz_questions)
        pct   = int(score / total * 100)

        if pct >= 83:
            emoji, grade, color, bg = "🏆","Excellent!","#81c784","rgba(76,175,80,0.12)"
            msg = "You're an EarthMender champion! Share with your community."
        elif pct >= 58:
            emoji, grade, color, bg = "👍","Good Job!","#ffd54f","rgba(255,193,7,0.1)"
            msg = "Solid knowledge! Review Recycling Tips to go further."
        else:
            emoji, grade, color, bg = "📚","Keep Learning!","#ef9a9a","rgba(244,67,54,0.1)"
            msg = "Check the Sorting Guide and Recycling Tips, then try again!"

        st.markdown(f"""
        <div class="quiz-result" style="background:{bg};border-color:{color}40;">
          <div class="quiz-result-icon">{emoji}</div>
          <div class="quiz-result-grade" style="color:{color};">{grade}</div>
          <div class="quiz-result-score">{score} / {total} &nbsp;·&nbsp; {pct}%</div>
          <div class="quiz-result-msg">{msg}</div>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔁 Try Again", use_container_width=True):
                st.session_state.update({
                    "quiz_started":   True,
                    "quiz_questions": random.sample(QUIZ_QUESTIONS, len(QUIZ_QUESTIONS)),
                    "quiz_index": 0, "quiz_score": 0,
                    "quiz_done": False, "quiz_answered": False,
                })
                st.rerun()
        with col2:
            if st.button("📚 Study Tips", use_container_width=True):
                st.session_state.quiz_started = False
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)
        return

    # ── QUESTION ──────────────────────────────────────────────────────────────
    questions = st.session_state.quiz_questions
    idx       = st.session_state.quiz_index
    q         = questions[idx]
    total     = len(questions)
    pct_done  = idx / total * 100

    # Progress bar
    st.markdown(f"""
    <div class="progress-track">
      <div class="progress-fill" style="width:{pct_done}%;"></div>
    </div>
    """, unsafe_allow_html=True)

    # Question card
    st.markdown(f"""
    <div class="quiz-card">
      <div class="quiz-card-num">
        <span>Question {idx+1} of {total}</span>
        <span style="color:#555;">Score: {st.session_state.quiz_score}</span>
      </div>
      <div class="quiz-question">{q['question']}</div>
    </div>
    """, unsafe_allow_html=True)

    # Feedback (shown after answering)
    if st.session_state.quiz_answered:
        correct = st.session_state.quiz_feedback_correct
        explain = st.session_state.quiz_feedback_explain
        if correct:
            st.markdown(f"""
            <div class="quiz-feedback-correct">
              <div class="quiz-fb-header" style="color:#81c784;">✅ Correct!</div>
              <div class="quiz-fb-explain">{explain}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            ans_txt = "TRUE" if q["answer"] else "FALSE"
            st.markdown(f"""
            <div class="quiz-feedback-wrong">
              <div class="quiz-fb-header" style="color:#ef9a9a;">
                ❌ Incorrect — Answer is {ans_txt}
              </div>
              <div class="quiz-fb-explain">{explain}</div>
            </div>
            """, unsafe_allow_html=True)

        label = "➡️ Next" if idx+1 < total else "🏁 See Results"
        if st.button(label, type="primary", use_container_width=True):
            st.session_state.quiz_index    += 1
            st.session_state.quiz_answered  = False
            if st.session_state.quiz_index >= total:
                st.session_state.quiz_done = True
            st.rerun()

    else:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅  TRUE", type="primary", use_container_width=True):
                _answer(True, q)
        with col2:
            if st.button("❌  FALSE", use_container_width=True):
                _answer(False, q)

    st.markdown("</div>", unsafe_allow_html=True)


def _answer(user_ans: bool, q: dict):
    correct = q["answer"]
    if user_ans == correct:
        st.session_state.quiz_score += 1
        st.session_state.quiz_feedback_correct = True
    else:
        st.session_state.quiz_feedback_correct = False
    st.session_state.quiz_feedback_explain = q["explanation"]
    st.session_state.quiz_answered = True
    st.rerun()


# ── MASTER RENDER ─────────────────────────────────────────────────────────────
def render_education_tab():
    sub1, sub2, sub3 = st.tabs([
        "🗂️ Sorting Guide",
        "🔄 Recycling Tips",
        "🧠 Quiz",
    ])
    with sub1:
        render_sorting_guide()
    with sub2:
        render_recycling_tips()
    with sub3:
        render_quiz()
