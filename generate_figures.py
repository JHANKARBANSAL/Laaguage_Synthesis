import matplotlib.pyplot as plt

# ==============================================================================
# Generate figure_ex_comparison.png (Bar Chart for Section VI)
# ==============================================================================
languages = ['English', 'Marathi', 'Bengali', 'Telugu', 'Hinglish', 'Hindi', 'Tamil']
ex_scores = [17.5, 17.5, 20.0, 20.0, 27.5, 27.5, 27.5]
# Professional academic color palette:
# Gray for English baseline, subtle blue for mid-tier, dark green for top Indic
colors = ['#868e96', '#868e96', '#4dabf7', '#4dabf7', '#2b8a3e', '#2b8a3e', '#2b8a3e']

plt.figure(figsize=(7, 4.2), dpi=300)
bars = plt.bar(languages, ex_scores, color=colors, width=0.55, edgecolor='black', linewidth=0.8)

# Add exact percentage labels on top of bars
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2.0, yval + 0.8, f"{yval:.1f}%", 
             ha='center', va='bottom', fontsize=9.5, fontweight='bold')

plt.ylabel('Execution Match (EX %)', fontsize=11, fontweight='bold')
plt.title('Execution Match Across 7 Languages (Qwen-2.5-7B Zero-Shot)', fontsize=11, fontweight='bold', pad=12)
plt.ylim(0, 35)
plt.axhline(y=17.5, color='#e03131', linestyle='--', linewidth=1.2, label='English Baseline (17.5%)')
plt.legend(loc='upper left', frameon=True, fontsize=9.5)
plt.grid(axis='y', linestyle='--', alpha=0.4)
plt.tight_layout()

plt.savefig('figure_ex_comparison.png')
print("✅ Successfully generated: figure_ex_comparison.png")

# ==============================================================================
# Generate figure_error_breakdown.png (Donut Chart for Section VII)
# ==============================================================================
plt.figure(figsize=(6, 4.5), dpi=300)
labels = [
    'Column / Schema Hallucination\n(75.0%, 96 cases)',
    'Runtime Timeout >60s\n(19.5%, 25 cases)',
    'Upstream Gold Defects\n(5.5%, 7 cases)'
]
sizes = [75.0, 19.5, 5.5]
colors = ['#e03131', '#fd7e14', '#fab005']
explode = (0.05, 0, 0)

wedges, texts, autotexts = plt.pie(
    sizes, explode=explode, labels=labels, colors=colors,
    autopct='%1.1f%%', startangle=140, pctdistance=0.75,
    textprops=dict(color="black", fontsize=9)
)
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_weight('bold')
    

centre_circle = plt.Circle((0,0), 0.50, fc='white')
fig = plt.gcf()
fig.gca().add_artist(centre_circle)

plt.title('Root-Cause Breakdown of Non-Executable Queries (N=128)', fontsize=11, fontweight='bold', pad=12)
plt.tight_layout()
plt.savefig('figure_error_breakdown.png')
print("✅ Successfully generated: figure_error_breakdown.png")

