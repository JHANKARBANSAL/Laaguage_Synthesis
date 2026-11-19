import matplotlib.pyplot as plt
import numpy as np

# Set global academic typography
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.edgecolor'] = '#333333'
plt.rcParams['axes.linewidth'] = 0.8

# ==============================================================================
# FIGURE 1: Language-Wise Execution Match (EX %) with Wilson 95% CIs
# ==============================================================================
languages = ['English\n(EN)', 'Marathi\n(MR)', 'Bengali\n(BN)', 'Telugu\n(TE)', 'Hinglish\n(HI-EN)', 'Hindi\n(HI)', 'Tamil\n(TA)']
ex_scores = [17.5, 17.5, 20.0, 20.0, 27.5, 27.5, 27.5]
# Asymmetric Wilson 95% CIs
ci_lower = [17.5 - 8.7, 17.5 - 8.7, 20.0 - 10.5, 20.0 - 10.5, 27.5 - 16.1, 27.5 - 16.1, 27.5 - 16.1]
ci_upper = [31.9 - 17.5, 31.9 - 17.5, 34.8 - 20.0, 34.8 - 20.0, 42.8 - 27.5, 42.8 - 27.5, 42.8 - 27.5]
yerr = [ci_lower, ci_upper]

colors = ['#868e96', '#868e96', '#4dabf7', '#4dabf7', '#2b8a3e', '#2b8a3e', '#2b8a3e']

fig, ax = plt.subplots(figsize=(8, 4.5), dpi=300)
bars = ax.bar(languages, ex_scores, color=colors, width=0.55, edgecolor='black', linewidth=0.9,
              yerr=yerr, capsize=4, error_kw=dict(lw=1.0, capthick=1.0, ecolor='#333333'))

for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2.0, yval + 1.2, f"{yval:.1f}%", 
            ha='center', va='bottom', fontsize=9.5, fontweight='bold', color='#111111')

ax.set_ylabel('Execution Match (EX %)', fontsize=11, fontweight='bold')
ax.set_title('Language-Wise Execution Match Across 7 Languages (N=280, Qwen-2.5-7B Zero-Shot)', 
             fontsize=11, fontweight='bold', pad=14)
ax.set_ylim(0, 48)
ax.axhline(y=17.5, color='#e03131', linestyle='--', linewidth=1.3, label='English Reference Baseline (17.5%)')
ax.annotate('+10.0 pp Indic Gain', xy=(5, 30), xytext=(4.5, 40),
            arrowprops=dict(facecolor='#2b8a3e', shrink=0.08, width=1.5, headwidth=6),
            fontsize=10, fontweight='bold', color='#2b8a3e', ha='center')
ax.legend(loc='upper left', frameon=True, facecolor='#f8f9fa', edgecolor='#cccccc', fontsize=9.5)
ax.grid(axis='y', linestyle=':', alpha=0.6)
plt.tight_layout()
plt.savefig('fig1_ex_indic_gap.png')
plt.close()
print("✅ Generated: fig1_ex_indic_gap.png")

# ==============================================================================
# FIGURE 2: Dual Metric Comparison (Execution Success ES vs. Execution Match EX)
# Demonstrating the "Semantic Divergence Gap"
# ==============================================================================
langs = ['EN', 'HI-EN', 'HI', 'MR', 'BN', 'TA', 'TE', 'Overall']
es_scores = [42.5, 52.5, 60.0, 47.5, 57.5, 62.5, 60.0, 54.6]
ex_scores2 = [17.5, 27.5, 27.5, 17.5, 20.0, 27.5, 20.0, 22.5]

x = np.arange(len(langs))
width = 0.35

fig, ax = plt.subplots(figsize=(8.5, 4.5), dpi=300)
rects1 = ax.bar(x - width/2, es_scores, width, label='Execution Success (ES % - Valid SQL)', color='#1c7ed6', edgecolor='black', lw=0.8)
rects2 = ax.bar(x + width/2, ex_scores2, width, label='Execution Match (EX % - Exact Semantics)', color='#20c997', edgecolor='black', lw=0.8)

