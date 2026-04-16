# VitalScan-Final
# VitalScan AI: The Privacy-First Medical Sentinel 🩺

**Aura-Sync** is a contactless medical diagnostic hub designed for rural telemedicine. It eliminates the need for expensive hardware sensors by using software-only **rPPG (Remote Photoplethysmography)** principles.

## 🏆 MLH Prize Track Integrations
We have integrated multiple sponsor technologies to build a robust medical SaaS:

* **Google Gemini API**: Used for AI-driven clinical reasoning. It analyzes raw vitals metadata to generate doctor-ready reports.
* **MongoDB Atlas**: Serves as our "Encrypted Health Vault" for storing anonymized patient history.
* **Solana Blockchain**: Provides decentralized data verification to ensure patient records are tamper-proof.
* **Auth0**: Implements secure medical staff identity management via Universal Login.
* **ElevenLabs**: Converts clinical reports into AI-voice for better accessibility in clinical environments.

## 🛠️ How it Works
1. **Signal Capture**: Analyzes light absorption changes in the skin (face/finger) via webcam.
2. **Analysis**: Gemini 1.5 Flash processes the signals for clinical stability.
3. **Storage**: Data is hashed on Solana and stored in MongoDB.

## 🚀 Setup
This project is optimized for **Vercel** deployment with a Python Flask backend.
