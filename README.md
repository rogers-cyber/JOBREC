# JOBREC – Job Recommendation Engine (Full Source Code)

JOBREC is a modern Python desktop application for **intelligent job search and recommendation**.  
It analyzes user-provided keywords and matches them against job listings to deliver **ranked job recommendations** based on relevance, skills, and descriptions — all inside a clean, responsive desktop UI.

This repository contains the **full source code**, allowing you to customize the recommendation logic, data sources, UI layout, pagination, or extend it with real-world job APIs and AI models.

------------------------------------------------------------
🌟 FEATURES
------------------------------------------------------------

- 🔍 Keyword-Based Job Search — Search jobs using titles, skills, or descriptions
- 🎯 Smart Job Ranking — Scores and ranks jobs by relevance to user query
- 📄 Paginated Results — Clean pagination for browsing multiple job listings
- 🏢 Company Details — Displays company name, location, skills, and description
- 🖼️ Company Logos — Dynamically loads and caches company logos
- 🌐 Click-to-Open Jobs — Double-click job titles to open listings in browser
- ⚡ Multithreaded Search — Keeps UI responsive during job fetching
- 🎨 Modern Themed UI — Built with Tkinter + ttkbootstrap (Flatly theme)
- 📜 Scrollable Results View — Comfortable reading for longer descriptions
- 🔒 Local Demo Mode — Uses mock job data (easy to replace with APIs)

------------------------------------------------------------
🚀 INSTALLATION
------------------------------------------------------------

1. Clone or download this repository:

git clone https://github.com/yourusername/JOBREC.git  
cd JOBREC

2. Install required Python packages:

pip install ttkbootstrap pillow requests

(Tkinter is included with standard Python installations.)

3. Run the application:

python job_recommendation_engine.py

4. Optional: Build a standalone executable using PyInstaller:

pyinstaller --onefile --windowed job_recommendation_engine.py

------------------------------------------------------------
💡 USAGE
------------------------------------------------------------

1. Enter Job Keywords:
   - Type job titles, skills, or technologies (e.g., `python`, `react`, `data`)

2. Search:
   - Click 🔍 **Search** or press **Enter**

3. Browse Results:
   - Jobs are ranked by relevance
   - View title, company, location, skills, and description
   - Logos load automatically when available

4. Open Job Listing:
   - Double-click a job title to open it in your web browser

5. Navigate Pages:
   - Use ← **Prev** and **Next →** buttons to browse results

------------------------------------------------------------
⚙️ CONFIGURATION OPTIONS
------------------------------------------------------------

Option                     Description
-------------------------- --------------------------------------------------
Search Input               Job keywords or skills
Search Button              Starts job search
Results Per Page           Controlled by RESULTS_PER_PAGE constant
Pagination Controls        Navigate job result pages
Logo Cache                 Prevents repeated image downloads
Recommendation Engine      Scores jobs based on keyword overlap

------------------------------------------------------------
📦 OUTPUT
------------------------------------------------------------

- Ranked Job Listings
  - Job Title
  - Company Name
  - Location
  - Required Skills
  - Job Description
  - Company Logo (if available)
- Clickable Job URLs

------------------------------------------------------------
📦 DEPENDENCIES
------------------------------------------------------------

- Python 3.10+
- Tkinter — Standard Python GUI framework
- ttkbootstrap — Modern themed UI components
- Pillow (PIL) — Image handling for company logos
- Requests — HTTP image fetching
- Threading — Background search execution
- Webbrowser — Opens job links externally

------------------------------------------------------------
📝 NOTES
------------------------------------------------------------

- Uses mock job data for demonstration
- Easily extendable with real job APIs (Indeed, LinkedIn, RapidAPI, etc.)
- Recommendation engine is keyword-based (simple & fast)
- Can be upgraded with NLP, embeddings, or ML-based ranking
- Suitable for demos, portfolio projects, or recruitment tools
- Fully portable when compiled as a standalone executable

------------------------------------------------------------
👤 ABOUT
------------------------------------------------------------

JOBREC is developed and maintained by **Mate Technologies**, delivering practical Python-based desktop applications with clean UI and extensible logic.

Website: https://matetools.gumroad.com

------------------------------------------------------------
📜 LICENSE
------------------------------------------------------------

Distributed as commercial source code.  
You may use it for personal or commercial projects.  
Redistribution, resale, or rebranding as a competing product is not allowed.
