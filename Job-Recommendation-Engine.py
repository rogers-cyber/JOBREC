import threading
import webbrowser
import tkinter as tk
from tkinter import messagebox
from dataclasses import dataclass
from typing import List, Tuple, Dict, Optional
import io
import requests
from PIL import Image, ImageTk

import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap.widgets.scrolled import ScrolledText

# ---------------- CONFIG ---------------- #
RESULTS_PER_PAGE = 6

# ---------------- GLOBAL STATE ---------------- #
all_ranked_jobs: List[Tuple["Job", float]] = []
current_page = 1
logo_cache: Dict[str, ImageTk.PhotoImage] = {}

# ---------------- DATA STRUCTURE ---------------- #
@dataclass
class Job:
    title: str
    company: str
    url: str
    description: str
    skills: List[str]
    location: str
    logo_url: str = ""
    score: float = 0.0

# ---------------- MOCK / FETCH JOBS ---------------- #
def fetch_jobs(query: str) -> List[Job]:
    """
    Fetch jobs matching the query.
    For demo purposes, this uses a static list.
    In real applications, replace this with API calls.
    """
    try:
        jobs_data = [
            Job("Python Developer", "TechCorp", "https://example.com/job1",
                "Develop backend applications using Python.", ["Python", "Django"], "Remote",
                "https://via.placeholder.com/100x100.png?text=TechCorp"),
            Job("Frontend Engineer", "Webify", "https://example.com/job2",
                "Build responsive web apps with React.", ["JavaScript", "React"], "NY, USA",
                "https://via.placeholder.com/100x100.png?text=Webify"),
            Job("Data Scientist", "DataWorks", "https://example.com/job3",
                "Analyze large datasets and build ML models.", ["Python", "ML", "Pandas"], "SF, USA",
                "https://via.placeholder.com/100x100.png?text=DataWorks"),
            Job("Java Developer", "SoftSolutions", "https://example.com/job4",
                "Develop enterprise Java applications.", ["Java", "Spring"], "Remote",
                "https://via.placeholder.com/100x100.png?text=SoftSolutions"),
            Job("UI/UX Designer", "DesignHub", "https://example.com/job5",
                "Design intuitive user interfaces.", ["Figma", "UX"], "LA, USA",
                "https://via.placeholder.com/100x100.png?text=DesignHub"),
        ]
        # For demo, just filter by keyword in title, description, or skills
        query_tokens = set(query.lower().split())
        matched_jobs = []
        for job in jobs_data:
            text_to_match = " ".join([
                job.title.lower(),
                job.description.lower(),
                " ".join(job.skills).lower()
            ])
            if any(token in text_to_match for token in query_tokens):
                matched_jobs.append(job)
        return matched_jobs
    except Exception as e:
        messagebox.showerror("Error", str(e))
        return []

# ---------------- RECOMMENDATION ENGINE ---------------- #
def recommend_jobs(query: str, candidates: List[Job], top_n=RESULTS_PER_PAGE) -> List[Tuple[Job, float]]:
    """
    Simple content-based recommendation:
    Scores jobs by overlap with query in title, description, and skills.
    """
    query_tokens = set(query.lower().split())
    recommendations: List[Tuple[Job, float]] = []

    for job in candidates:
        text_to_match = " ".join([
            job.title.lower(),
            job.description.lower(),
            " ".join(job.skills).lower()
        ])
        score = sum(1 for token in query_tokens if token in text_to_match)
        recommendations.append((job, score))

    recommendations.sort(key=lambda x: x[1], reverse=True)
    return recommendations[:top_n]

# ---------------- UI HELPERS ---------------- #
def open_url(url: str):
    webbrowser.open_new_tab(url)

