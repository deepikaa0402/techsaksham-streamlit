import streamlit as st
import sqlite3
from streamlit_option_menu import option_menu

def connectDB():
    return sqlite3.connect("mydatabase.db")

def createTable():
    with connectDB() as con:
        cur = con.cursor()
        cur.execute("create table IF NOT exists students(name text, password text, roll int primary key, branch text)")
        con.commit()

def addRec(data):
    createTable()
    with connectDB() as con:
        cur = con.cursor()
        try:
            cur.execute("insert into students(name, password, roll, branch) values(?,?,?,?)", data)
            con.commit()
        except sqlite3.IntegrityError:
            st.error("Already registered")

def display():
    with connectDB() as conn:
        cur = conn.cursor()
        cur.execute("select * from students")
        result = cur.fetchall()
        if result:
            print(st.table(result))
        else:
            st.write("No records found.")

def resetPassword():
    st.title("Reset Password")
    roll = st.number_input("Enter Roll No", format="%0.0f")
    new_pwd = st.text_input("Enter New Password", type="password")
    if st.button("Reset"):
        with connectDB() as con:
            cur = con.cursor()
            cur.execute("update students set password=? where roll=?", (new_pwd, roll))
            con.commit()
            st.success("Password Reset Successfully")

def filterByBranch():
    st.title("Filter by Branch")
    branch = st.selectbox("Select Branch", ['CSE', "AIML", "ECE"])
    with connectDB() as conn:
        cur = conn.cursor()
        cur.execute("select * from students where branch=?", (branch,))
        result = cur.fetchall()
        if result:
            print(st.table(result))
        else:
            st.write("No records found for this branch.")

def searchByRoll():
    st.title("Search Student")
    roll = st.number_input("Enter Roll No", format="%0.0f")
    if st.button("Search by roll"):
        with connectDB() as conn:
            cur = conn.cursor()
            cur.execute("select * from students where roll=?", (roll,))
            result = cur.fetchone()
            if result:
                st.write("Student Details:", result)
            else:
                st.error("No student found.")

def deleteRecord():
    st.title("Delete Record")
    roll = st.number_input("Enter Roll No to delete: ", format="%0.0f")
    if st.button("Delete"):
        with connectDB() as con:
            cur = con.cursor()
            cur.execute("delete from students where roll=?", (roll,))
            con.commit()
            st.success("Record Deleted Successfully")

def signup():
    st.title("Signup Page")
    name = st.text_input("Enter Name")
    pwd = st.text_input("Enter Password", type='password')
    rePwd = st.text_input("Re-enter Password", type='password')
    roll = st.number_input("Enter Roll No", format="%0.0f")
    branch = st.selectbox("Choose Your Branch", ['CSE', "AIML", "ECE"])
    data = [name, pwd, roll, branch]
    if st.button('Sign Up'):
        if pwd != rePwd:
            st.warning("Passwords do not match")
        else:
            addRec(data)
            st.success("Signup Successful")

with st.sidebar:
    selected = option_menu("Options:", ["SignUp", "Display All Records", "Reset Password", "Filter by Branch", "Search by Roll", "Delete Record"])

if selected == "SignUp":
    signup()
elif selected == "Display All Records":
    display()
elif selected == "Reset Password":
    resetPassword()
elif selected == "Filter by Branch":
    filterByBranch()
elif selected == "Search by Roll":
    searchByRoll()
elif selected == "Delete Record":
    deleteRecord()
