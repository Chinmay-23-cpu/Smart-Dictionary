import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from difflib import get_close_matches
import pyttsx3, random

# Flashcard data
motivational_flashcards = [
    {"word": "serendipity", "meaning": "The occurrence of events by chance in a happy or beneficial way.",
     "quote": "Sometimes you find good things without looking for them."},
    {"word": "resilience", "meaning": "The capacity to recover quickly from difficulties.",
     "quote": "Resilience is not about avoiding the fall, but rising every time you fall."},
    {"word": "optimism", "meaning": "Hopefulness and confidence about the future.",
     "quote": "Keep your face always toward the sunshine—and shadows will fall behind you."},
    {"word": "perseverance", "meaning": "Persistence in doing something despite difficulty.",
     "quote": "It always seems impossible until it's done."},
    {"word": "growth", "meaning": "The process of developing or maturing physically, mentally, or spiritually.",
     "quote": "Strive for progress, not perfection."}
]

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")
engine = pyttsx3.init()

def start_gui():
    root = ctk.CTk()
    root.title("WordWise: The Smart Dictionary")
    root.geometry("800x720")

    lemmatizer, is_dark_mode, bookmarks = WordNetLemmatizer(), [False], []

    def speak(text): engine.say(text); engine.runAndWait()

    def speakWord():
        w = word.get().strip()
        speak(w) if w else messagebox.showinfo("No Word", "Please enter a word to speak.")

    def insert_heading(label, content):
        meaning_box.insert("end", f"{label}\n", "heading")
        meaning_box.insert("end", f"{', '.join(list(content)[:5]) or 'None'}\n\n")

    def getMeaning(word_to_search=None):
        w = (word_to_search or word.get().strip().lower()).replace(" ", "_")
        if not w: return messagebox.showwarning("Input Error", "Please enter a word.")
        w_lookup = lemmatizer.lemmatize(w)
        meanings = wordnet.synsets(w_lookup)

        if not meanings:
            suggestion = get_close_matches(w_lookup, list(wordnet.words()), n=1, cutoff=0.8)
            if suggestion and messagebox.askyesno("Did you mean?", f"Did you mean '{suggestion[0]}' instead?"):
                word.delete(0, "end"); word.insert(0, suggestion[0]); return getMeaning(suggestion[0])
            return messagebox.showinfo("⚠ Not Found", f"No meaning found for '{w}'.")

        m, pos_map = meanings[0], {'n': 'Noun', 'v': 'Verb', 'a': 'Adjective', 's': 'Adjective Satellite', 'r': 'Adverb'}
        example = m.examples()[0] if m.examples() else "No example found."
        synonyms = {lemma.name().replace('_', ' ') for syn in meanings for lemma in syn.lemmas()}
        antonyms = {a.name().replace('_', ' ') for syn in meanings for lemma in syn.lemmas() for a in lemma.antonyms()}

        meaning_box.configure(state="normal")
        meaning_box.delete("1.0", "end")
        meaning_box.insert("end", f"{m.definition()} ({pos_map.get(m.pos(), m.pos())})\n\n")
        for label, content in [("🟢 SYNONYMS:", synonyms), ("🔴 ANTONYMS:", antonyms), ("💬 EXAMPLE:", [example])]:
            insert_heading(label, content)
        meaning_box.tag_configure("heading", font=("Segoe UI Black", 16, "bold"))
        meaning_box.configure(state="disabled")

    def clearAll():
        word.delete(0, "end")
        meaning_box.configure(state="normal"); meaning_box.delete("1.0", "end"); meaning_box.configure(state="disabled")

    def toggleTheme():
        is_dark_mode[0] = not is_dark_mode[0]
        ctk.set_appearance_mode("dark" if is_dark_mode[0] else "light")

    def bookmarkWordEntry(w):
        if w not in bookmarks:
            bookmarks.append(w); messagebox.showinfo("Bookmarked", f"'{w}' added to bookmarks.")
        else:
            messagebox.showinfo("Already Bookmarked", f"'{w}' is already bookmarked.")

    def bookmarkWord():
        w = word.get().strip()
        if w: bookmarkWordEntry(w)
        else: messagebox.showwarning("No Word", "Enter a word to bookmark.")

    def viewBookmarks():
        if not bookmarks: return messagebox.showinfo("📚 Bookmarked Words", "No bookmarks yet.")
        popup = ctk.CTkToplevel(root); popup.title("📚 Bookmarked Words"); popup.geometry("450x450"); popup.grab_set()
        ctk.CTkLabel(popup, text="Your Bookmarks", font=("Segoe UI Black", 20)).pack(pady=(15, 5))
        list_frame = ctk.CTkScrollableFrame(popup, width=420, height=320, corner_radius=15, border_width=2)
        list_frame.pack(pady=10, padx=10)

        def refresh():
            for w in list_frame.winfo_children(): w.destroy()
            for bw in bookmarks:
                row = ctk.CTkFrame(list_frame, fg_color="transparent"); row.pack(pady=4, padx=5, fill="x")
                ctk.CTkLabel(row, text=bw, font=("Segoe UI", 15), width=160, anchor="w").pack(side="left", padx=(5, 10))
                btn_frame = ctk.CTkFrame(row, fg_color="transparent"); btn_frame.pack(side="left", padx=5)
                ctk.CTkButton(btn_frame, text="🔍 View", width=70, height=32, font=("Segoe UI", 14),
                    command=lambda w=bw: (word.delete(0, "end"), word.insert(0, w), getMeaning(w))).pack(side="left", padx=(0, 6))
                ctk.CTkButton(btn_frame, text="🗑 Remove", width=90, height=32, font=("Segoe UI", 14),
                    fg_color="#cc3300", hover_color="#a62000",
                    command=lambda w=bw: (bookmarks.remove(w), refresh())).pack(side="left", padx=(0, 6))

        refresh(); ctk.CTkButton(popup, text="Close", command=popup.destroy, width=100).pack(pady=10)

    def show_word_of_day(btn):
        fc = random.choice(motivational_flashcards)
        popup = ctk.CTkToplevel(root); popup.title("🌟 Word of the Day"); popup.geometry("400x350"); popup.grab_set()
        ctk.CTkLabel(popup, text="✨ Word of the Day", font=("Segoe UI Black", 20)).pack(pady=(15, 10))
        ctk.CTkLabel(popup, text=f"📝 {fc['word']}", font=("Segoe UI", 18, "bold")).pack(pady=(5, 5))
        ctk.CTkLabel(popup, text=f"📖 {fc['meaning']}", wraplength=350, font=("Segoe UI", 14)).pack(pady=(0, 10))
        ctk.CTkLabel(popup, text=f"💡 \"{fc['quote']}\"", wraplength=350, font=("Segoe UI Italic", 13)).pack(pady=(0, 15))
        ctk.CTkButton(popup, text="🔖 Bookmark", command=lambda: bookmarkWordEntry(fc['word'])).pack(pady=5)
        ctk.CTkButton(popup, text="Close", command=popup.destroy).pack(pady=(5, 10))
        btn.pack_forget()

    # GUI Layout
    ctk.CTkLabel(root, text="📚 WordWise", font=("Segoe UI Black", 40, "bold")).pack(pady=(25, 0))
    ctk.CTkLabel(root, text="The Smart Dictionary", font=("Segoe UI", 18, "italic")).pack(pady=(0, 15))

    content_frame = ctk.CTkFrame(root, fg_color="transparent")
    content_frame.pack(fill="both", expand=True, padx=20, pady=10)

    left_panel = ctk.CTkFrame(content_frame, fg_color="transparent", width=150)
    left_panel.pack(side="left", fill="y", padx=(0, 15))

    btn_opts = {"corner_radius": 18, "font": ("Segoe UI", 14, "bold"), "border_width": 2, "height": 40, "width": 140}
    buttons = [
        ("🔖 Bookmark", bookmarkWord),
        ("📚 View Bookmarks", viewBookmarks),
        ("🔈 Speak", speakWord),
        ("🩱 Clear", clearAll),
        ("🌙 Theme", toggleTheme)
    ]
    for txt, cmd in buttons:
        kwargs = {"fg_color": "#cc3300", "hover_color": "#a62000"} if "Clear" in txt else {}
        ctk.CTkButton(left_panel, text=txt, command=cmd, **btn_opts, **kwargs).pack(pady=10)

    word_of_day_btn = ctk.CTkButton(left_panel, text="🌟 Word of the Day", command=lambda: show_word_of_day(word_of_day_btn), **btn_opts)
    word_of_day_btn.pack(pady=10)

    divider = ctk.CTkFrame(content_frame, width=2, height=500, fg_color="grey")
    divider.pack(side="left", padx=(0, 10), pady=10, fill="y")

    right_panel = ctk.CTkFrame(content_frame, fg_color="transparent")
    right_panel.pack(side="left", fill="both", expand=True)

    entry_frame = ctk.CTkFrame(right_panel, fg_color="transparent")
    entry_frame.pack(pady=10)

    ctk.CTkLabel(entry_frame, text="🔍 Word:", font=("Segoe UI Semibold", 18)).pack(side="left", padx=(0, 5))
    word = ctk.CTkEntry(entry_frame, font=("Segoe UI", 17), width=320, height=40, corner_radius=18, border_width=2)
    word.pack(side="left", padx=5)
    ctk.CTkButton(entry_frame, text="Search", command=getMeaning, height=38, width=85,
                  font=("Segoe UI", 14, "bold"), corner_radius=15).pack(side="left", padx=5)
    word.bind("<Return>", lambda e: getMeaning())
    word.focus()

    result_card = ctk.CTkScrollableFrame(right_panel, width=580, height=350, corner_radius=20, border_width=2)
    result_card.pack(pady=20)
    global meaning_box
    meaning_box = tk.Text(result_card, font=("Segoe UI", 15), height=20, wrap="word", bd=2, relief="ridge")
    meaning_box.pack(padx=10, pady=10, fill="both", expand=True)
    meaning_box.configure(state="disabled")

    root.mainloop()

start_gui()
