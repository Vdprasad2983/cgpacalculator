import streamlit as st 
import pandas as pd
from streamlit_option_menu import option_menu
st.set_page_config(page_title="aditya college",page_icon="🎓",layout="wide")


def ind_sem(data):
    sel=option_menu(menu_title=None,options=["sem-I","sem-II","sem-III","sem-IV","sem-V","sem-VI","sem-VII","sem-VIII"],orientation="horizontal")
    if sel=="sem-I":
        st.dataframe(data[["Roll.No","Student Name","I-I SGPA","I-I Credits","I-I Backlogs"]])
    if sel=="sem-II":
        st.dataframe(data[["Roll.No","Student Name","I-II SGPA","I-II Credits","I-II Backlogs"]])
    if sel=="sem-III":
        st.dataframe(data[["Roll.No","Student Name","II-I SGPA","II-I Credits","II-I Backlogs"]])
    if sel=="sem-IV":
        st.dataframe(data[["Roll.No","Student Name","II-II SGPA","II-II Credits","II-II Backlogs"]])
    if sel=="sem-V":
        st.dataframe(data[["Roll.No","Student Name","III-I SGPA","III-I Credits","III-I Backlogs"]])
    if sel=="sem-VI":
        st.dataframe(data[["Roll.No","Student Name","III-II SGPA","III-II Credits","III-II Backlogs"]])
    if sel=="sem-VII":
        st.dataframe(data[["Roll.No","Student Name","IV-I SGPA","IV-I Credits","IV-I Backlogs"]])
    if sel=="sem-VIII":
        st.dataframe(data[["Roll.No","Student Name","IV-II SGPA","IV-II Credits","IV-II Backlogs"]])

def find_percentage(grade):
    if (grade=="-") or (grade=="0"):
        return "0"
    else:
        return f"{((float(grade)-0.75)*10):.2f}"

def ind_person(roll,data):
    x=data[data["Roll.No"]==roll]
    try:
        col1,col2,col3=st.columns(3)
        col1.write("Roll Number: ")
        col2.write(x.iloc[0][1])
        col1.write("Student Name: ")
        col2.write(x.iloc[0][2])
        
        df=pd.DataFrame([
            {"SEMESTER":"I-I","SGPA":x.iloc[0][3],"CREDITS":x.iloc[0][4],"BACKLOGS":x.iloc[0][5],"PERCENTAGE":find_percentage(x.iloc[0][3])},
            {"SEMESTER":"I-II","SGPA":x.iloc[0][6],"CREDITS":x.iloc[0][7],"BACKLOGS":x.iloc[0][8],"PERCENTAGE":find_percentage(x.iloc[0][6])},
            {"SEMESTER":"II-I","SGPA":x.iloc[0][9],"CREDITS":x.iloc[0][10],"BACKLOGS":x.iloc[0][11],"PERCENTAGE":find_percentage(x.iloc[0][9])},
            {"SEMESTER":"II-II","SGPA":x.iloc[0][12],"CREDITS":x.iloc[0][13],"BACKLOGS":x.iloc[0][14],"PERCENTAGE":find_percentage(x.iloc[0][12])},
            {"SEMESTER":"III-I","SGPA":x.iloc[0][15],"CREDITS":x.iloc[0][16],"BACKLOGS":x.iloc[0][17],"PERCENTAGE":find_percentage(x.iloc[0][15])},
            {"SEMESTER":"III-II","SGPA":x.iloc[0][18],"CREDITS":x.iloc[0][19],"BACKLOGS":x.iloc[0][20],"PERCENTAGE":find_percentage(x.iloc[0][18])},
            {"SEMESTER":"IV-I","SGPA":x.iloc[0][21],"CREDITS":x.iloc[0][22],"BACKLOGS":x.iloc[0][23],"PERCENTAGE":find_percentage(x.iloc[0][21])},
            {"SEMESTER":"IV-II","SGPA":x.iloc[0][24],"CREDITS":x.iloc[0][25],"BACKLOGS":x.iloc[0][26],"PERCENTAGE":find_percentage(x.iloc[0][24])},
            {"SEMESTER":"Total CGPA","SGPA":x.iloc[0][27],"CREDITS":x.iloc[0][28],"BACKLOGS":x.iloc[0][29],"PERCENTAGE":x.iloc[0][30]}
        ])
        st.table(df)
    except IndexError:
        st.error("please enter the roll number in the range")

