
Receptive Skills CAT – Starter Content Pack
==========================================

What’s inside
-------------
- content/grammar|listening|reading/A1..C2.json  → seed items (3 per level)
- media/listening/...                             → placeholder WAVs for testlets
- authoring/grammar.csv, listening.csv, reading.csv → CSV templates
- authoring/build_from_csv.py                     → convert CSVs → JSON banks

How to scale to ~40 items per level
-----------------------------------
1) Open the CSV templates in authoring/ and add your items.
   - Keep 'section' and 'level' consistent.
   - Fill options 0..3 and the correct answer_index (0-based).
   - Use 'tags' (semicolon-separated) to help blueprint quotas (e.g., gist;detail;inference).
   - If you want items excluded from scoring (calibration), set pretest = true.
   - For stable equating items, set anchor = true.

2) Run the builder:
   python authoring/build_from_csv.py authoring content

3) (Optional) Place real MP3/WAV files under media/listening/<level>/ and reference them
   via audio_url in listening.csv (e.g., /media/listening/b2/my_audio.wav).

Notes
-----
- The included WAVs are simple tones (placeholders) so your pipeline runs end-to-end.
- The backend (main.py) expands testlets automatically and hides answer_index from clients.
- IRT defaults follow approximate difficulty per level; adjust irt_b as you calibrate.
