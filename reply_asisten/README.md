# Reply Assistant 🤖

Asisten reply pesan media sosial berbasis terminal, powered by Google Gemini API.

## Fitur
- 4 gaya balasan: Santai, Formal, Lucu, Singkat
- 3 bahasa: Indonesia, Inggris, Campur (Indo-Eng)
- Bisa dipakai di Termux (Android) maupun Linux/Mac
- Ringan, hanya butuh `requests` dan `colorama`

## Instalasi

```bash
git clone https://github.com/username/reply-assistant.git
cd reply-assistant
pip install -r requirements.txt
```

## Setup API Key

1. Daftar gratis di [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
2. Buat file `.env` dari template:

```bash
cp .env.example .env
nano .env  # isi API key kamu
```

Isi file `.env`:
```
GEMINI_API_KEY=AIza...
```

## Cara Pakai

```bash
python reply_assistant.py
```

## Catatan
- File `.env` sudah di-ignore oleh `.gitignore`, aman tidak akan ter-commit
- Gemini API gratis dengan quota harian yang cukup untuk pemakaian normal
