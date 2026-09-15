import re
import cv2
import numpy as np
import easyocr


# ==========================================
# Initialize OCR
# ==========================================

reader = easyocr.Reader(["en"], gpu=False)


# ==========================================
# Regular Expression Patterns
# ==========================================

EMAIL_PATTERN = (
    r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
)

PHONE_PATTERN = (
    r"\b(?:\+?\d{1,3}[-.\s]?)?"
    r"(?:\(?\d{2,4}\)?[-.\s]?)?"
    r"\d{3,4}[-.\s]?\d{3,4}\b"
)

URL_PATTERN = (
    r"\b(?:https?://|www\.)[^\s]+\b"
)

SECRET_PATTERN = (
    r"\b(?:"
    r"sk-[A-Za-z0-9]{20,}|"
    r"AKIA[0-9A-Z]{16}|"
    r"[A-Za-z0-9_-]{32,}"
    r")\b"
)


# ==========================================
# Pattern Detection
# ==========================================

def detect_patterns(text):

    emails = re.findall(
        EMAIL_PATTERN,
        text
    )

    phones = re.findall(
        PHONE_PATTERN,
        text
    )

    urls = re.findall(
        URL_PATTERN,
        text
    )

    secrets = re.findall(
        SECRET_PATTERN,
        text
    )

    return {
        "email": emails,
        "phone": phones,
        "url": urls,
        "secret": secrets
    }


# ==========================================
# Lightweight Entity Detection
# ==========================================

def detect_entities(text):

    sensitive_entities = []

    indicators = [
        "name:",
        "location:",
        "address:",
        "organization:",
        "company:"
    ]

    text_lower = text.lower()

    for indicator in indicators:

        if indicator in text_lower:

            start = text_lower.find(indicator)

            value = text[start:].split("\n")[0].strip()

            sensitive_entities.append({
                "text": value,
                "label": "POTENTIAL_ENTITY"
            })

    return sensitive_entities


# ==========================================
# Risk Score Calculation
# ==========================================

def calculate_risk_score(
    emails,
    phones,
    urls,
    secrets,
    entities
):

    score = 0

    # Email = 20 points
    score += len(emails) * 20

    # Phone = 25 points
    score += len(phones) * 25

    # URL = 10 points
    score += len(urls) * 10

    # Secret-like pattern = 40 points
    score += len(secrets) * 40

    # Potential entity = 10 points
    score += len(entities) * 10

    # Maximum score = 100
    score = min(score, 100)

    # Risk level
    if score >= 70:
        level = "HIGH"

    elif score >= 40:
        level = "MEDIUM"

    elif score > 0:
        level = "LOW"

    else:
        level = "SAFE"

    return score, level


# ==========================================
# Main Image Analysis
# ==========================================

def analyze_image(image):

    # --------------------------------------
    # OCR
    # --------------------------------------

    results = reader.readtext(image)

    full_text = ""

    for item in results:

        text = item[1]

        full_text += text + " "


    # --------------------------------------
    # Detect Patterns
    # --------------------------------------

    patterns = detect_patterns(full_text)

    emails = patterns["email"]
    phones = patterns["phone"]
    urls = patterns["url"]
    secrets = patterns["secret"]


    # --------------------------------------
    # Detect Potential Entities
    # --------------------------------------

    entities = detect_entities(full_text)


    # --------------------------------------
    # Calculate Risk
    # --------------------------------------

    risk_score, risk_level = calculate_risk_score(
        emails,
        phones,
        urls,
        secrets,
        entities
    )


    # --------------------------------------
    # Create Redacted Image
    # --------------------------------------

    redacted_image = image.copy()


    # --------------------------------------
    # Check Each OCR Detection
    # --------------------------------------

    for item in results:

        box = item[0]

        text = item[1]

        should_redact = False


        # Check email
        if re.search(
            EMAIL_PATTERN,
            text
        ):
            should_redact = True


        # Check phone
        elif re.search(
            PHONE_PATTERN,
            text
        ):
            should_redact = True


        # Check URL
        elif re.search(
            URL_PATTERN,
            text
        ):
            should_redact = True


        # Check secret-like pattern
        elif re.search(
            SECRET_PATTERN,
            text
        ):
            should_redact = True


        # Check potential entity keywords
        else:

            text_lower = text.lower()

            entity_keywords = [
                "name:",
                "location:",
                "address:",
                "organization:",
                "company:"
            ]

            for keyword in entity_keywords:

                if keyword in text_lower:

                    should_redact = True

                    break


        # ----------------------------------
        # Draw Black Redaction Box
        # ----------------------------------

        if should_redact:

            points = np.array(
                box,
                dtype=np.int32
            )

            x_min = np.min(
                points[:, 0]
            )

            y_min = np.min(
                points[:, 1]
            )

            x_max = np.max(
                points[:, 0]
            )

            y_max = np.max(
                points[:, 1]
            )

            cv2.rectangle(
                redacted_image,
                (x_min, y_min),
                (x_max, y_max),
                (0, 0, 0),
                -1
            )


    # ======================================
    # Return Complete Result
    # ======================================

    return {

        "risk_score": risk_score,

        "risk_level": risk_level,

        "counts": {

            "email": len(emails),

            "phone": len(phones),

            "url": len(urls),

            "secret": len(secrets),

            "entity": len(entities)
        },

        "redacted_image": redacted_image,

        "text": full_text
    }