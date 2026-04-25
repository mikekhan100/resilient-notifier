# Resilient Notifier (Circuit Breaker Pattern)

A high-resilience notification system built with **Python** and **FastAPI**. This project demonstrates the **Circuit Breaker** design pattern, a strategy used in microservices to prevent cascading failures.

## 🚀 The Problem
When integrating with third-party APIs (like Twilio, Stripe, or AWS), those services will inevitably fail or experience latency.  Without a safeguard:
1. Your application hangs while waiting for timeouts.
2. Thread pools and memory become exhausted.
3. A failure in a downstream service "cascades" and crashes the entire system.

## 🛠 The Solution
This project implements a **State Machine** that sits between the app and the flaky service:

- **CLOSED (Healthy)**: Requests flow normally.  If a request fails, the breaker increments a counter.
- **OPEN (Tripped)**: Once the failure threshold is hit, the circuit "trips."  All further requests fail **instantly** without hitting the network, giving the provider time to recover.
- **HALF-OPEN (Testing)**: After a cooldown period, the breaker allows a single "probe" request.  If it succeeds, the circuit closes; if it fails, the cooldown resets.



## 💻 Tech Stack
- **Python 3.14+**
- **FastAPI** (Web Layer)
- **Uvicorn** (ASGI Server)
- **Git** (Version Control)

## 🚦 How to Run
1. **Clone the repo:**
   ```bash
   git clone https://github.com/mikekhan100/resilient-notifier.git
   cd resilient-notifier

2. **Set up environment:**
   python -m venv venv
   source venv/bin/activate  # Windows: .\venv\Scripts\activate
   pip install fastapi uvicorn

3. **Launch the API:**
   uvicorn main:app --reload

4. **Test it:**
   Visit http://127.0.0.1:8000/send-notification and refresh the page to watch the state transitions in your terminal.