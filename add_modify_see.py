# add_modify_see.py

import streamlit as st
import pandas as pd
import ast
from utils.s3_utils import read_user_csv_from_s3, write_user_csv_to_s3
from utils.cgpa_utils import calculate_cgpa, calculate_percentage

def add_data(user):
    df = read_user_csv_from_s3(user)
    if df is None:
        st.warning("No record found. Please register first.")
        return

    sems = ["I-I", "I-II", "II-I", "II-II", "III-I", "III-II", "IV-I", "IV-II"]
    existing_sems = df["sem"].tolist()
    available_sems = [sem for sem in sems if sem not in existing_sems]

    if not available_sems:
        st.info("All semesters are already added.")
        return

    sem = st.selectbox("Select Semester", available_sems)
    num = st.slider("Number of Subjects", 1, 10)

    grades = ["A+", "A", "B", "C", "D", "E", "F", "COMPLETED"]
    credits = [3.0, 1.5, 2.0, 4.0, 8.0, 0.0]

    names, grade_list, credit_list, actual_list = [], [], [], []

    for i in range(num):
        cols = st.columns(4)
        names.append(cols[0].text_input(f"Subject {i+1}"))
        grade_list.append(cols[1].selectbox(f"Grade {i+1}", grades, key=f"g{i}"))
        credit_list.append(float(cols[2].selectbox(f"Credits {i+1}", credits, key=f"c{i}")))
        actual_list.append(float(cols[3].selectbox(f"Actual Credits {i+1}", credits, key=f"ac{i}")))

    if st.button("Submit Data"):
        cgpa = round(calculate_cgpa(grade_list, credit_list, actual_list), 2)
        perc = calculate_percentage(cgpa)

        new_row = {
            "subject_names": names,
            "grades": grade_list,
            "credits": credit_list,
            "actual_credits": actual_list,
            "sem": sem,
            "grade": cgpa,
            "percentage": perc
        }

        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        write_user_csv_to_s3(user, df)
        st.success(f"Data for {sem} added. CGPA: {cgpa}, Percentage: {perc}%")


def modify_data(user):
    df = read_user_csv_from_s3(user)
    if df is None or df.empty:
        st.warning("No data to modify.")
        return
    sem_order = ["I-I", "I-II", "II-I", "II-II", "III-I", "III-II", "IV-I", "IV-II"]
    # Sort semesters present in df by sem_order
    semesters_present = df["sem"].unique().tolist()
    semesters_sorted = sorted(semesters_present, key=lambda x: sem_order.index(x) if x in sem_order else 99)

    sem = st.selectbox("Select Semester to Modify", semesters_sorted)
    idx = df[df["sem"] == sem].index[0]
    key_ss = f"edit_subjects_{sem}"

    # Initialize edit state from existing data if not present
    if key_ss not in st.session_state:
        try:
            st.session_state[key_ss] = {
                "names": ast.literal_eval(df.at[idx, "subject_names"]),
                "grades": ast.literal_eval(df.at[idx, "grades"]),
                "credits": ast.literal_eval(df.at[idx, "credits"]),
                "actuals": ast.literal_eval(df.at[idx, "actual_credits"]),
            }
        except Exception:
            st.error("Error loading existing data.")
            return

    data = st.session_state[key_ss]

    # Track deletion index
    delete_index = st.session_state.get("delete_index", None)

    # Display subjects with edit controls and delete buttons
    for i, (name, grade, credit, actual) in enumerate(
        zip(data["names"], data["grades"], data["credits"], data["actuals"])
    ):
        cols = st.columns([3, 2, 2, 2, 1])
        data["names"][i] = cols[0].text_input(f"Subject {i+1}", value=name, key=f"edit_name_{sem}_{i}")
        grade_opts = ["A+", "A", "B", "C", "D", "E", "F", "COMPLETED"]
        data["grades"][i] = cols[1].selectbox(
            f"Grade {i+1}", grade_opts,
            index=grade_opts.index(grade),
            key=f"edit_grade_{sem}_{i}"
        )
        credit_opts = [3.0, 1.5, 2.0, 4.0, 8.0, 0.0]
        data["credits"][i] = float(cols[2].selectbox(
            f"Credit {i+1}", credit_opts,
            index=credit_opts.index(credit),
            key=f"edit_credit_{sem}_{i}"
        ))
        data["actuals"][i] = float(cols[3].selectbox(
            f"Actual Credit {i+1}", credit_opts,
            index=credit_opts.index(actual),
            key=f"edit_actual_{sem}_{i}"
        ))
        if cols[4].button("🗑️", key=f"delete_subject_{sem}_{i}"):
            st.session_state["delete_index"] = i
            st.rerun()

    # Perform the deletion immediately after rerun
    if delete_index is not None:
        for key in ["names", "grades", "credits", "actuals"]:
            data[key].pop(delete_index)
        st.session_state["delete_index"] = None
        st.rerun()

    # Button to add a new blank subject row
    if st.button("➕ Add Subject"):
        data["names"].append("")
        data["grades"].append("A+")
        data["credits"].append(3.0)
        data["actuals"].append(3.0)
        st.rerun()

    # Update semester data and save
    if st.button("Update Semester"):
        if not data["names"]:
            st.warning("At least one subject is required.")
            return
        cgpa = round(calculate_cgpa(data["grades"], data["credits"], data["actuals"]), 2)
        perc = calculate_percentage(cgpa)

        df.at[idx, "subject_names"] = data["names"]
        df.at[idx, "grades"] = data["grades"]
        df.at[idx, "credits"] = data["credits"]
        df.at[idx, "actual_credits"] = data["actuals"]
        df.at[idx, "grade"] = cgpa
        df.at[idx, "percentage"] = perc

        write_user_csv_to_s3(user, df)
        st.success(f"Updated {sem} successfully.")
        del st.session_state[key_ss]
        st.rerun()



