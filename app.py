from flask import Flask,render_template,request,redirect
import sqlite3


app = Flask(__name__)


allowed_colleges=[
"Anna University",
"IIT Madras",
"VIT University",
"SRM University",
"Saveetha Engineering College",
"Rajalakshmi Engineering College",
"Bitm collage",
"Other"
]


fake_words=[
"registration fee",
"pay money",
"investment",
"telegram",
"whatsapp only",
"guaranteed job",
"earn huge",
"no experience",
"urgent hiring"
]



def database():

    con=sqlite3.connect("database.db")

    cur=con.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
    name TEXT,
    phone TEXT,
    email TEXT,
    college TEXT
    )
    """)

    con.commit()
    con.close()



database()



@app.route("/")
def splash():

    return render_template("splash.html")



@app.route("/register",methods=["GET","POST"])
def register():


    if request.method=="POST":

        name=request.form["name"]
        phone=request.form["phone"]
        email=request.form["email"]
        college=request.form["college"]


        if college not in allowed_colleges:

            return "College not approved"


        con=sqlite3.connect("database.db")

        cur=con.cursor()

        cur.execute(
        "INSERT INTO users VALUES(?,?,?,?)",
        (name,phone,email,college)
        )

        con.commit()

        con.close()


        return redirect("/dashboard")


    return render_template(
    "register.html",
    colleges=allowed_colleges
    )




@app.route("/dashboard",methods=["GET","POST"])
def dashboard():


    result=""

    if request.method=="POST":

        job=request.form["job"].lower()

        score=0


        for word in fake_words:

            if word in job:
                score+=10



        if score>=30:
            result="❌ Fake Job Detected"

        elif score>=10:
            result="⚠️ Suspicious Offer"

        else:
            result="✅ Genuine Looking"



    internships=[

    "Google AI Internship",
    "Microsoft Student Internship",
    "AI Research Internship"

    ]


    jobs=[

    "Python Developer",
    "AI Engineer",
    "Data Analyst"

    ]


    return render_template(
    "dashboard.html",
    result=result,
    internships=internships,
    jobs=jobs
    )




app.run(debug=True)