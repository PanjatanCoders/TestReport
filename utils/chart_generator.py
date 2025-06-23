import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os

def generate_pie_chart(df, output_dir="reports/charts"):
    status_counts = df["status"].value_counts()
    labels = status_counts.index.tolist()
    sizes = status_counts.tolist()

    # Define consistent colors
    color_map = {
        "Pass": "#4CAF50",       # Green
        "Fail": "#F44336",       # Red
        "Skipped": "#FF9800",    # Orange
        "Blocked": "#9E9E9E",    # Gray
        "Retest": "#FFEB3B"      # Yellow
    }

    status_colors = [color_map.get(label, "#2196F3") for label in labels]  # fallback to blue

    fig, (ax1, ax2) = plt.subplots(
        1, 2,
        figsize=(11, 6),
        gridspec_kw={'width_ratios': [2, 1]}
    )

    # 📊 Pie Chart
    ax1.pie(
        sizes,
        labels=labels,
        autopct="%1.1f%%",
        startangle=140,
        colors=status_colors,
        textprops={'fontsize': 12}
    )
    ax1.set_title("Test Execution Summary", fontsize=14, fontweight='bold')

    # 📝 Summary section
    ax2.axis("off")
    ax2.set_title("Summary", fontsize=14, fontweight='bold', loc='left', pad=20)

    total = sum(sizes)
    y_pos = 1.0
    for label, size in zip(labels, sizes):
        percent = round((size / total) * 100, 1)
        color = color_map.get(label, "#2196F3")

        # Add bullet
        circle = mpatches.Circle((0.02, y_pos), 0.012, color=color, transform=ax2.transAxes, clip_on=False)
        ax2.add_patch(circle)

        # Status text (larger & bold)
        ax2.text(
            0.06, y_pos,
            f"{label}: {size} ({percent}%)",
            transform=ax2.transAxes,
            fontsize=12,
            fontweight='bold',
            va='center',
            ha='left',
            family='monospace'
        )
        y_pos -= 0.1  # Increased spacing between lines

    # # 🏢 Company name on top
    # fig.suptitle("E2OPEN", fontsize=18, fontweight='bold', color='#2c3e50')

    # 💾 Save the chart
    os.makedirs(output_dir, exist_ok=True)
    chart_path = os.path.join(output_dir, "execution_summary.png")
    plt.tight_layout(rect=[0, 0.03, 1, 0.92])  # space for suptitle
    plt.savefig(chart_path)
    plt.close()
    print(f"[✓] Pie chart saved to: {chart_path}")
