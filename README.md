# EDITH.ai

### Environmental Digital Intelligence for Threat & Habitat

EDITH.ai is an AI-powered wildlife detection and human-wildlife conflict management system designed to help protect agricultural areas while supporting safer, non-harmful wildlife response.

## 🌿 Problem

Human-wildlife conflict can cause significant crop damage and create safety risks for both farmers and wildlife.

Traditional monitoring methods may depend on manual observation and delayed reporting.

EDITH.ai aims to provide an intelligent monitoring layer that can detect wildlife, assess risk, estimate potential crop damage, analyze movement patterns, and support timely response.

## 🤖 Key Features

- 🐘 Wildlife species detection using YOLO
- 📷 Real-time camera-based monitoring
- ⚠️ Wildlife risk assessment
- 🌾 Crop damage assessment
- 📊 Wildlife movement intelligence
- 🚨 Farmer and authority alert concept
- 🔊 Non-harmful deterrent response concept
- 🖥️ Interactive Streamlit dashboard
- ⚡ GPU-accelerated inference support

## 🐾 Supported Wildlife Classes

The custom wildlife detection model is trained for:

- Bear
- Deer
- Elephant
- Leopard
- Monkey
- Tiger
- WildBoar

## 🧠 System Architecture

```text
Camera / Image
      │
      ▼
┌──────────────────┐
│ Wildlife Detector│
│      YOLO        │
└────────┬─────────┘
         │
         ▼
   Species + Confidence
         │
         ▼
┌──────────────────┐
│   Risk Engine    │
└────────┬─────────┘
         │
         ├───────────────┐
         ▼               ▼
┌────────────────┐ ┌──────────────────┐
│ Damage Analysis│ │ Movement Analysis│
└───────┬────────┘ └────────┬─────────┘
        │                   │
        └─────────┬─────────┘
                  ▼
          EDITH Intelligence
                  │
                  ▼
       Alert / Response System
