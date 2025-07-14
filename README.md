# 📚 Course Availability Notifier

This is a backend service that scrapes live registration data and automatically notifies users via SMS when a seat becomes available in their desired course.

## 🚀 Overview

Users enter their:
- Name
- Phone number
- Email
- Desired course (CRN)

Every 5 minutes, the app scrapes updated course registration data. If a user’s requested class has an open seat, they automatically receive a text notification.

This is a continuation of my work in the previous repository: [insert link here]

---

## 🛠 Features

- Web scraping of live course data
- Periodic background checks (every 5 minutes)
- SMS notifications using Twilio
- Clean and modular backend architecture
- Easily extendable with a frontend for user input

---

## 🧱 Tech Stack

- **Python** (Core logic)
- **Selenium / Playwright** (Web scraping)
- **FastAPI / Flask** (REST API for user registration)
- **Twilio API** (SMS notifications)
- **SQLite / JSON** (User data storage)
- **Schedule / APScheduler** (Recurring scraping tasks)

---

## 📁 Project Structure

Will Update Soon

---

## 📝 Getting Started

Will Update Soon