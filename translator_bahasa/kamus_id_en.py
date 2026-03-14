#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════╗
║         KAMUS INDONESIA - INGGRIS v2.0           ║
║    Kamus Kata + Translator Kalimat (Online)      ║
╚══════════════════════════════════════════════════╝
Cara pakai: python kamus_id_en.py
Tombol:
  s        → Cari kata di kamus
  t        → Translator kalimat (butuh internet)
  Tab      → Ganti arah (ID -> EN / EN -> ID)
  Enter    → Lihat detail & contoh kalimat
  k        → Keluar

Install untuk fitur translator:
  pip install deep-translator
"""

import curses
import sys
import threading

# -- Cek deep-translator
try:
    from deep_translator import GoogleTranslator
    HAS_TRANSLATOR = True
except ImportError:
    HAS_TRANSLATOR = False

# ─── DATA KAMUS ───────────────────────────────────────────────────────────────
# Format: (indonesia, inggris, kategori, contoh_id, contoh_en)

KAMUS = [
    # ── SAPAAN & UMUM ──
    ("halo",           "hello",              "Sapaan",    "Halo, apa kabar?",                   "Hello, how are you?"),
    ("selamat pagi",   "good morning",       "Sapaan",    "Selamat pagi, semoga harimu menyenangkan.", "Good morning, have a great day."),
    ("selamat siang",  "good afternoon",     "Sapaan",    "Selamat siang, sudah makan?",        "Good afternoon, have you eaten?"),
    ("selamat malam",  "good evening",       "Sapaan",    "Selamat malam, istirahat yang baik.", "Good evening, rest well."),
    ("selamat tidur",  "good night",         "Sapaan",    "Selamat tidur, mimpi indah.",        "Good night, sweet dreams."),
    ("sampai jumpa",   "goodbye",            "Sapaan",    "Sampai jumpa besok!",                "Goodbye, see you tomorrow!"),
    ("terima kasih",   "thank you",          "Sapaan",    "Terima kasih atas bantuanmu.",       "Thank you for your help."),
    ("sama-sama",      "you're welcome",     "Sapaan",    "Sama-sama, senang bisa membantu.",   "You're welcome, happy to help."),
    ("maaf",           "sorry",              "Sapaan",    "Maaf, saya terlambat.",              "Sorry, I am late."),
    ("permisi",        "excuse me",          "Sapaan",    "Permisi, boleh saya lewat?",         "Excuse me, may I pass?"),
    ("tolong",         "please",             "Sapaan",    "Tolong bantu saya.",                 "Please help me."),
    ("ya",             "yes",                "Sapaan",    "Ya, saya setuju.",                   "Yes, I agree."),
    ("tidak",          "no",                 "Sapaan",    "Tidak, saya tidak mau.",             "No, I don't want to."),
    ("apa kabar",      "how are you",        "Sapaan",    "Apa kabar hari ini?",                "How are you today?"),
    ("baik",           "fine / good",        "Sapaan",    "Saya baik, terima kasih.",           "I am fine, thank you."),
    ("nama saya",      "my name is",         "Sapaan",    "Nama saya Budi.",                    "My name is Budi."),
    ("senang bertemu", "nice to meet you",   "Sapaan",    "Senang bertemu denganmu.",           "Nice to meet you."),

    # ── KATA GANTI ──
    ("saya",           "I / me",             "Kata Ganti", "Saya pergi ke pasar.",              "I go to the market."),
    ("kamu",           "you",                "Kata Ganti", "Kamu sangat pintar.",               "You are very smart."),
    ("dia",            "he / she",           "Kata Ganti", "Dia sedang belajar.",               "He/She is studying."),
    ("kami",           "we (excl.)",         "Kata Ganti", "Kami pergi bersama.",               "We go together."),
    ("kita",           "we (incl.)",         "Kata Ganti", "Kita harus bersatu.",               "We must be united."),
    ("mereka",         "they",               "Kata Ganti", "Mereka bermain di taman.",          "They are playing in the park."),
    ("ini",            "this",               "Kata Ganti", "Ini bukuku.",                       "This is my book."),
    ("itu",            "that",               "Kata Ganti", "Itu rumahnya.",                     "That is his house."),
    ("apa",            "what",               "Kata Ganti", "Apa yang kamu makan?",              "What are you eating?"),
    ("siapa",          "who",                "Kata Ganti", "Siapa namamu?",                     "Who is your name?"),
    ("di mana",        "where",              "Kata Ganti", "Di mana kamu tinggal?",             "Where do you live?"),
    ("kapan",          "when",               "Kata Ganti", "Kapan kamu datang?",                "When will you come?"),
    ("mengapa",        "why",                "Kata Ganti", "Mengapa kamu menangis?",            "Why are you crying?"),
    ("bagaimana",      "how",                "Kata Ganti", "Bagaimana caranya?",                "How do you do it?"),
    ("berapa",         "how much / how many","Kata Ganti", "Berapa harganya?",                  "How much is it?"),

    # ── ANGKA ──
    ("satu",           "one",                "Angka",     "Ada satu apel di meja.",             "There is one apple on the table."),
    ("dua",            "two",                "Angka",     "Saya punya dua kucing.",             "I have two cats."),
    ("tiga",           "three",              "Angka",     "Tiga hari lagi libur.",              "Three more days until holiday."),
    ("empat",          "four",               "Angka",     "Empat musim ada di Eropa.",          "There are four seasons in Europe."),
    ("lima",           "five",               "Angka",     "Lima jari di setiap tangan.",        "Five fingers on each hand."),
    ("enam",           "six",                "Angka",     "Enam sisi kubus.",                   "A cube has six sides."),
    ("tujuh",          "seven",              "Angka",     "Seminggu ada tujuh hari.",           "A week has seven days."),
    ("delapan",        "eight",              "Angka",     "Gurita punya delapan kaki.",         "An octopus has eight legs."),
    ("sembilan",       "nine",               "Angka",     "Sembilan planet di tata surya.",     "Nine planets in the solar system."),
    ("sepuluh",        "ten",                "Angka",     "Sepuluh jari tangan dan kaki.",      "Ten fingers and toes."),
    ("seratus",        "one hundred",        "Angka",     "Seratus persen usaha.",              "One hundred percent effort."),
    ("seribu",         "one thousand",       "Angka",     "Seribu langkah perjalanan.",         "A thousand steps of journey."),

    # ── WAKTU ──
    ("hari",           "day",                "Waktu",     "Hari ini cerah sekali.",             "Today is very sunny."),
    ("minggu",         "week",               "Waktu",     "Minggu depan ada ujian.",            "Next week there is an exam."),
    ("bulan",          "month",              "Waktu",     "Bulan ini sangat sibuk.",            "This month is very busy."),
    ("tahun",          "year",               "Waktu",     "Tahun ini penuh tantangan.",         "This year is full of challenges."),
    ("jam",            "hour / clock",       "Waktu",     "Jam berapa sekarang?",               "What time is it now?"),
    ("menit",          "minute",             "Waktu",     "Tunggu lima menit lagi.",            "Wait five more minutes."),
    ("detik",          "second",             "Waktu",     "Satu detik sangat berharga.",        "One second is very precious."),
    ("pagi",           "morning",            "Waktu",     "Saya bangun pagi setiap hari.",      "I wake up every morning."),
    ("siang",          "afternoon / noon",   "Waktu",     "Siang hari sangat panas.",           "The afternoon is very hot."),
    ("malam",          "night",              "Waktu",     "Malam ini ada bintang banyak.",      "There are many stars tonight."),
    ("kemarin",        "yesterday",          "Waktu",     "Kemarin saya sakit.",                "Yesterday I was sick."),
    ("hari ini",       "today",              "Waktu",     "Hari ini aku bahagia.",              "Today I am happy."),
    ("besok",          "tomorrow",           "Waktu",     "Besok kita pergi bersama.",          "Tomorrow we go together."),
    ("sekarang",       "now",                "Waktu",     "Saya sibuk sekarang.",               "I am busy now."),
    ("nanti",          "later",              "Waktu",     "Nanti kita bicara.",                 "We'll talk later."),
    ("selalu",         "always",             "Waktu",     "Saya selalu tepat waktu.",           "I am always on time."),
    ("sering",         "often",              "Waktu",     "Dia sering terlambat.",              "He is often late."),
    ("kadang",         "sometimes",          "Waktu",     "Kadang saya lupa.",                  "Sometimes I forget."),
    ("jarang",         "rarely",             "Waktu",     "Saya jarang makan fast food.",       "I rarely eat fast food."),
    ("tidak pernah",   "never",              "Waktu",     "Saya tidak pernah merokok.",         "I never smoke."),

    # ── KELUARGA ──
    ("ayah",           "father",             "Keluarga",  "Ayah saya seorang dokter.",          "My father is a doctor."),
    ("ibu",            "mother",             "Keluarga",  "Ibu memasak setiap pagi.",           "Mother cooks every morning."),
    ("kakak",          "older sibling",      "Keluarga",  "Kakak saya sudah menikah.",          "My older sibling is married."),
    ("adik",           "younger sibling",    "Keluarga",  "Adik saya masih kecil.",             "My younger sibling is still small."),
    ("nenek",          "grandmother",        "Keluarga",  "Nenek membuat kue yang enak.",       "Grandmother makes delicious cake."),
    ("kakek",          "grandfather",        "Keluarga",  "Kakek suka berkebun.",               "Grandfather likes gardening."),
    ("paman",          "uncle",              "Keluarga",  "Paman datang dari jauh.",            "Uncle came from far away."),
    ("bibi",           "aunt",               "Keluarga",  "Bibi membawa oleh-oleh.",            "Aunt brought souvenirs."),
    ("anak",           "child",              "Keluarga",  "Anak itu sangat lucu.",              "That child is very cute."),
    ("keluarga",       "family",             "Keluarga",  "Keluarga adalah segalanya.",         "Family is everything."),
    ("suami",          "husband",            "Keluarga",  "Suamiku sangat perhatian.",          "My husband is very caring."),
    ("istri",          "wife",               "Keluarga",  "Istriku masak dengan baik.",         "My wife cooks well."),

    # ── MAKANAN & MINUMAN ──
    ("nasi",           "rice",               "Makanan",   "Nasi adalah makanan pokok Indonesia.","Rice is Indonesia's staple food."),
    ("air",            "water",              "Makanan",   "Minum air yang cukup setiap hari.",  "Drink enough water every day."),
    ("makan",          "eat",                "Makanan",   "Ayo makan bersama!",                 "Let's eat together!"),
    ("minum",          "drink",              "Makanan",   "Kamu mau minum apa?",                "What do you want to drink?"),
    ("lapar",          "hungry",             "Makanan",   "Saya sangat lapar sekarang.",        "I am very hungry now."),
    ("kenyang",        "full / satisfied",   "Makanan",   "Saya sudah kenyang.",                "I am already full."),
    ("haus",           "thirsty",            "Makanan",   "Saya haus sekali.",                  "I am very thirsty."),
    ("enak",           "delicious",          "Makanan",   "Makanan ini enak sekali!",           "This food is very delicious!"),
    ("pedas",          "spicy",              "Makanan",   "Sambal ini sangat pedas.",           "This sambal is very spicy."),
    ("manis",          "sweet",              "Makanan",   "Kue ini manis sekali.",              "This cake is very sweet."),
    ("asin",           "salty",              "Makanan",   "Sup ini terlalu asin.",              "This soup is too salty."),
    ("pahit",          "bitter",             "Makanan",   "Kopi tanpa gula itu pahit.",         "Coffee without sugar is bitter."),
    ("masak",          "cook",               "Makanan",   "Ibu sedang masak di dapur.",         "Mother is cooking in the kitchen."),
    ("restoran",       "restaurant",         "Makanan",   "Ayo makan di restoran itu.",         "Let's eat at that restaurant."),
    ("warung",         "small food stall",   "Makanan",   "Warung itu murah dan enak.",         "That food stall is cheap and delicious."),
    ("buah",           "fruit",              "Makanan",   "Makan buah itu sehat.",              "Eating fruit is healthy."),
    ("sayur",          "vegetable",          "Makanan",   "Sayur bayam kaya zat besi.",         "Spinach is rich in iron."),
    ("daging",         "meat",               "Makanan",   "Sate daging sangat lezat.",          "Meat satay is very tasty."),
    ("ikan",           "fish",               "Makanan",   "Ikan goreng adalah favoritku.",      "Fried fish is my favorite."),
    ("telur",          "egg",                "Makanan",   "Telur dadar untuk sarapan.",         "Omelet for breakfast."),

    # ── TEMPAT ──
    ("rumah",          "house / home",       "Tempat",    "Rumah saya dekat sekolah.",          "My house is near the school."),
    ("sekolah",        "school",             "Tempat",    "Saya pergi ke sekolah setiap hari.", "I go to school every day."),
    ("pasar",          "market",             "Tempat",    "Ibu belanja di pasar pagi.",         "Mother shops at the morning market."),
    ("rumah sakit",    "hospital",           "Tempat",    "Dia dirawat di rumah sakit.",        "He is treated in the hospital."),
    ("kantor",         "office",             "Tempat",    "Ayah bekerja di kantor.",            "Father works at the office."),
    ("bank",           "bank",               "Tempat",    "Saya menabung di bank.",             "I save money at the bank."),
    ("masjid",         "mosque",             "Tempat",    "Masjid itu sangat besar.",           "That mosque is very big."),
    ("gereja",         "church",             "Tempat",    "Gereja itu bersejarah.",             "That church is historic."),
    ("jalan",          "road / street",      "Tempat",    "Jalan ini macet sekali.",            "This road is very congested."),
    ("taman",          "park / garden",      "Tempat",    "Anak-anak bermain di taman.",        "Children play in the park."),
    ("pantai",         "beach",              "Tempat",    "Pantai Bali sangat indah.",          "Bali beach is very beautiful."),
    ("gunung",         "mountain",           "Tempat",    "Gunung Rinjani sangat tinggi.",      "Mount Rinjani is very high."),
    ("bandara",        "airport",            "Tempat",    "Pesawat mendarat di bandara.",       "The plane lands at the airport."),
    ("stasiun",        "station",            "Tempat",    "Stasiun kereta api itu ramai.",      "The train station is crowded."),
    ("hotel",          "hotel",              "Tempat",    "Hotel itu mewah sekali.",            "That hotel is very luxurious."),
    ("perpustakaan",   "library",            "Tempat",    "Perpustakaan tempat membaca.",       "Library is a place for reading."),
    ("toko",           "store / shop",       "Tempat",    "Toko itu menjual baju murah.",       "That store sells cheap clothes."),

    # ── PEKERJAAN ──
    ("dokter",         "doctor",             "Pekerjaan", "Dokter itu sangat ramah.",           "That doctor is very friendly."),
    ("guru",           "teacher",            "Pekerjaan", "Guru mengajar dengan sabar.",        "The teacher teaches patiently."),
    ("polisi",         "police",             "Pekerjaan", "Polisi menjaga keamanan.",           "Police maintain security."),
    ("tentara",        "soldier / army",     "Pekerjaan", "Tentara melindungi negara.",         "Soldiers protect the country."),
    ("petani",         "farmer",             "Pekerjaan", "Petani menanam padi.",               "Farmers plant rice."),
    ("nelayan",        "fisherman",          "Pekerjaan", "Nelayan pergi melaut pagi-pagi.",    "Fishermen go to sea early morning."),
    ("pedagang",       "merchant / trader",  "Pekerjaan", "Pedagang itu ramah sekali.",         "That merchant is very friendly."),
    ("koki",           "chef / cook",        "Pekerjaan", "Koki itu memasak dengan baik.",      "That chef cooks very well."),
    ("pilot",          "pilot",              "Pekerjaan", "Pilot menerbangkan pesawat.",        "The pilot flies the plane."),
    ("insinyur",       "engineer",           "Pekerjaan", "Insinyur merancang jembatan.",       "Engineers design bridges."),
    ("programmer",     "programmer",         "Pekerjaan", "Programmer membuat aplikasi.",       "Programmers create applications."),
    ("mahasiswa",      "university student", "Pekerjaan", "Mahasiswa belajar di kampus.",       "University students study on campus."),
    ("pelajar",        "student",            "Pekerjaan", "Pelajar itu rajin belajar.",         "That student studies diligently."),

    # ── SIFAT & PERASAAN ──
    ("senang",         "happy / glad",       "Perasaan",  "Saya senang bertemu kamu.",          "I am happy to meet you."),
    ("sedih",          "sad",                "Perasaan",  "Dia sedih karena kehilangan.",       "He is sad because of the loss."),
    ("marah",          "angry",              "Perasaan",  "Jangan membuat dia marah.",          "Don't make him angry."),
    ("takut",          "afraid / scared",    "Perasaan",  "Saya takut gelap.",                  "I am afraid of the dark."),
    ("bosan",          "bored",              "Perasaan",  "Saya bosan di rumah terus.",         "I am bored staying home."),
    ("lelah",          "tired",              "Perasaan",  "Saya sangat lelah hari ini.",        "I am very tired today."),
    ("kaget",          "surprised / shocked","Perasaan",  "Saya kaget mendengar berita itu.",   "I was shocked to hear that news."),
    ("malu",           "shy / embarrassed",  "Perasaan",  "Dia malu berbicara di depan umum.",  "He is shy to speak in public."),
    ("khawatir",       "worried",            "Perasaan",  "Ibu khawatir karena saya terlambat.","Mother is worried because I am late."),
    ("bahagia",        "happy / blissful",   "Perasaan",  "Saya bahagia bersama keluarga.",     "I am happy with my family."),
    ("rindu",          "miss / longing",     "Perasaan",  "Saya rindu kampung halaman.",        "I miss my hometown."),
    ("cinta",          "love",               "Perasaan",  "Cinta itu indah.",                   "Love is beautiful."),
    ("benci",          "hate",               "Perasaan",  "Jangan benci siapapun.",             "Don't hate anyone."),

    # ── SIFAT BENDA ──
    ("besar",          "big / large",        "Sifat",     "Gajah adalah hewan yang besar.",     "Elephant is a large animal."),
    ("kecil",          "small / little",     "Sifat",     "Semut sangat kecil.",                "Ants are very small."),
    ("panjang",        "long",               "Sifat",     "Sungai Nil sangat panjang.",         "The Nile River is very long."),
    ("pendek",         "short",              "Sifat",     "Dia bertubuh pendek.",               "He has a short stature."),
    ("tinggi",         "tall / high",        "Sifat",     "Gedung itu sangat tinggi.",          "That building is very tall."),
    ("berat",          "heavy",              "Sifat",     "Batu itu sangat berat.",             "That rock is very heavy."),
    ("ringan",         "light",              "Sifat",     "Kapas sangat ringan.",               "Cotton is very light."),
    ("cepat",          "fast / quick",       "Sifat",     "Cheetah berlari sangat cepat.",      "Cheetah runs very fast."),
    ("lambat",         "slow",               "Sifat",     "Kura-kura berjalan sangat lambat.",  "Turtles walk very slowly."),
    ("panas",          "hot",                "Sifat",     "Cuaca hari ini sangat panas.",       "The weather today is very hot."),
    ("dingin",         "cold",               "Sifat",     "Air dari kulkas sangat dingin.",     "Water from the fridge is very cold."),
    ("baru",           "new",                "Sifat",     "Saya beli HP baru.",                 "I bought a new phone."),
    ("lama",           "old / long time",    "Sifat",     "Gedung itu sudah sangat lama.",      "That building is very old."),
    ("indah",          "beautiful",          "Sifat",     "Pemandangan itu sangat indah.",      "That view is very beautiful."),
    ("jelek",          "ugly / bad",         "Sifat",     "Cuaca jelek hari ini.",              "Bad weather today."),
    ("murah",          "cheap",              "Sifat",     "Harga itu sangat murah.",            "That price is very cheap."),
    ("mahal",          "expensive",          "Sifat",     "Rumah di kota sangat mahal.",        "Houses in the city are very expensive."),
    ("mudah",          "easy",               "Sifat",     "Soal ini mudah sekali.",             "This problem is very easy."),
    ("sulit",          "difficult / hard",   "Sifat",     "Matematika sangat sulit.",           "Mathematics is very difficult."),
    ("pintar",         "smart / clever",     "Sifat",     "Dia murid yang pintar.",             "He is a smart student."),
    ("bodoh",          "stupid / foolish",   "Sifat",     "Jangan merasa bodoh, terus belajar.","Don't feel stupid, keep learning."),
    ("rajin",          "diligent / hardworking","Sifat",  "Siswa yang rajin pasti sukses.",     "A diligent student will succeed."),
    ("malas",          "lazy",               "Sifat",     "Jangan malas belajar.",              "Don't be lazy to study."),

    # ── KATA KERJA ──
    ("pergi",          "go",                 "Kata Kerja","Saya pergi ke sekolah.",             "I go to school."),
    ("datang",         "come",               "Kata Kerja","Kapan kamu datang?",                 "When will you come?"),
    ("pulang",         "go home / return",   "Kata Kerja","Saya pulang jam 5 sore.",            "I go home at 5 PM."),
    ("tidur",          "sleep",              "Kata Kerja","Saya tidur jam 10 malam.",           "I sleep at 10 PM."),
    ("bangun",         "wake up / stand up", "Kata Kerja","Saya bangun jam 5 pagi.",            "I wake up at 5 AM."),
    ("belajar",        "study / learn",      "Kata Kerja","Ayo belajar bersama!",               "Let's study together!"),
    ("bekerja",        "work",               "Kata Kerja","Ayah bekerja keras setiap hari.",    "Father works hard every day."),
    ("bermain",        "play",               "Kata Kerja","Anak-anak bermain di lapangan.",     "Children play in the field."),
    ("berlari",        "run",                "Kata Kerja","Saya berlari setiap pagi.",           "I run every morning."),
    ("berjalan",       "walk",               "Kata Kerja","Kami berjalan ke pasar.",            "We walk to the market."),
    ("membaca",        "read",               "Kata Kerja","Saya suka membaca buku.",            "I like reading books."),
    ("menulis",        "write",              "Kata Kerja","Dia menulis surat untuk temannya.",  "He writes a letter to his friend."),
    ("berbicara",      "speak / talk",       "Kata Kerja","Tolong berbicara lebih pelan.",      "Please speak more slowly."),
    ("mendengar",      "listen / hear",      "Kata Kerja","Dengarkan baik-baik.",               "Listen carefully."),
    ("melihat",        "see / look",         "Kata Kerja","Saya melihat bintang di malam hari.","I see stars at night."),
    ("mencari",        "search / look for",  "Kata Kerja","Saya mencari kunci saya.",           "I am looking for my key."),
    ("menemukan",      "find",               "Kata Kerja","Saya menemukan dompet di jalan.",    "I found a wallet on the road."),
    ("membeli",        "buy",                "Kata Kerja","Ibu membeli sayur di pasar.",        "Mother buys vegetables at the market."),
    ("menjual",        "sell",               "Kata Kerja","Dia menjual rumahnya.",              "He sells his house."),
    ("memberi",        "give",               "Kata Kerja","Dia memberi saya hadiah.",           "He gives me a gift."),
    ("mengambil",      "take",               "Kata Kerja","Ambil buku itu untukku.",            "Take that book for me."),
    ("membantu",       "help",               "Kata Kerja","Tolong bantu saya.",                 "Please help me."),
    ("berpikir",       "think",              "Kata Kerja","Berpikir sebelum bertindak.",        "Think before acting."),
    ("mengerti",       "understand",         "Kata Kerja","Apakah kamu mengerti?",              "Do you understand?"),
    ("lupa",           "forget",             "Kata Kerja","Maaf, saya lupa.",                   "Sorry, I forgot."),
    ("ingat",          "remember",           "Kata Kerja","Ingat janjimu!",                     "Remember your promise!"),
    ("mencintai",      "love",               "Kata Kerja","Saya mencintai keluarga saya.",      "I love my family."),
    ("membenci",       "hate",               "Kata Kerja","Jangan membenci siapapun.",          "Don't hate anyone."),
    ("tertawa",        "laugh",              "Kata Kerja","Mereka tertawa bersama.",            "They laugh together."),
    ("menangis",       "cry",                "Kata Kerja","Bayi itu menangis keras.",           "The baby cries loudly."),
    ("menyanyi",       "sing",               "Kata Kerja","Dia menyanyi dengan merdu.",         "She sings melodiously."),
    ("menari",         "dance",              "Kata Kerja","Mereka menari di pesta.",            "They dance at the party."),
    ("memasak",        "cook",               "Kata Kerja","Ibu memasak rendang hari ini.",      "Mother cooks rendang today."),
    ("mengemudi",      "drive",              "Kata Kerja","Ayah mengemudi dengan hati-hati.",   "Father drives carefully."),
    ("terbang",        "fly",                "Kata Kerja","Burung terbang di langit.",          "Birds fly in the sky."),
    ("berenang",       "swim",               "Kata Kerja","Saya berenang setiap minggu.",       "I swim every week."),
    ("menunggu",       "wait",               "Kata Kerja","Tolong tunggu sebentar.",            "Please wait a moment."),
    ("bertanya",       "ask",                "Kata Kerja","Jangan takut bertanya.",             "Don't be afraid to ask."),
    ("menjawab",       "answer",             "Kata Kerja","Dia menjawab dengan benar.",         "He answers correctly."),

    # ── ALAM ──
    ("matahari",       "sun",                "Alam",      "Matahari terbit di timur.",          "The sun rises in the east."),
    ("bulan",          "moon",               "Alam",      "Bulan purnama sangat indah.",        "The full moon is very beautiful."),
    ("bintang",        "star",               "Alam",      "Bintang berkelip di malam hari.",    "Stars twinkle at night."),
    ("langit",         "sky",                "Alam",      "Langit biru sangat cerah.",          "The blue sky is very clear."),
    ("awan",           "cloud",              "Alam",      "Awan hitam pertanda hujan.",         "Dark clouds signal rain."),
    ("hujan",          "rain",               "Alam",      "Hujan deras sejak tadi pagi.",       "It has been raining heavily since morning."),
    ("angin",          "wind",               "Alam",      "Angin sepoi-sepoi terasa sejuk.",    "The gentle breeze feels cool."),
    ("laut",           "sea / ocean",        "Alam",      "Laut Indonesia sangat luas.",        "Indonesian sea is very vast."),
    ("sungai",         "river",              "Alam",      "Anak bermain di sungai.",            "Children play in the river."),
    ("hutan",          "forest",             "Alam",      "Hutan Indonesia sangat lebat.",      "Indonesian forest is very dense."),
    ("api",            "fire",               "Alam",      "Jangan bermain api.",                "Don't play with fire."),
    ("tanah",          "soil / ground / earth","Alam",    "Tanah ini subur sekali.",            "This soil is very fertile."),
    ("batu",           "rock / stone",       "Alam",      "Batu itu sangat keras.",             "That rock is very hard."),
    ("pohon",          "tree",               "Alam",      "Pohon itu sangat rindang.",          "That tree is very shady."),
    ("bunga",          "flower",             "Alam",      "Bunga mawar sangat harum.",          "Roses smell very fragrant."),
    ("rumput",         "grass",              "Alam",      "Rumput halaman berwarna hijau.",     "The yard grass is green."),

    # ── TEKNOLOGI ──
    ("komputer",       "computer",           "Teknologi", "Komputer saya sangat cepat.",        "My computer is very fast."),
    ("telepon",        "phone / telephone",  "Teknologi", "Telepon saya rusak.",                "My phone is broken."),
    ("internet",       "internet",           "Teknologi", "Internet sangat penting sekarang.",  "Internet is very important now."),
    ("aplikasi",       "application / app",  "Teknologi", "Aplikasi ini sangat berguna.",       "This application is very useful."),
    ("kata sandi",     "password",           "Teknologi", "Jaga kata sandi dengan baik.",       "Keep your password safe."),
    ("unduh",          "download",           "Teknologi", "Unduh filenya dulu.",                "Download the file first."),
    ("unggah",         "upload",             "Teknologi", "Unggah foto ke media sosial.",       "Upload photos to social media."),
    ("layar",          "screen",             "Teknologi", "Layar HP saya retak.",               "My phone screen is cracked."),
    ("baterai",        "battery",            "Teknologi", "Baterai HP saya hampir habis.",      "My phone battery is almost dead."),
    ("kamera",         "camera",             "Teknologi", "Kamera ini resolusinya tinggi.",     "This camera has high resolution."),
    ("printer",        "printer",            "Teknologi", "Printer itu rusak.",                 "That printer is broken."),
    ("jaringan",       "network",            "Teknologi", "Jaringan internet lemah.",           "The internet network is weak."),
    ("pesan",          "message",            "Teknologi", "Kirim pesan ke saya.",               "Send me a message."),
    ("email",          "email",              "Teknologi", "Cek email kamu.",                    "Check your email."),

    # ── KESEHATAN ──
    ("sakit",          "sick / pain",        "Kesehatan", "Saya sakit kepala hari ini.",        "I have a headache today."),
    ("sehat",          "healthy",            "Kesehatan", "Makan sayur agar sehat.",            "Eat vegetables to be healthy."),
    ("obat",           "medicine",           "Kesehatan", "Minum obat setelah makan.",          "Take medicine after eating."),
    ("demam",          "fever",              "Kesehatan", "Anak itu demam tinggi.",             "That child has a high fever."),
    ("batuk",          "cough",              "Kesehatan", "Saya batuk sejak kemarin.",          "I have been coughing since yesterday."),
    ("pilek",          "cold / runny nose",  "Kesehatan", "Cuaca dingin bikin pilek.",          "Cold weather causes a cold."),
    ("pusing",         "dizzy",              "Kesehatan", "Kepala saya pusing sekali.",         "My head is very dizzy."),
    ("lelah",          "tired / exhausted",  "Kesehatan", "Saya kelelahan setelah olahraga.",   "I am exhausted after exercise."),
    ("olahraga",       "exercise / sport",   "Kesehatan", "Olahraga teratur itu sehat.",        "Regular exercise is healthy."),
    ("istirahat",      "rest",               "Kesehatan", "Istirahat yang cukup itu penting.",  "Adequate rest is important."),
    ("tidur",          "sleep",              "Kesehatan", "Tidur 8 jam sehari sangat baik.",    "Sleeping 8 hours a day is very good."),

    # ── PENDIDIKAN ──
    ("buku",           "book",               "Pendidikan","Buku adalah jendela dunia.",         "Books are windows to the world."),
    ("pena",           "pen",                "Pendidikan","Pena saya kehabisan tinta.",         "My pen ran out of ink."),
    ("pensil",         "pencil",             "Pendidikan","Gambar dengan pensil dulu.",         "Draw with pencil first."),
    ("kelas",          "class / classroom",  "Pendidikan","Kelas kami sangat bersih.",          "Our classroom is very clean."),
    ("ujian",          "exam / test",        "Pendidikan","Ujian besok sangat sulit.",          "Tomorrow's exam is very difficult."),
    ("nilai",          "grade / score",      "Pendidikan","Nilainya sangat bagus.",             "His grade is very good."),
    ("pintar",         "smart / intelligent","Pendidikan","Dia sangat pintar di matematika.",   "He is very smart in mathematics."),
    ("ilmu",           "knowledge / science","Pendidikan","Ilmu pengetahuan sangat penting.",   "Knowledge is very important."),
    ("universitas",    "university",         "Pendidikan","Dia kuliah di universitas ternama.", "He studies at a famous university."),
    ("diploma",        "diploma",            "Pendidikan","Dia mendapat diploma teknik.",       "He received a diploma in engineering."),
]

# ─── UTILS ────────────────────────────────────────────────────────────────────

def get_categories():
    cats = []
    seen = set()
    for entry in KAMUS:
        cat = entry[2]
        if cat not in seen:
            cats.append(cat)
            seen.add(cat)
    return cats

def build_flat(query="", direction="id_en", cat_filter="Semua"):
    flat = []
    q = query.lower().strip()
    for entry in KAMUS:
        id_word, en_word, cat, ex_id, ex_en = entry
        if cat_filter != "Semua" and cat != cat_filter:
            continue
        if direction == "id_en":
            word   = id_word
            transl = en_word
        else:
            word   = en_word
            transl = id_word
        if q and q not in word.lower() and q not in transl.lower():
            continue
        flat.append({
            "word":   word,
            "transl": transl,
            "cat":    cat,
            "ex_id":  ex_id,
            "ex_en":  ex_en,
            "dir":    direction,
        })
    return flat

# ─── TRANSLATOR ONLINE ────────────────────────────────────────────────────────

def translate_text(text, src, tgt):
    """Terjemahkan teks via Google Translate (deep-translator)."""
    if not HAS_TRANSLATOR:
        return None, "deep-translator tidak terinstall.\nJalankan: pip install deep-translator"
    try:
        result = GoogleTranslator(source=src, target=tgt).translate(text)
        return result, None
    except Exception as e:
        return None, str(e)

def show_translator(stdscr):
    """Layar translator kalimat panjang."""
    curses.curs_set(1)
    direction  = "id_en"   # id_en atau en_id
    input_text = ""
    result     = ""
    error_msg  = ""
    translating = False
    char_count  = 0

    while True:
        h, w = stdscr.getmaxyx()
        stdscr.erase()

        src_lang = "ID" if direction == "id_en" else "EN"
        tgt_lang = "EN" if direction == "id_en" else "ID"
        src_code = "id"  if direction == "id_en" else "en"
        tgt_code = "en"  if direction == "id_en" else "id"

        # Header
        stdscr.attron(curses.color_pair(15) | curses.A_BOLD)
        stdscr.addstr(0, 0, f" 🌐 TRANSLATOR KALIMAT  [{src_lang} → {tgt_lang}] ".ljust(w - 1))
        stdscr.attroff(curses.color_pair(15) | curses.A_BOLD)

        # Info
        if not HAS_TRANSLATOR:
            stdscr.attron(curses.color_pair(16) | curses.A_BOLD)
            stdscr.addstr(1, 2, "pip install deep-translator")
            stdscr.attroff(curses.color_pair(16) | curses.A_BOLD)
        else:
            stdscr.attron(curses.color_pair(13))
            stdscr.addstr(1, 2, "Butuh koneksi internet. Tab=Balik Arah  Enter=Terjemah  Esc=Kembali")
            stdscr.attroff(curses.color_pair(13))

        # Separator
        stdscr.attron(curses.color_pair(15))
        stdscr.addstr(2, 0, "─" * min(w - 1, 80))
        stdscr.attroff(curses.color_pair(15))

        # Label input
        stdscr.attron(curses.color_pair(16) | curses.A_BOLD)
        stdscr.addstr(3, 2, f"INPUT ({src_lang}):")
        stdscr.attroff(curses.color_pair(16) | curses.A_BOLD)

        # Kotak input — word wrap
        input_rows = []
        if input_text:
            words = input_text.split(' ')
            line  = ""
            for word in words:
                if len(line) + len(word) + 1 > w - 6:
                    input_rows.append(line)
                    line = word
                else:
                    line = (line + " " + word).strip()
            if line:
                input_rows.append(line)
        if not input_rows:
            input_rows = [""]

        box_h = max(3, len(input_rows) + 1)
        for bi in range(box_h):
            line_str = input_rows[bi] if bi < len(input_rows) else ""
            stdscr.attron(curses.color_pair(13))
            stdscr.addstr(4 + bi, 2, f"│ {line_str:<{w-6}} │"[:w-1])
            stdscr.attroff(curses.color_pair(13))

        # Jumlah karakter input
        char_count = len(input_text)
        stdscr.attron(curses.color_pair(16))
        stdscr.addstr(4 + box_h, 2, f"{char_count} karakter")
        stdscr.attroff(curses.color_pair(16))

        result_start = 4 + box_h + 2

        # Separator tengah
        stdscr.attron(curses.color_pair(15))
        stdscr.addstr(result_start - 1, 0, "─" * min(w - 1, 80))
        stdscr.attroff(curses.color_pair(15))

        # Label hasil
        stdscr.attron(curses.color_pair(17) | curses.A_BOLD)
        stdscr.addstr(result_start, 2, f"HASIL ({tgt_lang}):")
        stdscr.attroff(curses.color_pair(17) | curses.A_BOLD)

        if translating:
            stdscr.attron(curses.color_pair(16) | curses.A_BOLD)
            stdscr.addstr(result_start + 1, 4, "Menerjemahkan...")
            stdscr.attroff(curses.color_pair(16) | curses.A_BOLD)
        elif error_msg:
            stdscr.attron(curses.color_pair(12))
            for i, ln in enumerate(error_msg.split('\n')):
                if result_start + 1 + i < h - 2:
                    stdscr.addstr(result_start + 1 + i, 4, ln[:w - 6])
            stdscr.attroff(curses.color_pair(12))
        elif result:
            # Word wrap hasil
            result_words = result.split(' ')
            rlines, rline = [], ""
            for word in result_words:
                if len(rline) + len(word) + 1 > w - 6:
                    rlines.append(rline)
                    rline = word
                else:
                    rline = (rline + " " + word).strip()
            if rline:
                rlines.append(rline)
            for i, ln in enumerate(rlines):
                if result_start + 1 + i < h - 2:
                    stdscr.attron(curses.color_pair(17) | curses.A_BOLD)
                    stdscr.addstr(result_start + 1 + i, 4, ln[:w - 6])
                    stdscr.attroff(curses.color_pair(17) | curses.A_BOLD)
            # Jumlah karakter hasil
            res_row = result_start + 1 + len(rlines)
            if res_row < h - 2:
                stdscr.attron(curses.color_pair(16))
                stdscr.addstr(res_row, 4, f"{len(result)} karakter")
                stdscr.attroff(curses.color_pair(16))
        else:
            stdscr.attron(curses.color_pair(13))
            stdscr.addstr(result_start + 1, 4, "Ketik kalimat di atas lalu tekan Enter...")
            stdscr.attroff(curses.color_pair(13))

        # Footer
        stdscr.attron(curses.color_pair(15))
        stdscr.addstr(h - 1, 0,
            " [Enter] Terjemah  [Tab] Balik Arah  [Esc] Kembali ke Kamus "[:w - 1])
        stdscr.attroff(curses.color_pair(15))

        # Posisi kursor di akhir input
        cur_row = 4 + min(len(input_rows) - 1, box_h - 1)
        cur_col = min(len(input_rows[-1]) + 4, w - 3)
        try:
            stdscr.move(cur_row, cur_col)
        except:
            pass

        stdscr.refresh()
        key = stdscr.getch()

        if key == 27:  # Esc — kembali ke kamus
            break
        elif key == 9:  # Tab — balik arah
            direction = "en_id" if direction == "id_en" else "id_en"
            result    = ""
            error_msg = ""
        elif key in (10, 13):  # Enter — terjemah
            if input_text.strip():
                result     = ""
                error_msg  = ""
                translating = True
                stdscr.refresh()

                # Jalankan di thread agar tidak freeze
                res_holder = [None, None]
                def do_translate():
                    res_holder[0], res_holder[1] = translate_text(
                        input_text.strip(), src_code, tgt_code)
                t = threading.Thread(target=do_translate)
                t.start()
                t.join(timeout=15)

                translating = False
                result    = res_holder[0] or ""
                error_msg = res_holder[1] or ""
        elif key in (curses.KEY_BACKSPACE, 127, 8):
            input_text = input_text[:-1]
            result     = ""
            error_msg  = ""
        elif 32 <= key <= 126:
            input_text += chr(key)
            result      = ""
            error_msg   = ""

    curses.curs_set(0)

# ─── WARNA ────────────────────────────────────────────────────────────────────

CAT_COLORS_MAP = {}

def get_cat_color(cat, cats):
    colors = [
        curses.COLOR_CYAN, curses.COLOR_GREEN, curses.COLOR_YELLOW,
        curses.COLOR_MAGENTA, curses.COLOR_RED, curses.COLOR_BLUE,
        curses.COLOR_CYAN, curses.COLOR_GREEN, curses.COLOR_YELLOW,
        curses.COLOR_MAGENTA, curses.COLOR_RED, curses.COLOR_BLUE,
    ]
    idx = cats.index(cat) if cat in cats else 0
    return (idx % len(colors)) + 1

# ─── DETAIL VIEW ─────────────────────────────────────────────────────────────

def show_detail(stdscr, item, cats):
    cp = get_cat_color(item["cat"], cats)
    while True:
        h, w = stdscr.getmaxyx()
        stdscr.erase()

        # Header
        stdscr.attron(curses.color_pair(15) | curses.A_BOLD)
        stdscr.addstr(0, 0, " 📖 DETAIL KATA ".ljust(w - 1))
        stdscr.attroff(curses.color_pair(15) | curses.A_BOLD)

        # Kategori
        stdscr.attron(curses.color_pair(cp) | curses.A_BOLD)
        stdscr.addstr(2, 2, f"[ {item['cat']} ]")
        stdscr.attroff(curses.color_pair(cp) | curses.A_BOLD)

        # Kata utama
        stdscr.attron(curses.color_pair(cp) | curses.A_BOLD)
        stdscr.addstr(4, 2, "KATA:")
        stdscr.attroff(curses.color_pair(cp) | curses.A_BOLD)
        stdscr.attron(curses.color_pair(13) | curses.A_BOLD)
        stdscr.addstr(5, 4, item["word"][:w - 6])
        stdscr.attroff(curses.color_pair(13) | curses.A_BOLD)
        stdscr.attron(curses.color_pair(16))
        stdscr.addstr(6, 4, f"{len(item['word'])} karakter")
        stdscr.attroff(curses.color_pair(16))

        # Terjemahan
        stdscr.attron(curses.color_pair(cp) | curses.A_BOLD)
        stdscr.addstr(8, 2, "TERJEMAHAN:")
        stdscr.attroff(curses.color_pair(cp) | curses.A_BOLD)
        stdscr.attron(curses.color_pair(17) | curses.A_BOLD)
        stdscr.addstr(9, 4, item["transl"][:w - 6])
        stdscr.attroff(curses.color_pair(17) | curses.A_BOLD)
        stdscr.attron(curses.color_pair(16))
        stdscr.addstr(10, 4, f"{len(item['transl'])} karakter")
        stdscr.attroff(curses.color_pair(16))

        # Separator
        stdscr.attron(curses.color_pair(cp))
        stdscr.addstr(12, 2, "─" * min(w - 4, 50))
        stdscr.attroff(curses.color_pair(cp))

        # Contoh kalimat Indonesia
        stdscr.attron(curses.color_pair(16) | curses.A_BOLD)
        stdscr.addstr(13, 2, "CONTOH (Indonesia):")
        stdscr.attroff(curses.color_pair(16) | curses.A_BOLD)

        # Word wrap contoh
        def wrap(text, width):
            words = text.split()
            lines, line = [], ""
            for word in words:
                if len(line) + len(word) + 1 > width:
                    lines.append(line)
                    line = word
                else:
                    line = (line + " " + word).strip()
            if line:
                lines.append(line)
            return lines

        id_lines = wrap(item["ex_id"], w - 8)
        for i, ln in enumerate(id_lines):
            if 14 + i < h - 6:
                stdscr.attron(curses.color_pair(13))
                stdscr.addstr(14 + i, 4, ln)
                stdscr.attroff(curses.color_pair(13))

        en_start = 14 + len(id_lines) + 1

        # Contoh kalimat Inggris
        if en_start < h - 5:
            stdscr.attron(curses.color_pair(16) | curses.A_BOLD)
            stdscr.addstr(en_start, 2, "CONTOH (English):")
            stdscr.attroff(curses.color_pair(16) | curses.A_BOLD)

            en_lines = wrap(item["ex_en"], w - 8)
            for i, ln in enumerate(en_lines):
                if en_start + 1 + i < h - 3:
                    stdscr.attron(curses.color_pair(17))
                    stdscr.addstr(en_start + 1 + i, 4, ln)
                    stdscr.attroff(curses.color_pair(17))

        # Footer
        stdscr.attron(curses.color_pair(15))
        stdscr.addstr(h - 1, 0, " [Esc / k / ←] Kembali ".ljust(w - 1))
        stdscr.attroff(curses.color_pair(15))

        stdscr.refresh()
        key = stdscr.getch()
        if key in (27, ord('k'), ord('K'), curses.KEY_LEFT, curses.KEY_BACKSPACE):
            break

# ─── MAIN ─────────────────────────────────────────────────────────────────────

def main(stdscr):
    curses.curs_set(0)
    curses.start_color()
    curses.use_default_colors()

    cats = get_categories()
    colors = [
        curses.COLOR_CYAN, curses.COLOR_GREEN, curses.COLOR_YELLOW,
        curses.COLOR_MAGENTA, curses.COLOR_RED, curses.COLOR_BLUE,
        curses.COLOR_CYAN, curses.COLOR_GREEN, curses.COLOR_YELLOW,
        curses.COLOR_MAGENTA, curses.COLOR_RED, curses.COLOR_BLUE,
    ]
    for i, col in enumerate(colors, 1):
        curses.init_pair(i, col, -1)
    curses.init_pair(13, curses.COLOR_WHITE,   -1)
    curses.init_pair(14, curses.COLOR_BLACK,   curses.COLOR_CYAN)
    curses.init_pair(15, curses.COLOR_CYAN,    -1)
    curses.init_pair(16, curses.COLOR_YELLOW,  -1)
    curses.init_pair(17, curses.COLOR_GREEN,   -1)
    curses.init_pair(18, curses.COLOR_BLACK,   curses.COLOR_WHITE)

    state = {
        "query":       "",
        "search_mode": False,
        "offset":      0,
        "cursor":      0,
        "direction":   "id_en",   # id_en atau en_id
        "cat_filter":  "Semua",
    }

    while True:
        flat = build_flat(state["query"], state["direction"], state["cat_filter"])
        h, w = stdscr.getmaxyx()
        stdscr.erase()

        # ── Header ──
        dir_label = "ID → EN" if state["direction"] == "id_en" else "EN → ID"
        header = f" 📖 KAMUS INDONESIA-INGGRIS  [{dir_label}] "
        stdscr.attron(curses.color_pair(15) | curses.A_BOLD)
        stdscr.addstr(0, 0, header[:w - 1].ljust(w - 1))
        stdscr.attroff(curses.color_pair(15) | curses.A_BOLD)

        # ── Search bar ──
        if state["search_mode"]:
            stdscr.attron(curses.color_pair(18) | curses.A_BOLD)
        else:
            stdscr.attron(curses.color_pair(13))
        search_str = f" 🔍 Cari: {state['query']}" + ("█" if state["search_mode"] else "")
        stdscr.addstr(1, 0, search_str[:w - 1].ljust(w - 1))
        if state["search_mode"]:
            stdscr.attroff(curses.color_pair(18) | curses.A_BOLD)
        else:
            stdscr.attroff(curses.color_pair(13))

        # ── Info bar ──
        info = f" {len(flat)} kata  |  ↑↓ Jelajah  |  s Cari  |  t Translator  |  Tab Balik  |  k Keluar "
        stdscr.attron(curses.color_pair(13))
        stdscr.addstr(2, 0, info[:w - 1])
        stdscr.attroff(curses.color_pair(13))

        # ── Separator ──
        stdscr.attron(curses.color_pair(15))
        stdscr.addstr(3, 0, "─" * min(w - 1, 80))
        stdscr.attroff(curses.color_pair(15))

        # ── List ──
        list_top = 4
        list_h   = h - list_top - 2
        n        = len(flat)

        if state["cursor"] >= n and n > 0:   state["cursor"] = n - 1
        if state["cursor"] < 0:              state["cursor"] = 0
        if n > 0:
            if state["cursor"] < state["offset"]:
                state["offset"] = state["cursor"]
            if state["cursor"] >= state["offset"] + list_h:
                state["offset"] = state["cursor"] - list_h + 1

        prev_cat = None
        row = list_top
        for idx in range(state["offset"], min(state["offset"] + list_h, n)):
            item = flat[idx]
            cp   = get_cat_color(item["cat"], cats)

            # Kategori header
            if item["cat"] != prev_cat and row < list_top + list_h:
                stdscr.attron(curses.color_pair(cp) | curses.A_BOLD)
                stdscr.addstr(row, 0, f"  ── {item['cat']} "[:w - 1])
                stdscr.attroff(curses.color_pair(cp) | curses.A_BOLD)
                row += 1
                prev_cat = item["cat"]
                if row >= list_top + list_h:
                    break

            if row >= list_top + list_h:
                break

            is_sel = (idx == state["cursor"])
            if is_sel:
                stdscr.attron(curses.color_pair(14) | curses.A_BOLD)
                line = f"  ▶ {item['word']:<28} {item['transl']}"
                stdscr.addstr(row, 0, line[:w - 1].ljust(min(w - 1, 70)))
                stdscr.attroff(curses.color_pair(14) | curses.A_BOLD)
            else:
                # Kata
                stdscr.attron(curses.color_pair(cp))
                word_part = f"     {item['word']:<28}"[:w - 1]
                stdscr.addstr(row, 0, word_part)
                stdscr.attroff(curses.color_pair(cp))
                # Terjemahan
                stdscr.attron(curses.color_pair(17))
                remaining = w - 1 - len(word_part)
                if remaining > 2:
                    stdscr.addstr(row, len(word_part), item["transl"][:remaining - 1])
                stdscr.attroff(curses.color_pair(17))

            row += 1

        # ── Footer ──
        stdscr.attron(curses.color_pair(15))
        stdscr.addstr(h - 1, 0,
            " [s] Cari  [t] Translator  [Tab] Balik Arah  [Enter] Detail  [k] Keluar "[:w - 1])
        stdscr.attroff(curses.color_pair(15))

        stdscr.refresh()

        # ── Input ──
        key = stdscr.getch()

        if state["search_mode"]:
            if key == 27:
                state["search_mode"] = False
                state["query"]  = ""
                state["cursor"] = 0
                state["offset"] = 0
            elif key in (10, 13):
                state["search_mode"] = False
                state["cursor"] = 0
                state["offset"] = 0
            elif key in (curses.KEY_BACKSPACE, 127, 8):
                state["query"]  = state["query"][:-1]
                state["cursor"] = 0
                state["offset"] = 0
            elif 32 <= key <= 126:
                state["query"] += chr(key)
                state["cursor"] = 0
                state["offset"] = 0
        else:
            if key in (ord('k'), ord('K')):
                return
            elif key == ord('t'):
                show_translator(stdscr)
            elif key == ord('s'):
                state["search_mode"] = True
            elif key == 9:  # Tab — balik arah
                state["direction"] = "en_id" if state["direction"] == "id_en" else "id_en"
                state["cursor"] = 0
                state["offset"] = 0
                state["query"]  = ""
            elif key == 27:
                state["query"]  = ""
                state["cursor"] = 0
                state["offset"] = 0
            elif key == curses.KEY_UP:
                state["cursor"] = max(0, state["cursor"] - 1)
            elif key == curses.KEY_DOWN:
                state["cursor"] = min(n - 1, state["cursor"] + 1)
            elif key == curses.KEY_PPAGE:
                state["cursor"] = max(0, state["cursor"] - list_h)
            elif key == curses.KEY_NPAGE:
                state["cursor"] = min(n - 1, state["cursor"] + list_h)
            elif key == curses.KEY_HOME:
                state["cursor"] = 0
                state["offset"] = 0
            elif key == curses.KEY_END:
                state["cursor"] = n - 1
            elif key in (10, 13) and n > 0:
                show_detail(stdscr, flat[state["cursor"]], cats)

# ─── ENTRY ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)
    print("\n✅ Terima kasih sudah menggunakan Kamus ID-EN!\n")
