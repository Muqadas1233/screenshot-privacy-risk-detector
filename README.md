# 🛡️ Screenshot Privacy Risk Detector

An AI-assisted privacy tool that analyzes screenshots for potentially sensitive information before they are shared.

## Problem

Screenshots can accidentally expose emails, phone numbers, URLs, secret-like tokens, names, organizations, or locations.

## Solution

This project combines OCR, NLP, regular-expression pattern detection, risk scoring, and automatic redaction.

## Features

- Screenshot upload
- OCR-based text extraction
- Email detection
- Phone number detection
- URL detection
- Secret-like pattern detection
- NLP entity detection
- Privacy risk scoring
- Automatic redaction
- Streamlit interface

## Technologies

- Python
- EasyOCR
- spaCy
- OpenCV
- Regular Expressions
- NumPy
- Streamlit

## Workflow

Screenshot  
↓  
OCR  
↓  
Sensitive Information Detection  
↓  
Privacy Risk Scoring  
↓  
Automatic Redaction

## Disclaimer

This is an educational prototype and does not guarantee that all sensitive information will be detected.

## Future Improvements

- More PII categories
- Better entity recognition
- Improved redaction
- Multi-language OCR
- More advanced risk scoring
- Cloud-based privacy scanning

## Author

5th Semester BSAI Student