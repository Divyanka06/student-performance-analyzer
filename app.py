import gradio as gr
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# ==========================================
# DATA
# ==========================================

data = {
    "Name": [
        "Aarav",
        "Riya",
        "Rahul",
        "Sneha",
        "Ananya",
        "Kabir",
        "Priya",
        "Aditya"
    ],
    "Python": [85, 78, 65, 90, 88, 72, 95, 70],
    "NumPy": [80, 82, 60, 85, 90, 68, 92, 75],
    "Pandas": [88, 75, 70, 92, 85, 74, 96, 78],
    "Mathematics": [75, 80, 62, 88, 91, 70, 89, 73]
}

df = pd.DataFrame(data)

subjects = [
    "Python",
    "NumPy",
    "Pandas",
    "Mathematics"
]


# ==========================================
# CALCULATIONS
# ==========================================

df["Total"] = df[subjects].sum(axis=1)

df["Average"] = np.round(
    df[subjects].mean(axis=1),
    2
)

df["Result"] = np.where(
    df["Average"] >= 40,
    "Pass",
    "Fail"
)

class_average = round(
    df["Average"].mean(),
    2
)

topper = df.loc[
    df["Average"].idxmax(),
    "Name"
]

pass_rate = round(
    (df["Result"] == "Pass").mean() * 100,
    2
)


# ==========================================
# CSS
# ==========================================

css = """

.gradio-container {
    max-width: 1200px !important;
    margin: auto !important;
}

.title {
    text-align: center;
    padding: 20px;
}

.title h1 {
    font-size: 36px;
    margin-bottom: 5px;
}

.kpi {
    text-align: center;
    padding: 18px;
    border-radius: 12px;
}

footer {
    display: none !important;
}

"""


# ==========================================
# STUDENT ANALYSIS
# ==========================================

def student_analysis(student):

    row = df[df["Name"] == student].iloc[0]

    values = [
        row[subject]
        for subject in subjects
    ]

    best_subject = subjects[
        np.argmax(values)
    ]

    information = f"""
## 🎓 {student}'s Performance

| Metric | Value |
|---|---:|
| **Total Marks** | {int(row["Total"])} |
| **Average** | {row["Average"]}% |
| **Result** | {row["Result"]} |
| **Best Subject** | {best_subject} |
"""

    fig, ax = plt.subplots(
        figsize=(8, 4.5)
    )

    ax.bar(
        subjects,
        values
    )

    ax.set_title(
        f"{student} - Subject Performance",
        fontsize=16,
        fontweight="bold"
    )

    ax.set_ylabel("Marks")
    ax.set_ylim(0, 100)

    for i, value in enumerate(values):

        ax.text(
            i,
            value + 2,
            str(value),
            ha="center",
            fontweight="bold"
        )

    plt.tight_layout()

    return information, fig


# ==========================================
# SUBJECT AVERAGE CHART
# ==========================================

def subject_analysis():

    averages = df[subjects].mean()

    fig, ax = plt.subplots(
        figsize=(7, 4)
    )

    ax.bar(
        averages.index,
        averages.values
    )

    ax.set_title(
        "Average Performance by Subject",
        fontsize=15,
        fontweight="bold"
    )

    ax.set_ylabel("Average Marks")
    ax.set_ylim(0, 100)

    for i, value in enumerate(
        averages.values
    ):

        ax.text(
            i,
            value + 2,
            f"{value:.1f}",
            ha="center",
            fontweight="bold"
        )

    plt.tight_layout()

    return fig


# ==========================================
# STUDENT AVERAGE CHART
# ==========================================

def student_average_chart():

    sorted_df = df.sort_values(
        "Average",
        ascending=False
    )

    fig, ax = plt.subplots(
        figsize=(8, 4)
    )

    ax.bar(
        sorted_df["Name"],
        sorted_df["Average"]
    )

    ax.set_title(
        "Student Average Performance",
        fontsize=15,
        fontweight="bold"
    )

    ax.set_ylabel("Average Marks")
    ax.set_ylim(0, 100)

    plt.tight_layout()

    return fig


