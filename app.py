import streamlit as st
import cv2
import numpy as np

from privacy_detector import analyze_image


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Privacy Guard AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown(
    """
    <style>

    .stApp {
        background: #080b12;
        color: #f5f7ff;
    }

    .block-container {
        max-width: 1200px;
        padding-top: 2.5rem;
        padding-bottom: 3rem;
    }

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        background: transparent !important;
    }

    [data-testid="stFileUploader"] {
        background: #111827;
        border: 1px dashed #4f46e5;
        border-radius: 18px;
        padding: 12px;
    }

    .section-space {
        margin-top: 25px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ==========================================
# HEADER
# ==========================================

st.title("🛡️ Privacy Guard AI")

st.caption(
    "AI-assisted screenshot privacy scanner • "
    "Detect → Analyze → Redact"
)


# ==========================================
# UPLOAD SECTION
# ==========================================

st.subheader("📸 Upload a screenshot")

st.caption(
    "Use a synthetic/demo screenshot for testing. "
    "Avoid uploading real private information."
)

uploaded_file = st.file_uploader(
    "Choose an image",
    type=["png", "jpg", "jpeg"],
    label_visibility="visible"
)


# ==========================================
# IMAGE PROCESSING
# ==========================================

if uploaded_file is not None:

    file_bytes = np.asarray(
        bytearray(uploaded_file.read()),
        dtype=np.uint8
    )

    image = cv2.imdecode(
        file_bytes,
        cv2.IMREAD_COLOR
    )

    if image is None:

        st.error(
            "❌ Could not read this image."
        )

    else:

        with st.spinner(
            "🔍 Scanning screenshot for sensitive information..."
        ):

            result = analyze_image(image)


        # ==========================================
        # RESULTS
        # ==========================================

        st.divider()

        st.subheader("🔎 Privacy Scan Results")

        score = result["risk_score"]
        level = result["risk_level"]


        # ==========================================
        # RESULT CARDS
        # ==========================================

        col1, col2, col3 = st.columns(3)


        with col1:

            st.metric(
                label="Privacy Risk",
                value=f"{score}/100"
            )


        with col2:

            st.metric(
                label="Risk Level",
                value=level
            )


        with col3:

            total_detected = sum(
                result["counts"].values()
            )

            st.metric(
                label="Detected Items",
                value=total_detected
            )


        # ==========================================
        # DETECTION SUMMARY
        # ==========================================

        st.subheader("🧠 Detection Summary")

        counts = result["counts"]

        detected_items = []


        if counts["email"] > 0:

            detected_items.append(
                f"📧 Email × {counts['email']}"
            )


        if counts["phone"] > 0:

            detected_items.append(
                f"📱 Phone × {counts['phone']}"
            )


        if counts["url"] > 0:

            detected_items.append(
                f"🔗 URL × {counts['url']}"
            )


        if counts["secret"] > 0:

            detected_items.append(
                f"🔑 Secret × {counts['secret']}"
            )


        if counts["entity"] > 0:

            detected_items.append(
                f"👤 Entity × {counts['entity']}"
            )


        if detected_items:

            st.write(
                "  •  ".join(detected_items)
            )

        else:

            st.success(
                "✨ No sensitive patterns detected"
            )


        # ==========================================
        # ORIGINAL VS REDACTED
        # ==========================================

        st.divider()

        st.subheader("🖼️ Original vs Redacted")

        st.caption(
            "Compare the uploaded screenshot with "
            "the automatically redacted version."
        )


        original_rgb = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2RGB
        )

        redacted_rgb = cv2.cvtColor(
            result["redacted_image"],
            cv2.COLOR_BGR2RGB
        )


        col_original, col_redacted = st.columns(
            2,
            gap="large"
        )


        with col_original:

            st.markdown("### 🖼️ Original")

            st.image(
                original_rgb,
                use_container_width=True
            )


        with col_redacted:

            st.markdown("### 🔒 Redacted")

            st.image(
                redacted_rgb,
                use_container_width=True
            )


        # ==========================================
        # OCR TEXT
        # ==========================================

        with st.expander(
            "📝 View OCR extracted text"
        ):

            if result["text"].strip():

                st.code(
                    result["text"],
                    language="text"
                )

            else:

                st.info(
                    "No readable text was detected."
                )


# ==========================================
# CLEAN HOME SCREEN
# ==========================================

else:

    st.divider()

    st.markdown("## 🛡️ Ready to protect your screenshot?")

    st.write(
        "Upload a screenshot and Privacy Guard AI "
        "will scan it for potentially sensitive "
        "information, calculate its privacy risk, "
        "and create a redacted version automatically."
    )

    st.info(
        "🔍 Detect  •  📊 Analyze  •  🔒 Redact"
    )


# ==========================================
# FOOTER
# ==========================================

st.divider()

st.caption(
    "Privacy Guard AI • Built with Python, EasyOCR, "
    "OpenCV & Streamlit • Educational Prototype"
)