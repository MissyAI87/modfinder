# ModFinder for Sims 4

**ModFinder** is a Python script that searches for Sims 4 mods based on keywords, then filters for links from trusted sites. It outputs real, usable download links and stores them in a local `.json` file for review.

---

## 💡 Features

- 🔍 Searches for Sims 4 mods by keyword
- 🌐 Filters for safe, trusted domains (e.g., CurseForge, Patreon, etc.)
- 💾 Saves all valid mod URLs to a JSON file
- 🧠 Meant to be part of an AI-controlled mod manager system
- 🧪 Experimental detection of direct download pages

---

## 🖥️ How to Run

Make sure your virtual environment is activated (if you use one):

```bash
source ~/sims4env/bin/activate
python modfinder.py
modfinder_results.json
---

## 🙋 Author Notes

This tool was built to automate and simplify the process of finding Sims 4 mods. It’s designed to integrate with a larger AI mod manager system. Building this taught me a lot about filtering web results, working with JSON, and planning for future automation.

---

## 📋 Future Plans

- Improve link verification and expand trusted domain list  
- Add headless browser scraping for better accuracy  
- Integrate with ModFixer and Baby AI assistant  
- Build a GUI version using PySimpleGUI or Gradio  
- Allow preview of mod descriptions or images (when available)

---

## 📝 License

This project is licensed under the MIT License.  
You are free to use, modify, and distribute this software.  
There is no warranty or liability for issues that may arise from use.


