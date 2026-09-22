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

    "Python": [
        85, 78, 65, 90,
        88, 72, 95, 70
    ],

    "NumPy": [
        80, 82, 60, 85,
        90, 68, 92, 75
    ],

    "Pandas": [
        88, 75, 70, 92,
        85, 74, 96, 78
    ],

    "Mathematics": [
        75, 80, 62, 88,
        91, 70, 89, 73
    ]
}


# ==========================================
# CREATE DATAFRAME
# ==========================================

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
.title {
    text-align: center;
    margin-bottom: 20px;
}

.kpi {
    text-align: center;
    padding: 15px;
    border-radius: 12px;
    background: #f5f5f5;
}

footer {
    display: none !important;
}
"""


# ==========================================
# STUDENT ANALYSIS FUNCTION
# ==========================================

def student_analysis(student):

    row = df[
        df["Name"] == student
    ].iloc[0]

    values = [
        row[subject]
        for subject in subjects
    ]

    best_subject = subjects[
        np.argmax(values)
    ]

    information = f"""
## 👤 Student Information

**Student:** {student}

**Average:** {row["Average"]}

**Total Marks:** {row["Total"]}

**Result:** {row["Result"]}

**Best Subject:** {best_subject}
"""

    fig, ax = plt.subplots(
        figsize=(8, 4)
    )

    ax.bar(
        subjects,
        values
    )

    ax.set_ylim(
        0,
        100
    )

    ax.set_title(
        f"{student}'s Subject Performance"
    )

    ax.set_xlabel(
        "Subjects"
    )

    ax.set_ylabel(
        "Marks"
    )

    plt.xticks(
        rotation=20
    )

    plt.tight_layout()

    return information, fig


# ==========================================
# SUBJECT PERFORMANCE
# ==========================================

def subject_analysis():

    averages = df[
        subjects
    ].mean()

    fig, ax = plt.subplots(
        figsize=(8, 4)
    )

    ax.bar(
        subjects,
        averages
    )

    ax.set_ylim(
        0,
        100
    )

    ax.set_title(
        "Average Performance by Subject"
    )

    ax.set_xlabel(
        "Subjects"
    )

    ax.set_ylabel(
        "Average Marks"
    )

    plt.xticks(
        rotation=20
    )

    plt.tight_layout()

    return fig


# ==========================================
# STUDENT AVERAGE CHART
# ==========================================

def student_average_chart():

    fig, ax = plt.subplots(
        figsize=(8, 4)
    )

    ax.bar(
        df["Name"],
        df["Average"]
    )

    ax.set_ylim(
        0,
        100
    )

    ax.set_title(
        "Student Average Performance"
    )

    ax.set_xlabel(
        "Students"
    )

    ax.set_ylabel(
        "Average Marks"
    )

    plt.xticks(
        rotation=30
    )

    plt.tight_layout()

    return fig


# ==========================================
# HEATMAP
# ==========================================

def performance_heatmap():

    fig, ax = plt.subplots(
        figsize=(8, 5)
    )

    sns.heatmap(
        df[subjects],
        annot=True,
        cmap="coolwarm",
        vmin=0,
        vmax=100,
        ax=ax
    )

    ax.set_title(
        "Student Performance Heatmap"
    )

    plt.tight_layout()

    return fig


# ==========================================
# GRADIO DASHBOARD
# ==========================================

demo = gr.Blocks(
    title="Student Performance Analyzer"
)


with demo:

    # ======================================
    # HEADER
    # ======================================

    gr.HTML(
        """
        <div class="title">
            <h1>🎓 Student Performance Analyzer</h1>
            <p>
                Analyze and visualize student academic performance
            </p>
        </div>
        """
    )


    # ======================================
    # KPI CARDS
    # ======================================

    with gr.Row():

        with gr.Column():

            gr.Markdown(
                f"""
                ### 👨‍🎓 Number of Students

                # {len(df)}
                """
            )


        with gr.Column():

            gr.Markdown(
                f"""
                ### 📊 Class Average

                # {class_average}
                """
            )


        with gr.Column():

            gr.Markdown(
                f"""
                ### 🏆 Topper

                # {topper}
                """
            )


        with gr.Column():

            gr.Markdown(
                f"""
                ### ✅ Pass Rate

                # {pass_rate}%
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

        with gr.Column():

            student_dropdown = gr.Dropdown(
                choices=df["Name"].tolist(),
                value=df["Name"].iloc[0],
                label="Select Student"
            )

            analyze_button = gr.Button(
                "Analyze Student",
                variant="primary"
            )


        with gr.Column():

            student_info = gr.Markdown()


    student_chart = gr.Plot(
        label="Student Performance"
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
        "## 📚 Class Performance"
    )


    with gr.Row():

        subject_chart = gr.Plot(
            label="Subject Performance"
        )

        average_chart = gr.Plot(
            label="Student Average"
        )


    gr.Markdown("---")


    # ======================================
    # HEATMAP
    # ======================================

    gr.Markdown(
        "## 🔥 Performance Heatmap"
    )


    heatmap = gr.Plot(
        label="Performance Heatmap"
    )


    gr.Markdown("---")


    # ======================================
    # COMPLETE DATASET
    # ======================================

    gr.Markdown(
        "## 📋 Complete Student Dataset"
    )


    gr.Dataframe(
        value=df,
        interactive=False,
        label="Student Performance Data"
    )


    # ======================================
    # LOAD INITIAL CHARTS
    # ======================================

    demo.load(
        fn=subject_analysis,
        inputs=None,
        outputs=subject_chart
    )


    demo.load(
        fn=student_average_chart,
        inputs=None,
        outputs=average_chart
    )


    demo.load(
        fn=performance_heatmap,
        inputs=None,
        outputs=heatmap
    )


# ==========================================
# RUN APP
# ==========================================

if __name__ == "__main__":

    demo.launch(
        css=css
    )