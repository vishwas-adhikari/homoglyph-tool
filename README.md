# Homoglyph Toolkit – A Cybersecurity Web Application

<p align="center">
  <img src="https://github.com/vishwas-adhikari/homoglyph-tool/blob/main/poc-ss/HomePage.jpg" alt="Home Page" width="300">
  <img src="https://github.com/vishwas-adhikari/homoglyph-tool/blob/main/poc-ss/detector.jpg" alt="Detector" width="300">
  <img src="https://github.com/vishwas-adhikari/homoglyph-tool/blob/main/poc-ss/safedetection.jpg" alt="Safe Detection" width="300">
  <img src="https://github.com/vishwas-adhikari/homoglyph-tool/blob/main/poc-ss/Generator.jpg" alt="Generator" width="300">
  <img src="https://github.com/vishwas-adhikari/homoglyph-tool/blob/main/poc-ss/shortner.jpg" alt="Shortener" width="300">
</p>

A powerful, web-based cybersecurity tool built with Django and Python to both **detect** and **generate** homoglyph domain attacks. This toolkit serves as a practical resource for security analysts, penetration testers, and anyone interested in understanding the deceptive nature of lookalike domains used in phishing attacks.

---

## 🎯 The Problem: Homoglyph Attacks

Homoglyph attacks exploit the fact that many characters from different alphabets (e.g., Latin, Cyrillic, Greek) or symbols look identical or very similar. Attackers register domains like `gооgle.com` (using Cyrillic 'о's) to trick users into believing they are on a legitimate site, leading to credential theft and malware distribution.

This toolkit provides both defensive and offensive capabilities to combat this threat.

## ✨ Key Features

This application is a "one-stop-shop" for homoglyph analysis, featuring three integrated tools:

### 1. 🛡️ Homoglyph Detector
A robust analysis engine that inspects a domain for multiple types of visual deception:
*   **Cross-Script Detection:** Identifies characters from different alphabets (e.g., Cyrillic `а` vs. Latin `a`).
*   **Combining Marks:** Detects invisible combining characters (e.g., accents) used to modify standard letters (`n` + `̀` → `ǹ`).
*   **Punycode Awareness:** Automatically decodes Punycode domains (`xn--...`) to analyze their true Unicode form.
*   **Similarity Scoring:** Provides a percentage score to quickly gauge how closely a domain resembles its normalized form.

### 2. 🧪 Homoglyph Generator
An offensive security tool for training, awareness, and red team simulations:
*   **Realistic Variants:** Generates a curated list of high-impact, visually deceptive domain variants from a legitimate input.
*   **Curated Mapping:** Uses a custom, expert-curated JSON map that focuses on the most effective and common character swaps seen in real-world attacks.
*   **Multi-Type Swaps:** Includes not just Unicode homoglyphs but also common visual tricks like `l` → `1`, `o` → `0`, `s` → `$`, and `m` → `rn`.

### 3. 🔗 URL Shortener
A utility to "weaponize" generated domains for controlled phishing simulations:
*   **One-Click Shortening:** Seamlessly shorten any generated lookalike domain using the TinyURL API.
*   **Integrated Workflow:** Allows for a complete red team workflow, from generating a deceptive domain to creating a ready-to-use shortened link for campaigns.

---

## 🛠️ Tech Stack & Architecture

| Layer         | Technology / Library                                       |
|---------------|------------------------------------------------------------|
| **Language**  | Python 3.11+                                               |
| **Framework** | Django 5.x                                                 |
| **API**       | Django REST Framework (implicit via `JsonResponse`)        |
| **Core Libs** | `requests` (for URL Shortener), `unicodedata` (for normalization) |
| **Frontend**  | Plain HTML, CSS, and JavaScript (No frameworks)            |
| **Database**  | SQLite 3 (Default for Django)                              |

The core of this application is a **pre-compiled, curated data map**. A standalone Python script (`build_map.py`) processes a raw list of Unicode characters and generates a clean `homoglyph_map.json`. The Django application loads this perfect map at startup, ensuring high performance and reliability.

---

## 🚀 Getting Started: Local Setup & Installation

**1. Clone the Repository**
```bash
git clone https://github.com/YourUsername/homoglyph-toolkit-django.git
cd homoglyph-toolkit-django