def load_image(url: str, size=(80, 80)) -> Optional[ImageTk.PhotoImage]:
    if not url:
        return None
    if url in logo_cache:
        return logo_cache[url]
    try:
        resp = requests.get(url, timeout=10)
        img = Image.open(io.BytesIO(resp.content))
        img = img.resize(size, Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(img)
        logo_cache[url] = photo
        return photo
    except Exception:
        return None

def display_page():
    text.configure(state="normal")
    text.delete("1.0", "end")

    start = (current_page - 1) * RESULTS_PER_PAGE
    end = start + RESULTS_PER_PAGE
    page_results = all_ranked_jobs[start:end]

    if not page_results:
        text.insert("end", "No results found.\n")
        text.configure(state="disabled")
        update_pagination()
        return

    for idx, (job, score) in enumerate(page_results):
        text.insert("end", f"{job.title} @ {job.company}\n", f"title_{idx}")
        text.tag_config(f"title_{idx}", foreground="#1a0dab", font=("Segoe UI", 14, "bold"))
        text.tag_bind(f"title_{idx}", "<Double-Button-1>", lambda e, url=job.url: open_url(url))

        text.insert("end", f"Location: {job.location}  |  Skills: {', '.join(job.skills)}\n", f"info_{idx}")
        text.tag_config(f"info_{idx}", foreground="#006621", font=("Segoe UI", 10))

        logo = load_image(job.logo_url)
        if logo:
            text.image_create("end", image=logo)
            text.insert("end", "\n")

        text.insert("end", f"{job.description}\n\n")

    text.configure(state="disabled")
    update_pagination()

# ---------------- PAGINATION ---------------- #
def next_page():
    global current_page
    if current_page * RESULTS_PER_PAGE < len(all_ranked_jobs):
        current_page += 1
        display_page()

def prev_page():
    global current_page
    if current_page > 1:
        current_page -= 1
        display_page()

def update_pagination():
    total_pages = max(1, (len(all_ranked_jobs) - 1) // RESULTS_PER_PAGE + 1)
    page_label.config(text=f"Page {current_page} of {total_pages}")
    prev_btn.config(state=DISABLED if current_page == 1 else NORMAL)
    next_btn.config(state=DISABLED if current_page == total_pages else NORMAL)

# ---------------- SEARCH ---------------- #
def perform_search():
    query = query_entry.get().strip()
    if not query:
        messagebox.showwarning("Input Required", "Enter job title or keywords.")
        return
    threading.Thread(target=search_thread, args=(query,), daemon=True).start()

def search_thread(query: str):
    global all_ranked_jobs, current_page
    current_page = 1
    candidates = fetch_jobs(query)
    all_ranked_jobs = recommend_jobs(query, candidates, top_n=50)
    display_page()

# ---------------- UI SETUP ---------------- #
app = tb.Window(title="Job Recommendation Engine", themename="flatly", size=(980, 720), resizable=(True, True))

# Top frame
top = tb.Frame(app, padding=15)
top.pack(fill=tk.X)
tb.Label(top, text="Job Recommendation Engine", font=("Segoe UI", 16, "bold")).pack(anchor=tk.W)

query_entry = tb.Entry(top, font=("Segoe UI", 12))
query_entry.pack(fill=tk.X, pady=8)
query_entry.bind("<Return>", lambda e: perform_search())

tb.Button(top, text="Search", bootstyle="primary", command=perform_search).pack(anchor=tk.E)

# Results frame
result_frame = tb.Frame(app, padding=(15, 5))
result_frame.pack(fill=tk.BOTH, expand=True)

result_box = ScrolledText(result_frame, autohide=True)
result_box.pack(fill=tk.BOTH, expand=True)
text = result_box.text
text.configure(state="disabled", wrap="word")

# Navigation
nav = tb.Frame(app, padding=10)
nav.pack(fill=tk.X)

prev_btn = tb.Button(nav, text="← Prev", bootstyle="secondary", command=prev_page)
prev_btn.pack(side=tk.LEFT)

page_label = tb.Label(nav, text="Page 1", font=("Segoe UI", 10))
page_label.pack(side=tk.LEFT, padx=10)

next_btn = tb.Button(nav, text="Next →", bootstyle="secondary", command=next_page)
next_btn.pack(side=tk.LEFT)

app.mainloop()