def cus_person(roll,data):
    x=data.loc[data["Roll.No"].isin(roll)]
    # st.dataframe(x)
    columns=["Roll.No","Student Name","I-I SGPA","I-II SGPA","II-I SGPA","II-II SGPA","III-I SGPA","III-II SGPA","IV-I SGPA","IV-II SGPA","CGPA","Total Credits","Total Backlogs","Percentage"]
    col1,col2,col3=st.columns(3)
    sort_by = col1.selectbox("Sort by column", columns)
    ascending = col1.checkbox("Show in Ascending order", value=False)
    sorted_df = x.sort_values(by=sort_by, ascending=ascending)
    static_df = sorted_df.copy()
    static_df.insert(0, 'S.No', range(1, len(static_df) + 1))
    if x.empty:
        st.info("select atleast one roll number")
    else:
        st.dataframe(static_df[["S.No","Roll.No","Student Name","I-I SGPA","I-II SGPA","II-I SGPA","II-II SGPA","III-I SGPA","III-II SGPA","IV-I SGPA","IV-II SGPA","CGPA","Total Credits","Total Backlogs","Percentage"]],hide_index=True)


def innermain(data):
    select=option_menu(menu_title=None,options=["Search List","Custom List","Entire List","Show by Semester"],icons=["search","list-task","award","sliders"],orientation="horizontal")
    if select=="Search List":
        data1=list(data["Roll.No"])
        roll=st.selectbox("select your roll number",options=data1)
        if st.button("submit"):
            ind_person(roll,data)
    if select=="Custom List":
        data1=list(data["Roll.No"])
        roll=st.multiselect("Select the students roll numbers",options=data1)
        cus_person(roll,data)
    if select=="Entire List":
        columns=["Roll.No","Student Name","I-I SGPA","I-II SGPA","II-I SGPA","II-II SGPA","III-I SGPA","III-II SGPA","IV-I SGPA","IV-II SGPA","CGPA","Total Credits","Total Backlogs","Percentage"]
        col1,col2,col3=st.columns(3)
        sort_by = col1.selectbox("Sort by column", columns)
        ascending = col1.checkbox("Show in Ascending order", value=False)
        sorted_df = data.sort_values(by=sort_by, ascending=ascending)
        static_df = sorted_df.copy()
        static_df.insert(0, 'S.No', range(1, len(static_df) + 1))
        st.dataframe(static_df[["S.No","Roll.No","Student Name","I-I SGPA","I-II SGPA","II-I SGPA","II-II SGPA","III-I SGPA","III-II SGPA","IV-I SGPA","IV-II SGPA","CGPA","Total Credits","Total Backlogs","Percentage"]], hide_index=True, use_container_width=True)
        
    if select=="Show by Semester":
        ind_sem(data)
                        

if st.session_state.college=="Aditya College of Engineering and Technology":
    
    st.sidebar.success(f"Logged in as {st.session_state.username}")
    if st.sidebar.button("Logout"):
        for key in ["auth", "username", "otp", "otp_verified", "otp_entered","college"]:
            st.session_state[key] = None if key != "auth" else 0
        st.rerun()
    selection=option_menu(menu_title=None,options=["A Sec","B Sec","C Sec","D Sec","E Sec","F Sec","G Sec","H Sec"],orientation="horizontal")
    if selection=="A Sec":
        data=pd.read_excel("A section results.xlsx")
        innermain(data)
    if selection=="B Sec":
        data=pd.read_excel("B section results.xlsx")
        innermain(data)
    if selection=="C Sec":
        data=pd.read_excel("C section results.xlsx")
        innermain(data)
    if selection=="D Sec":
        data=pd.read_excel("D section results.xlsx")
        innermain(data)
    if selection=="E Sec":
        data=pd.read_excel("E section results.xlsx")
        innermain(data)
    if selection=="F Sec":
        data=pd.read_excel("F section results.xlsx")
        innermain(data)
    if selection=="G Sec":
        data=pd.read_excel("G section results.xlsx")
        innermain(data)
    if selection=="H Sec":
        data=pd.read_excel("H section results.xlsx")
        innermain(data)
else:
    st.error("This page is only for aditya ece students only (P3 & MH) or else login to your details")
