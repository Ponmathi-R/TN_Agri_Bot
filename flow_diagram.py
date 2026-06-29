import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Initialize the canvas with a gorgeous vertical infographic format
fig, ax = plt.subplots(figsize=(15, 20), facecolor='#f4faf4')
ax.set_facecolor('#f4faf4')
ax.set_xlim(0, 100)
ax.set_ylim(0, 140)
plt.axis('off')

# -------------------------------------------------------------
# 1. PREMIUM HEADER PANEL
# -------------------------------------------------------------
header_box = patches.FancyBboxPatch((2, 122), 96, 14, boxstyle="round,pad=1", 
                                    facecolor="#1b5e20", edgecolor="none")
ax.add_patch(header_box)
plt.text(50, 131, "🌾 TN SCHEME NAVIGATOR AI 🌾", color="white", fontsize=26, 
         fontweight="bold", ha="center", va="center", family="sans-serif")
plt.text(50, 125, "Bilingual GenAI + RAG Architecture Pipeline for Tamil Nadu Government Schemes", 
         color="#ffb300", fontsize=12, fontweight="600", ha="center", va="center")

# -------------------------------------------------------------
# 2. PROJECT GOAL BLOCK
# -------------------------------------------------------------
goal_box = patches.FancyBboxPatch((2, 110), 96, 8, boxstyle="round,pad=0.5", 
                                  facecolor="#ffffff", edgecolor="#2e7d32", linewidth=2)
ax.add_patch(goal_box)
# Draw a cute miniature targeting dart/goal icon
ax.add_patch(patches.Circle((5, 114), radius=1.8, facecolor="#e8f5e9", edgecolor="#1b5e20", linewidth=1.5))
ax.add_patch(patches.Circle((5, 114), radius=1.0, facecolor="#ffb300", edgecolor="none"))
plt.text(9, 114, "🎯 Project Goal:", color="#1b5e20", fontsize=14, fontweight="bold", va="center")
goal_text = "Help citizens, farmers, and manufacturers instantly search, explore, and understand official Tamil Nadu\nGovernment agricultural welfare policies using a secure, private local LLM engine."
plt.text(25, 114, goal_text, color="#3e2723", fontsize=11.5, va="center")

# -------------------------------------------------------------
# 3. HOW THE SYSTEM WORKS (Grid Layout with Miniature Drawings)
# -------------------------------------------------------------
plt.text(2, 102, "⚙️ Step-by-Step Data Processing & Architecture Flow", color="#1b5e20", fontsize=16, fontweight="bold")

# Definition of steps with customized miniature drawings instructions
steps = [
    {"num": "1", "title": "TN Gov Portal", "desc": "Scrapes policy tables\nfrom tn.gov.in source", "color": "#e8f5e9", "type": "web"},
    {"num": "2", "title": "Text Splitter", "desc": "Chunks content into\n1200 char fragments", "color": "#fff8e1", "type": "split"},
    {"num": "3", "title": "Nomic Engine", "desc": "Transforms texts into\nvector mathematics", "color": "#e1f5fe", "type": "embed"},
    {"num": "4", "title": "FAISS Index", "desc": "Stores structural coordinate\nembeddings locally", "color": "#ffecb3", "type": "db"},
    {"num": "5", "title": "User Query", "desc": "Accepts text in both\nEnglish & தமிழ் strings", "color": "#f3e5f5", "type": "query"},
    {"num": "6", "title": "Live Retriever", "desc": "Pulls top matching fragments\nand streams to UI panel", "color": "#e8eaf6", "type": "retrieve"},
    {"num": "7", "title": "Local Llama 3", "desc": "Generates factually aligned\nreplies via private core", "color": "#ffe0b2", "type": "llm"},
    {"num": "8", "title": "Bilingual UI", "desc": "Displays interactive cards\nand motivational quotes", "color": "#c8e6c9", "type": "ui"}
]

# Layout parameters (2 rows x 4 columns grid for massive, readable cards)
grid_positions = [
    (3, 76), (27, 76), (51, 76), (75, 76),  # Row 1
    (3, 46), (27, 46), (51, 46), (75, 46)   # Row 2
]

box_w = 21
box_h = 22

for i, pos in enumerate(grid_positions):
    x, y = pos
    step = steps[i]
    
    # Base Card
    card = patches