# Shaded gap indicator for overall
ax.annotate('32.1 pp Semantic Divergence Gap\n(Executes cleanly but returns wrong rows)',
            xy=(7, 38), xytext=(4.8, 68),
            arrowprops=dict(facecolor='#d6336c', shrink=0.05, width=1.2, headwidth=5),
            fontsize=9.5, fontweight='bold', color='#d6336c', ha='center',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#fff0f6', edgecolor='#d6336c', lw=0.8))

ax.set_ylabel('Percentage (%)', fontsize=11, fontweight='bold')
ax.set_title('The Semantic Divergence Gap: Execution Success (ES) vs. Execution Match (EX)', fontsize=11, fontweight='bold', pad=14)
ax.set_xticks(x)
ax.set_xticklabels(langs, fontweight='bold')
ax.set_ylim(0, 80)
ax.legend(loc='upper right', frameon=True, facecolor='#f8f9fa', edgecolor='#cccccc', fontsize=9.5)
ax.grid(axis='y', linestyle=':', alpha=0.6)
plt.tight_layout()
plt.savefig('fig2_semantic_divergence.png')
plt.close()
print("✅ Generated: fig2_semantic_divergence.png")

# ==============================================================================
# FIGURE 3: Relational Join-Depth Degradation Curve (0 to 6 Joins)
# ==============================================================================
join_depths = [0, 1, 2, 3, 4, 5, 6]
# Empirical join performance degradation
accuracy = [76.5, 65.0, 36.2, 21.4, 0.0, 0.0, 0.0]

fig, ax = plt.subplots(figsize=(7.5, 4.2), dpi=300)
ax.plot(join_depths, accuracy, marker='o', markersize=8, color='#d6336c', linewidth=2.4, label='IndicSQL (Qwen-2.5-7B Zero-Shot)')
ax.fill_between(join_depths, accuracy, color='#fcc2d7', alpha=0.4)

# Threshold markers
ax.axvline(x=1.5, color='#495057', linestyle='--', linewidth=1.0)
ax.axvline(x=3.5, color='#c92a2a', linestyle='--', linewidth=1.2)

ax.text(0.7, 50, 'Shallow Joins\n(69.0% EX)', fontsize=9.5, fontweight='bold', ha='center', color='#2b8a3e')
ax.text(2.5, 50, 'Moderate Joins\n(27.1% EX)', fontsize=9.5, fontweight='bold', ha='center', color='#e67700')
ax.text(5.0, 50, 'Catastrophic Collapse\nDepth >= 4 (0.0% EX)', fontsize=9.5, fontweight='bold', ha='center', color='#c92a2a')

ax.set_xlabel('Relational Join Depth (Number of Foreign-Key Joins)', fontsize=11, fontweight='bold')
ax.set_ylabel('Execution Match (EX %)', fontsize=11, fontweight='bold')
ax.set_title('Relational Join-Depth Degradation Curve on IndicDBBench (N=280)', fontsize=11, fontweight='bold', pad=14)
ax.set_ylim(-2, 90)
ax.set_xticks(join_depths)
ax.grid(True, linestyle=':', alpha=0.6)
ax.legend(loc='upper right', frameon=True, fontsize=9.5)
plt.tight_layout()
plt.savefig('fig3_join_degradation.png')
plt.close()
print("✅ Generated: fig3_join_degradation.png")

# ==============================================================================
# FIGURE 4: Root-Cause Decomposition Donut Chart (N_fail = 128)
# ==============================================================================
fig, ax = plt.subplots(figsize=(6.5, 4.5), dpi=300)
labels = [
    'Column / Schema Hallucination\n(75.0%, 96 cases)',
    'Runtime Timeout > 60s\n(19.5%, 25 cases)',
    'Upstream Gold Defects\n(5.5%, 7 cases)'
]
sizes = [75.0, 19.5, 5.5]
colors = ['#e03131', '#fd7e14', '#fab005']
explode = (0.06, 0.02, 0.02)

wedges, texts, autotexts = ax.pie(
    sizes, explode=explode, labels=labels, colors=colors,
    autopct='%1.1f%%', startangle=130, pctdistance=0.72,
    textprops=dict(color="#111111", fontsize=9.5),
    wedgeprops=dict(width=0.48, edgecolor='white', linewidth=2)
)
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_weight('bold')
    autotext.set_fontsize(10)

ax.set_title('Root-Cause Breakdown of Non-Executable Queries (N_fail = 128)', fontsize=11, fontweight='bold', pad=14)
plt.tight_layout()
plt.savefig('fig4_error_donut.png')
plt.close()
print("✅ Generated: fig4_error_donut.png")

# ==============================================================================
# FIGURE 5: Wall-Clock Latency Profile per Language
# ==============================================================================
lang_latency = ['Bengali (BN)', 'Telugu (TE)', 'Hinglish (HI-EN)', 'Tamil (TA)', 'Marathi (MR)', 'Hindi (HI)', 'English (EN)']
latencies = [13.2, 25.8, 41.1, 43.0, 44.0, 46.2, 58.4]
colors_lat = ['#20c997', '#38d9a9', '#4dabf7', '#4dabf7', '#4dabf7', '#4dabf7', '#fa5252']

fig, ax = plt.subplots(figsize=(7.5, 4.2), dpi=300)
bars = ax.barh(lang_latency, latencies, color=colors_lat, edgecolor='black', linewidth=0.8, height=0.6)

for bar in bars:
    xval = bar.get_width()
    ax.text(xval + 1.2, bar.get_y() + bar.get_height()/2.0, f"{xval:.1f} s",
            ha='left', va='center', fontsize=9.5, fontweight='bold')

ax.axvline(x=38.8, color='#333333', linestyle='--', linewidth=1.2, label='Mean Benchmark Latency (38.8 s)')
ax.set_xlabel('Mean Wall-Clock Latency per Query (Seconds)', fontsize=11, fontweight='bold')
ax.set_title('Inference Latency Profile Across 7 Languages (Local Qwen-2.5-7B, 4-bit)', fontsize=11, fontweight='bold', pad=14)
ax.set_xlim(0, 70)
ax.legend(loc='lower right', frameon=True, fontsize=9.5)
ax.grid(axis='x', linestyle=':', alpha=0.6)
plt.tight_layout()
plt.savefig('fig5_latency_profile.png')
plt.close()
print("✅ Generated: fig5_latency_profile.png")

# ==============================================================================
# FIGURE 6: Radar Chart of Benchmark Complexity (IndicDBBench vs. Spider vs. BIRD)
# ==============================================================================
categories = ['Max Join Depth', 'Aggregation Density', 'Abbreviation Entropy', 'Multilingual Diversity', 'Domain Realism']
N_cat = len(categories)

# Normalized scores (0 to 10 scale)
indicdb = [10.0, 9.5, 9.8, 9.5, 10.0]
spider  = [3.0,  3.5, 1.5, 2.0,  3.0]
bird    = [5.0,  5.2, 3.0, 2.0,  6.5]

# Repeat first value to close polygon
indicdb += indicdb[:1]
spider  += spider[:1]
bird    += bird[:1]
angles = [n / float(N_cat) * 2 * np.pi for n in range(N_cat)]
angles += angles[:1]

fig, ax = plt.subplots(figsize=(6.5, 6.5), subplot_kw=dict(polar=True), dpi=300)
plt.xticks(angles[:-1], categories, color='#222222', size=9.5, fontweight='bold')
ax.set_rlabel_position(0)
plt.yticks([2, 4, 6, 8, 10], ["2", "4", "6", "8", "10"], color="#666666", size=8)
plt.ylim(0, 10.5)

ax.plot(angles, indicdb, linewidth=2.0, linestyle='solid', label='IndicDBBench (Gov Open Data)', color='#2b8a3e')
ax.fill(angles, indicdb, color='#2b8a3e', alpha=0.25)

ax.plot(angles, bird, linewidth=1.8, linestyle='dashed', label='BIRD (HKU)', color='#1c7ed6')
ax.fill(angles, bird, color='#1c7ed6', alpha=0.15)

ax.plot(angles, spider, linewidth=1.8, linestyle='dotted', label='Spider (Yale)', color='#868e96')
ax.fill(angles, spider, color='#868e96', alpha=0.10)

plt.title('Benchmark Relational & Linguistic Complexity Topology', size=11, fontweight='bold', pad=20)
plt.legend(loc='upper right', bbox_to_anchor=(1.25, 1.15), frameon=True, fontsize=9)
plt.tight_layout()
plt.savefig('fig6_radar_complexity.png')
plt.close()
print("✅ Generated: fig6_radar_complexity.png")

print("\n🚀 ALL 6 PUBLICATION-GRADE FIGURES GENERATED SUCCESSFULLY!")
