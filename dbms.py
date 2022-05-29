from flask import Flask, render_template, request, redirect, url_for
import psycopg2
conn = psycopg2.connect(database="ABCnew", user='postgres', password='16062002', host='127.0.0.1', port='5432')
cursor=conn.cursor()
app = Flask(__name__)


def cal_bmi(weight,height):
    height=height/100
    bmi = weight/(height**2)
    return bmi

def cal_bmr(age,gender,weight,height):
    if gender=='M':
        bmr = 10*weight + 6.25*height -5*age + 5
    elif gender=='F':
        bmr = 10 * weight + 6.25 * height - 5 * age - 161
    return bmr

def chk_status(bmi):
    if bmi < 16:
        status = "Severely Thin"
    elif 16 <= bmi < 17:
        status = "Moderately Thin"
    elif 17 <= bmi < 18.5:
        status = "Mildly Thin"
    elif 18.5 <= bmi < 25:
        status = "Normal"
    elif 25 <= bmi < 30:
        status = "Overweight"
    elif 30 <= bmi < 35:
        status = "Obese Class 1"
    elif 35 <= bmi < 40:
        status = "Obese Class 2"
    elif bmi>40:
        status = "Obese Class 3"
    return status


# @app.route("/")
# def home():
#     return render_template("home.html")


@app.route("/",methods=["GET","POST"])
def show_rec():
    cursor.execute("select * from student")
    students = cursor.fetchall()
    students.sort()
    return render_template("show.html",students=students)


@app.route("/add_record", methods=["GET","POST"])
def add_rec():
    if request.method == "POST":
        name = request.form['name']
        roll = request.form['roll']
        age = int(request.form['age'])
        gender = request.form['gender']
        weight = int(request.form['weight'])
        height = int(request.form['height'])
        bmi = cal_bmi(weight,height)
        bmr = cal_bmr(age,gender,weight,height)
        status = chk_status(bmi)
        cursor.execute(f"insert into student(rollno,name,age,gender,weight,height,bmi,bmr,status) values('{roll}','{name}','{age}','{gender}','{weight}','{height}','{bmi:.4f}','{bmr}','{status}')")
        conn.commit()
        return redirect(url_for('show_rec'))
    else:
        return render_template("add.html")


@app.route("/update_record", methods=["GET","POST"])
def update_rec():
    if request.method == "POST":
        roll = request.form['roll']
        age = int(request.form['age'])
        weight = int(request.form['weight'])
        height = int(request.form['height'])
        cursor.execute(f"select gender from student where rollno={roll}")
        data=cursor.fetchone()
        bmi = cal_bmi(weight, height)
        bmr = cal_bmr(age, data[0], weight, height)
        status = chk_status(bmi)
        cursor.execute(f"update student set age='{age}',weight='{weight}',height='{height}',bmi='{bmi:.4f}',bmr='{bmr}',status='{status}' where rollno={roll}")
        conn.commit()
        return redirect(url_for('show_rec'))
    else:
        return render_template("update.html")

@app.route("/del_record",methods=["GET","POST"])
def del_rec():
    if request.method == "POST":
        roll = request.form['roll']
        cursor.execute(f"delete from student where rollno={roll}")
        conn.commit()
        return redirect(url_for('show_rec'))
    else:
        return render_template(("delete.html"))

# @app.route("/search_res",methods=["GET","POST"])
# def search():
#     if request.method == "POST":
#         cond = request.form['search']
#         cursor.execute(f"select * from student where name = '{cond}'")
#         search_res = cursor.fetchall()
#         return render_template("home.html", result=search_res, name=cond)
#     else:
#         return redirect(url_for('show_rec'))

if __name__ == '__main__':
    app.run(debug=True)


