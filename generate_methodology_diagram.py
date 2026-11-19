import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Set global academic typography with full Unicode support
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'Kohinoor Devanagari', 'DejaVu Sans', 'sans-serif']
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.edgecolor'] = '#333333'
plt.rcParams['axes.linewidth'] = 0.8

def generate_methodology_diagram():
    fig, ax = plt.subplots(figsize=(16, 9), dpi=300)
    ax.set_xlim(0, 160)
    ax.set_ylim(0, 90)
    ax.axis('off')

    # Color Palette - Professional Academic / Tech
    NAVY_BORDER = '#002b49'
    NAVY_FILL = '#e8f4f8'
    BLUE_CARD = '#d0ebff'
    BLUE_BORDER = '#1864ab'
    GREEN_CARD = '#d3f9d8'
    GREEN_BORDER = '#2b8a3e'
    ORANGE_CARD = '#ffe8cc'
    ORANGE_BORDER = '#d9480f'
    PURPLE_CARD = '#f3d9fa'
    PURPLE_BORDER = '#862e9c'
    RED_ACCENT = '#e03131'
    GRAY_CONTAINER = '#f8f9fa'
    GRAY_BORDER = '#adb5bd'
    TEXT_MAIN = '#111111'
    TEXT_MUTED = '#495057'

    # -------------------------------------------------------------
    # 0. MAIN TITLE & SUBTITLE BANNER
    # -------------------------------------------------------------
    ax.text(80, 86.5, "IndicSQL: Multi-Agent Swarm Architecture for Multilingual Governance Text-to-SQL",
            ha='center', va='center', fontsize=14, fontweight='bold', color=NAVY_BORDER)
    ax.text(80, 83.5, "Five-Agent Modular Pipeline Decomposing Schema Routing, Intent Abstraction, Relational Grounding, Execution Validation & Verbalization",
            ha='center', va='center', fontsize=9.5, fontstyle='italic', color=TEXT_MUTED)

    # -------------------------------------------------------------
    # 1. CITIZEN INPUT LAYER (Left Column)
    # -------------------------------------------------------------
    # Big Container
    input_box = patches.FancyBboxPatch((4, 12), 24, 66, boxstyle='round,pad=1.0',
                                       facecolor='#f1f3f5', edgecolor=GRAY_BORDER, lw=1.2, linestyle='--')
    ax.add_patch(input_box)
    ax.text(16, 75, "CITIZEN INPUT TIER", ha='center', va='center', fontsize=10, fontweight='bold', color='#343a40')

    # Example query cards
    queries = [
        ("Hindi (HI)", "1991 की जनगणना के आधार पर...", "#e7f5ff", "#1c7ed6"),
        ("Telugu (TE)", "2022 సంవత్సరానికి చెందిన లేదా...", "#e6fcf5", "#0ca678"),
        ("Bengali (BN)", "২০২১ সালে রেকর্ড করা প্রথম...", "#fff4e6", "#f76707"),
        ("Tamil (TA)", "2021-ல் பதிவு செய்யப்பட்ட...", "#f8f0fc", "#ae3ec9"),
        ("Hinglish", "5000 se adhik aawas wale...", "#fff9db", "#f59f00"),
        ("English (EN)", "List districts where total houses > 5000...", "#f1f3f5", "#495057"),
    ]
    y_pos = 67
    for lang, q_text, fcolor, bcolor in queries:
        card = patches.FancyBboxPatch((6, y_pos - 6), 20, 6.2, boxstyle='round,pad=0.4',
                                      facecolor=fcolor, edgecolor=bcolor, lw=1.0)
        ax.add_patch(card)
        ax.text(7.5, y_pos - 1.8, lang, fontsize=8, fontweight='bold', color=bcolor)
        ax.text(7.5, y_pos - 4.2, f'"{q_text[:28]}..."', fontsize=7.5, color='#212529', fontstyle='italic')
        y_pos -= 8.5

    # -------------------------------------------------------------
    # 2. AGENT 1: SCHEMA ROUTER (A_route)
    # -------------------------------------------------------------
    a1_box = patches.FancyBboxPatch((34, 46), 25, 30, boxstyle='round,pad=0.8',
                                    facecolor=BLUE_CARD, edgecolor=BLUE_BORDER, lw=1.5)
    ax.add_patch(a1_box)
    ax.text(46.5, 72.5, "Agent 1: Schema Router", ha='center', va='center', fontsize=10.5, fontweight='bold', color=BLUE_BORDER)
    ax.text(46.5, 69.8, r"($\mathcal{A}_{\mathrm{route}}$ - 98.9% Accuracy)", ha='center', va='center', fontsize=9, fontweight='bold', color='#1971c2')

    a1_features = [
        "• Dense Semantic Embeddings",
        "• Phonetic n-gram Anchors",
        "• Zero-Shot Domain Pruning",
        "• Isolates Target Schema",
        "  from 10+ NDAP Catalogs",
        "• No Gold Hints Leaked"
    ]
    y_feat = 65
    for feat in a1_features:
        ax.text(36.5, y_feat, feat, fontsize=7.8, color='#1864ab')
        y_feat -= 3.2

    # Output artifact pill
    p1 = patches.FancyBboxPatch((36, 48), 21, 4.2, boxstyle='round,pad=0.3', facecolor='#ffffff', edgecolor=BLUE_BORDER, lw=1.0)
    ax.add_patch(p1)
    ax.text(46.5, 50.1, r"Target Schema $S_k$ (e.g. Census 1991)", ha='center', va='center', fontsize=7.5, fontweight='bold', color=BLUE_BORDER)

    # -------------------------------------------------------------
    # 3. AGENT 2: METRIC & INTENT PLANNER (A_plan)
    # -------------------------------------------------------------
    a2_box = patches.FancyBboxPatch((65, 46), 27, 30, boxstyle='round,pad=0.8',
                                    facecolor=PURPLE_CARD, edgecolor=PURPLE_BORDER, lw=1.5)
    ax.add_patch(a2_box)
    ax.text(78.5, 72.5, "Agent 2: Intent Planner", ha='center', va='center', fontsize=10.5, fontweight='bold', color=PURPLE_BORDER)
    ax.text(78.5, 69.8, r"($\mathcal{A}_{\mathrm{plan}}$ - Intent Neutralization)", ha='center', va='center', fontsize=9, fontweight='bold', color='#6f2dbd')

    a2_features = [
        "• Bypasses Token Fertility Penalty",
        "• Deconstructs Query to Tuple:",
        r"  $\Pi = \langle \mathcal{M}, \mathcal{D}, \mathcal{F}, \mathcal{O}, \mathcal{K} \rangle$",
        r"• $\mathcal{M}$: Aggregations (SUM, AVG)",
        r"• $\mathcal{D}$: Group Dimensions (Location)",
        r"• $\mathcal{F}$: Filters (>5000, >1000)",
        r"• $\mathcal{K}$: Temporal Scopes (Year=1991)"
    ]
    y_feat = 65
    for feat in a2_features:
        ax.text(67.5, y_feat, feat, fontsize=7.8, color='#5c2491')
        y_feat -= 3.2

    p2 = patches.FancyBboxPatch((67, 48), 23, 4.2, boxstyle='round,pad=0.3', facecolor='#ffffff', edgecolor=PURPLE_BORDER, lw=1.0)
    ax.add_patch(p2)
    ax.text(78.5, 50.1, r"Semantic Intent Tuple ($\Pi$)", ha='center', va='center', fontsize=7.8, fontweight='bold', color=PURPLE_BORDER)

    # -------------------------------------------------------------
    # 4. AGENT 3: RELATIONAL SCHEMA GROUNDER (A_ground)
    # -------------------------------------------------------------
    a3_box = patches.FancyBboxPatch((98, 46), 28, 30, boxstyle='round,pad=0.8',
                                    facecolor=ORANGE_CARD, edgecolor=ORANGE_BORDER, lw=1.5)
    ax.add_patch(a3_box)
    ax.text(112, 72.5, "Agent 3: Schema Grounder", ha='center', va='center', fontsize=10.5, fontweight='bold', color=ORANGE_BORDER)
    ax.text(112, 69.8, r"($\mathcal{A}_{\mathrm{ground}}$ - Graph & Catalog Linking)", ha='center', va='center', fontsize=9, fontweight='bold', color='#c2410c')

    a3_features = [
        "• Disambiguates Cryptic Acronyms:",
        "  (tot_p_m, sch_mgmt_cat, dist_name)",
        "• Steiner Tree Join-Path Traversal",
        "• Traverses Foreign-Key Multigraph",
        "  Chains (up to Depth 6)",
        "• Generates Syntactically Valid SQL"
    ]
    y_feat = 65
    for feat in a3_features:
        ax.text(100.5, y_feat, feat, fontsize=7.8, color='#9a3412')
        y_feat -= 3.2

    p3 = patches.FancyBboxPatch((100, 48), 24, 4.2, boxstyle='round,pad=0.3', facecolor='#ffffff', edgecolor=ORANGE_BORDER, lw=1.0)
    ax.add_patch(p3)
    ax.text(112, 50.1, r"Synthesized SQL ($\hat{q}$)", ha='center', va='center', fontsize=7.8, fontweight='bold', color=ORANGE_BORDER)

    # -------------------------------------------------------------
    # 5. AGENT 4: EXECUTION VALIDATOR (A_valid) & POSTGRESQL ENGINE
    # -------------------------------------------------------------
    a4_box = patches.FancyBboxPatch((98, 12), 28, 27, boxstyle='round,pad=0.8',
                                    facecolor=GREEN_CARD, edgecolor=GREEN_BORDER, lw=1.5)
    ax.add_patch(a4_box)
    ax.text(112, 35.5, "Agent 4: Execution Validator", ha='center', va='center', fontsize=10.5, fontweight='bold', color=GREEN_BORDER)
    ax.text(112, 32.8, r"($\mathcal{A}_{\mathrm{valid}}$ - PostgreSQL 16 Guardrail)", ha='center', va='center', fontsize=9, fontweight='bold', color='#1e7e34')

    a4_features = [
        "• PostgreSQL 16 Isolated Runtime",
        "• Read-Only Transaction Wrap:",
        "  BEGIN READ ONLY ... ROLLBACK",
        "• 60s Timeout Barrier (tau=60s)",
        "• Traps Cartesian Join Blowups",
        "• Self-Correction Diagnostic Feed"
    ]
    y_feat = 28.5
    for feat in a4_features:
        ax.text(100.5, y_feat, feat, fontsize=7.8, color='#1b5e20')
        y_feat -= 2.9

    p4 = patches.FancyBboxPatch((100, 13.5), 24, 4.0, boxstyle='round,pad=0.3', facecolor='#ffffff', edgecolor=GREEN_BORDER, lw=1.0)
    ax.add_patch(p4)
    ax.text(112, 15.5, r"Validated Result ($\mathcal{R}$)", ha='center', va='center', fontsize=7.8, fontweight='bold', color=GREEN_BORDER)

    # -------------------------------------------------------------
    # 6. AGENT 5: MULTILINGUAL RESPONSE VERBALIZER (A_verbalize)
    # -------------------------------------------------------------
    a5_box = patches.FancyBboxPatch((45, 12), 44, 27, boxstyle='round,pad=0.8',
                                    facecolor=NAVY_FILL, edgecolor=NAVY_BORDER, lw=1.5)
    ax.add_patch(a5_box)
    ax.text(67, 35.5, "Agent 5: Response Verbalizer", ha='center', va='center', fontsize=10.5, fontweight='bold', color=NAVY_BORDER)
    ax.text(67, 32.8, r"($\mathcal{A}_{\mathrm{verbalize}}$ - Native Citizen Response)", ha='center', va='center', fontsize=9, fontweight='bold', color='#004085')

    a5_features = [
        "• Maps Relational Records back to Citizen's Native Script / Tongue",
        "• Synthesizes Mother-Tongue Executive Summaries (HI, TE, BN, TA, MR, EN)",
        "• Explains Null Result Sets Gracefully (e.g. Inverted 'OR' vs 'AND')",
        "• Catches Schema Exceptions into User-Friendly Native Advice"
    ]
    y_feat = 28
    for feat in a5_features:
        ax.text(47.5, y_feat, feat, fontsize=7.8, color='#084298')
        y_feat -= 3.1

    p5 = patches.FancyBboxPatch((48, 13.5), 38, 4.0, boxstyle='round,pad=0.3', facecolor='#ffffff', edgecolor=NAVY_BORDER, lw=1.0)
    ax.add_patch(p5)
    ax.text(67, 15.5, "Grounded Multilingual Citizen Answer + Verified Records", ha='center', va='center', fontsize=7.8, fontweight='bold', color=NAVY_BORDER)

    # -------------------------------------------------------------
    # 7. CITIZEN OUTPUT TIER (Far Right / Bottom Left)
    # -------------------------------------------------------------
    out_box = patches.FancyBboxPatch((132, 12), 24, 66, boxstyle='round,pad=1.0',
                                     facecolor='#f8f9fa', edgecolor='#20c997', lw=1.5)
    ax.add_patch(out_box)
    ax.text(144, 75, "CITIZEN UI / PORTAL", ha='center', va='center', fontsize=10, fontweight='bold', color='#099268')

    out_cards = [
        ("Grounded Summary", "1991 की जनगणना के आधार\nपर 18 स्थान मिले...", "#e6fcf5", "#099268"),
        ("Verified Table", "location_name | houses | ST\nAlipurduar    | 6,240  | 1,420\nSiliguri      | 8,910  | 2,150", "#f1f3f5", "#495057"),
        ("Zero Cloud Leakage", "100% Local Inference\n(Qwen-2.5-7B on Ollama)\nVRAM < 5.5 GB", "#e7f5ff", "#1864ab"),
        ("Audit Receipts", "SHA-256 Verified Log\nDeterministic Greedy T=0.0", "#fff9db", "#d97706"),
    ]
    y_out = 66
    for title, desc, fc, ec in out_cards:
        c = patches.FancyBboxPatch((134, y_out - 8.5), 20, 9.5, boxstyle='round,pad=0.4', facecolor=fc, edgecolor=ec, lw=1.0)
        ax.add_patch(c)
        ax.text(135.5, y_out - 2, title, fontsize=8, fontweight='bold', color=ec)
        ax.text(135.5, y_out - 4.5, desc, fontsize=7.0, color='#212529')
        y_out -= 12.5

    # -------------------------------------------------------------
    # 8. CONNECTING ARROWS & FLOW PIPELINES
    # -------------------------------------------------------------
    def draw_arrow(start, end, label=None, color='#495057', rad=0.0, label_offset=(0, 1.5)):
        arrow = patches.FancyArrowPatch(start, end,
                                         connectionstyle=f"arc3,rad={rad}",
                                         arrowstyle="-|>,head_length=5,head_width=3.5",
                                         color=color, lw=1.8)
        ax.add_patch(arrow)
        if label:
            mid = ((start[0] + end[0]) / 2 + label_offset[0], (start[1] + end[1]) / 2 + label_offset[1])
            ax.text(mid[0], mid[1], label, ha='center', va='center', fontsize=7.2, fontweight='bold',
                    color=color, bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor=color, lw=0.6))

    # Input -> A_route
    draw_arrow((28, 61), (34, 61), label="Raw NLQ (Q)", color='#1864ab')

    # A_route -> A_plan
    draw_arrow((59, 61), (65, 61), label="Schema (S_k)", color='#6f2dbd')

    # A_plan -> A_ground
    draw_arrow((92, 61), (98, 61), label="Tuple (Π)", color='#c2410c')

    # A_ground -> A_valid
    draw_arrow((112, 46), (112, 39), label="SQL (q̂)", color='#d9480f')

    # A_valid Self-Correction Loop back to A_ground (Red Curving Arrow)
    draw_arrow((126, 32), (126, 52), label="Syntax / Timeout Retry Loop", color=RED_ACCENT, rad=-0.45, label_offset=(4.5, 0))

    # A_valid -> A_verbalize
    draw_arrow((98, 25), (89, 25), label="Result (R)", color='#1e7e34')

    # A_verbalize -> Citizen UI
    draw_arrow((89, 15), (132, 15), label="Native Answer", color='#099268', rad=-0.12, label_offset=(0, -2.5))

    # A_ground -> Citizen UI (optional audit view)
    draw_arrow((126, 61), (132, 61), label="Audit SQL", color='#495057')

    plt.tight_layout()
    plt.savefig('fig_methodology_architecture.png', bbox_inches='tight')
    plt.close()
    print("✅ Successfully generated: fig_methodology_architecture.png (300 DPI)")

if __name__ == '__main__':
    generate_methodology_diagram()
