import re
from langdetect import detect
from deep_translator import GoogleTranslator

# ---------------- LANGUAGE DETECTION ----------------
def detect_language(msg):
    try:
        lang_code = detect(msg)
        lang_map = {
            "en": "English",
            "hi": "Hindi",
            "ta": "Tamil",
            "te": "Telugu",
            "kn": "Kannada",
            "ml": "Malayalam"
        }
        return lang_map.get(lang_code, lang_code)
    except:
        return "Unknown"

# ---------------- TRANSLATION ----------------
def translate_to_english(msg):
    try:
        return GoogleTranslator(source='auto', target='en').translate(msg)
    except:
        return msg

# ---------------- KEYWORDS ----------------
SCAM_KEYWORDS = [
    "click", "urgent", "verify", "kyc",
    "account", "blocked", "login", "otp",
    "bank", "update", "suspended"
]

# ---------------- HIGHLIGHT ----------------
def highlight_words(msg):
    words = msg.split()
    highlighted = []

    for w in words:
        clean_word = w.lower().strip(".,!?")

        if clean_word in SCAM_KEYWORDS:
            highlighted.append(f"[{w.upper()}]")
        else:
            highlighted.append(w)

    return " ".join(highlighted)

# ---------------- ENTITY EXTRACTION ----------------
def extract_entities(msg):
    upi_ids = re.findall(r'\b[\w.-]+@[\w]+\b', msg)
    links = re.findall(r'http[s]?://\S+', msg)
    amounts = re.findall(r'₹\d+|\d+\s?rs', msg.lower())

    return {
        "upi_ids": upi_ids,
        "links": links,
        "amounts": amounts
    }

# ---------------- RISK CALCULATION ----------------
def calculate_risk(msg):
    msg_lower = msg.lower()
    risk = 0
    reasons = []

    keyword_scores = {
        "click": 20,
        "urgent": 25,
        "verify": 20,
        "kyc": 20,
        "account": 10,
        "blocked": 20,
        "login": 15,
        "otp": 25,
        "bank": 15,
        "update": 10,
        "suspended": 20
    }

    for word, score in keyword_scores.items():
        if word in msg_lower:
            risk += score
            reasons.append(f"Suspicious keyword: {word}")

    if "http" in msg_lower:
        risk += 30
        reasons.append("Contains suspicious link")

    return risk, reasons

# ---------------- MAIN FUNCTION ----------------
def analyze_text(msg):
    language = detect_language(msg)
    translated_msg = translate_to_english(msg)
    highlighted_msg = highlight_words(msg)

    risk, reasons = calculate_risk(translated_msg)
    entities = extract_entities(msg)

    if risk >= 60:
        label = "FRAUD"
    elif risk >= 30:
        label = "SUSPICIOUS"
    else:
        label = "SAFE"

    return {
        "language": language,
        "original_text": msg,
        "translated_text": translated_msg,
        "highlighted_text": highlighted_msg,
        "label": label,
        "risk_score": risk,
        "confidence": round(min(risk/100, 1.0), 2),
        "reasons": reasons,
        "entities": entities
    }

# ---------------- PRETTY OUTPUT ----------------
def pretty_print(result):
    print("\n" + "="*40)
    print("🔍 SCAM ANALYSIS RESULT")
    print("="*40)

    print(f"🌐 Language     : {result.get('language')}")
    print(f"🧾 Label        : {result.get('label')}")
    print(f"📊 Risk Score   : {result.get('risk_score')}")
    print(f"🤖 Confidence   : {result.get('confidence')}")

    print("\n📝 Highlighted Message:")
    print(result.get("highlighted_text"))

    print("\n📌 Reasons:")
    for r in result.get('reasons', []):
        print("  ✔", r)

    entities = result.get('entities', {})

    print("\n📊 Extracted Info:")
    print("  💳 UPI IDs :", entities.get('upi_ids', []))
    print("  🔗 Links   :", entities.get('links', []))
    print("  💰 Amounts :", entities.get('amounts', []))

    print("="*40 + "\n")

# ---------------- TEST ----------------
msg = "Your account is blocked, click http://fake.com now"
result = analyze_text(msg)
pretty_print(result)