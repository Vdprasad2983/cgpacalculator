# 📊 CGPA Calculator Web App (Streamlit + AWS)

This project is a modern, user-friendly **CGPA Calculator** web application built using **Streamlit**. It supports **student registration with photo**, **OTP email verification**, **semester-wise grade entry**, **CGPA & percentage calculation**, and **cloud-based data storage using Amazon S3**.

---

## 🚀 Features

* 🧑‍🎓 User registration with OTP verification (via AWS SES)
* 🖼️ Photo upload or capture via webcam
* 🔐 Login with secure credential matching
* 📝 Semester-wise subject, grade & credit entry
* 📊 Automatic CGPA & percentage calculation
* ✏️ Modify previously entered data
* 📈 Visual summary of academic performance
* ☁️ Data storage in Amazon S3

---

## 🧰 Tech Stack

| Component      | Technology       |
| -------------- | ---------------- |
| Frontend UI    | Streamlit        |
| Backend Logic  | Python           |
| Data Storage   | Amazon S3        |
| Email Service  | AWS SES          |
| Image Encoding | base64           |
| Charting       | Streamlit Charts |
| File Format    | CSV              |

---

## 🗂️ Project Structure

```
📁 your-project-folder/
├── main.py
├── utils/
│   ├── s3_utils.py
│   ├── email_utils.py
│   └── cgpa_utils.py
├── add_modify_see.py
├── README.md
```

---

## 🧑‍💻 How to Run Locally

1. **Clone the repository**:

```bash
git clone <your-repo-url>
cd your-project-folder
```

2. **Install dependencies**:

```bash
pip install -r requirements.txt
```

3. **Setup AWS Credentials**:

* Create an S3 bucket named `cgpa-calculator-streamlit`
* Enable AWS SES in sandbox or production
* Store your access keys in environment variables:

```bash
export AWS_ACCESS_KEY_ID=YOUR_KEY
export AWS_SECRET_ACCESS_KEY=YOUR_SECRET
```

4. **Run the app**:

```bash
streamlit run main.py
```

---

## 📦 Key Functions

### main.py

* Handles user **register/login/dashboard** logic
* Calls respective functions for CGPA entry/modification/visualization

### utils/s3\_utils.py

* Uploads, downloads, and initializes user `.csv` files in S3

### utils/email\_utils.py

* Sends OTP and confirmation emails via AWS SES

### utils/cgpa\_utils.py

* Calculates CGPA and percentage from subject-level data

### add\_modify\_see.py

* UI logic for adding, editing, and viewing academic records

---

## 🛡️ Security Notes

* Use environment variables or `.env` files to hide AWS credentials
* Never hardcode secret keys in your codebase
* Optionally enable Gmail 2FA and use **App Password** (if still using SMTP)

---

## 📬 Contact

For questions or contributions, feel free to raise an issue or contact the project maintainer.

---

✅ Built with love using Streamlit & AWS ☁️
