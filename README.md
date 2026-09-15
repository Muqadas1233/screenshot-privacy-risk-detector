# 🛡️ Screenshot Privacy Risk Detector

An AI-assisted privacy tool that analyzes screenshots for potentially sensitive information before they are shared online.

## Problem

Screenshots can accidentally expose information such as:

- Email addresses
- Phone numbers
- URLs
- Secret-like tokens
- Other potentially sensitive text

Manually checking every screenshot before sharing can be inconvenient and error-prone.

## Here's the Solution

Screenshot Privacy Risk Detector analyzes an uploaded screenshot using OCR and pattern-based detection.

It:

1. Extracts text from the screenshot
2. Detects potentially sensitive patterns
3. Calculates a privacy risk score
4. Assigns a risk level
5. Automatically redacts detected information
6. Shows the original and redacted versions side-by-side

## ✨ Features

- 📸 Screenshot upload
- 🔍 OCR-based text extraction
- 📧 Email detection
- 📱 Phone number detection
- 🔗 URL detection
- 🔑 Secret-like pattern detection
- 📊 Privacy risk scoring
- 🔒 Automatic redaction
- 🌙 Dark modern interface
- 🖼️ Original vs Redacted comparison

## The Detection Workflow

```text
Screenshot
     ↓
OCR Text Extraction
     ↓
Sensitive Information Detection
     ↓
Risk Scoring
     ↓
Risk Level
     ↓
Automatic Redaction
     ↓
Privacy-Safe Preview