# ==========================================
# HEATMAP
# ==========================================

def performance_heatmap():

    fig, ax = plt.subplots(
        figsize=(9, 5)
    )

    sns.heatmap(
        df.set_index("Name")[subjects],
        annot=True,
        fmt=".0f",
        cmap="Blues",
        vmin=0,
        vmax=100,
        linewidths=0.5,
        ax=ax
    )

    ax.set_title(
        "Student Performance Heatmap",
        fontsize=16,
        fontweight="bold"
    )

    ax.set_xlabel("Subjects")
    ax.set_ylabel("Students")

    plt.tight_layout()

    return fig


# ==========================================
# GRADIO DASHBOARD
# ==========================================

with gr.Blocks(
    title="Student Performance Analyzer",
    css=css
) as app:

    # ======================================
    # HEADER
    # ======================================

    gr.HTML("""
    <div class="title">
        <h1>🎓 Student Performance Analyzer</h1>
    </div>
    """)


    # ======================================
    # KPI CARDS
    # ======================================

    with gr.Row():

        with gr.Column(
            elem_classes="kpi"
        ):
            gr.Markdown(
                f"""
                ### 👨‍🎓 {len(df)}
                **Students**
                """
            )

        with gr.Column(
            elem_classes="kpi"
        ):
            gr.Markdown(
                f"""
                ### 📊 {class_average}%
                **Class Average**
                """
            )

        with gr.Column(
            elem_classes="kpi"
        ):
            gr.Markdown(
                f"""
                ### 🏆 {topper}
                **Topper**
                """
            )

        with gr.Column(
            elem_classes="kpi"
        ):
            gr.Markdown(
                f"""
                ### ✅ {pass_rate}%
                **Pass Rate**
                """
            )


    gr.Markdown("---")


    # ======================================
    # STUDENT ANALYSIS
    # ======================================

    gr.Markdown(
        "## 👤 Student Analysis"
    )

    with gr.Row():

        with gr.Column(
            scale=1
        ):

            student_dropdown = gr.Dropdown(
                choices=df["Name"].tolist(),
                value="Aarav",
                label="Select Student"
            )

            analyze_button = gr.Button(
                "🔍 Analyze Student",
                variant="primary"
            )

        with gr.Column(
            scale=2
        ):

            student_info = gr.Markdown(
                "Select a student and click **Analyze Student**."
            )


    student_chart = gr.Plot(
        label="Student Performance",
        format="png"
    )


    analyze_button.click(
        fn=student_analysis,
        inputs=student_dropdown,
        outputs=[
            student_info,
            student_chart
        ]
    )


    gr.Markdown("---")


    # ======================================
    # CLASS PERFORMANCE
    # ======================================

    gr.Markdown(
        "## 📊 Class Performance"
    )

    with gr.Row():

        with gr.Column():

            gr.Markdown(
                "### Subject-wise Average"
            )

            gr.Plot(
                value=subject_analysis,
                format="png",
                show_label=False
            )

        with gr.Column():

            gr.Markdown(
                "### Student-wise Average"
            )

            gr.Plot(
                value=student_average_chart,
                format="png",
                show_label=False
            )


    gr.Markdown("---")


    # ======================================
    # HEATMAP
    # ======================================

    gr.Markdown(
        "## 🔥 Performance Heatmap"
    )

    gr.Plot(
        value=performance_heatmap,
        format="png",
        show_label=False
    )


    gr.Markdown("---")


    # ======================================
    # DATASET
    # ======================================

    gr.Markdown(
        "## 📋 Complete Student Dataset"
    )

    gr.Dataframe(
        value=df,
        interactive=False
    )


# ==========================================
# RUN APP
# ==========================================

if __name__ == "__main__":

    app.launch()