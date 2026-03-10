import requests
import json

# Ganti dengan API key Gemini kamu
API_KEY = "AIzaSyBFhIQEnteOSLjn56QQnrEAzEw_s6853f4"

def tanya_ai(pertanyaan, riwayat=[]):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"
    
    # Susun riwayat percakapan
    contents = []
    for pesan in riwayat:
        contents.append(pesan)
    contents.append({
        "role": "user",
        "parts": [{"text": pertanyaan}]
    })
    
    payload = {"contents": contents}
    headers = {"Content-Type": "application/json"}
    
    response = requests.post(url, headers=headers, json=payload)
    data = response.json()
    
    jawaban = data["candidates"][0]["content"]["parts"][0]["text"]
    return jawaban, contents

def jalankan_agent():
    print("=" * 40)
    print("   AI AGENT - Powered by Gemini")
    print("   Ketik 'keluar' untuk berhenti")
    print("=" * 40)
    
    riwayat = []
    
    while True:
        pertanyaan = input("\n🧑 Kamu: ")
        
        if pertanyaan.lower() == "keluar":
            print("👋 Sampai jumpa!")
            break
        
        if not pertanyaan.strip():
            continue
        
        print("🤖 Agent sedang berpikir...")
        
        try:
            jawaban, riwayat_baru = tanya_ai(pertanyaan, riwayat)
            
            # Simpan riwayat percakapan
            riwayat = riwayat_baru
            riwayat.append({
                "role": "model",
                "parts": [{"text": jawaban}]
            })
            
            print(f"\n🤖 Agent: {jawaban}")
            
        except Exception as e:
            print(f"❌ Error: {e}")

# Jalankan!
jalankan_agent()