def see_data(user):
    df = read_user_csv_from_s3(user)
    if df is None or df.empty:
        st.warning("No data found.")
        return

    # Define semester order for sorting
    sem_order = ["I-I", "I-II", "II-I", "II-II", "III-I", "III-II", "IV-I", "IV-II"]
    df["sem_order"] = df["sem"].apply(lambda x: sem_order.index(x) if x in sem_order else 99)
    df = df.sort_values("sem_order")

    # Calculate total credits per semester correctly
    df["total_sem_credits"] = df["actual_credits"].apply(
        lambda x: sum(ast.literal_eval(x)) if isinstance(x, str) else sum(x)
    )

    # Calculate weighted overall CGPA (sum of (SGPA * credits) / total credits)
    numerator = (df["total_sem_credits"] * df["grade"]).sum()
    denominator = df["total_sem_credits"].sum()
    overall_cgpa = numerator / denominator if denominator > 0 else 0.0

    # Calculate overall percentage with university formula
    overall_percentage = (overall_cgpa - 0.75) * 10 if overall_cgpa >= 0.75 else 0.0

    st.title("📄 Semester-wise Results Summary")

    # Show summary table of semester CGPA & Percentage as before
    summary = df[["sem", "grade", "percentage"]].rename(columns={
        "sem": "Semester",
        "grade": "CGPA",
        "percentage": "Percentage (%)"
    })
    summary.set_index("Semester", inplace=True)

    st.dataframe(summary.style.format({"CGPA": "{:.2f}", "Percentage (%)": "{:.2f}"}), height=200)

    # Show overall CGPA and overall percentage metrics
    col1, col2 = st.columns(2)
    col1.metric("🌟 Overall CGPA (Weighted)", f"{overall_cgpa:.2f}")
    col2.metric("📈 Overall Percentage (Weighted)", f"{overall_percentage:.2f}%")

    # CGPA Trend Chart
    st.subheader("📊 CGPA Trend Over Semesters")
    trend_df = df.sort_values("sem_order")[["sem", "grade"]].set_index("sem")
    st.line_chart(trend_df)

    # Detailed subjects info per semester in expandable sections
    for _, row in df.iterrows():
        with st.expander(f"🔎 Details for Semester: {row['sem']}"):
            try:
                subjects = pd.DataFrame({
                    "Subject": ast.literal_eval(row["subject_names"]),
                    "Grade": ast.literal_eval(row["grades"]),
                    "Credits": ast.literal_eval(row["credits"]),
                    "Actual Credits": ast.literal_eval(row["actual_credits"])
                })
                st.table(subjects)
            except Exception as e:
                st.error(f"Error loading subject details: {e}")

            st.markdown(f"**CGPA:** {row['grade']:.2f}    ")
            st.markdown(f"**Percentage:** {row['percentage']:.2f}%")

            # Optional: add a progress bar with percentage
            st.progress(min(int(row['percentage']), 100))



