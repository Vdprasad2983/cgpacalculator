# utils/cgpa_utils.py

def grade_point(grade):
    mapping = {
        "A+": 10,
        "A": 9,
        "B": 8,
        "C": 7,
        "D": 6,
        "E": 5,
        "F": 0,
        "COMPLETED": 0
    }
    return mapping.get(grade, 0)

def calculate_cgpa(grades, credits, actual_credits):
    try:
        total_points = sum(grade_point(grades[i]) * credits[i] for i in range(len(grades)))
        total_actual = sum(actual_credits)
        if total_actual == 0:
            return 0.0
        return total_points / total_actual
    except Exception:
        return 0.0

def calculate_percentage(cgpa):
    return round((cgpa - 0.75) * 10, 2)
