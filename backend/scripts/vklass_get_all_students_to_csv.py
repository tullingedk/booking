import csv
import requests
from json import load

s = requests.Session()

with open("vklass_credentials.json", "r") as f:
    login = load(f)

s.post("https://auth.vklass.se/credentials/signin", data=login)
r_class_list = s.get(
    "https://www.vklass.se/SchoolClasses.aspx?id=b5bf211e-414f-4403-8321-e1a5569500e1"
)

STUDENTS = []


def every_student(s, student_url, class_name):
    email = None
    name = None

    r = s.get(f"https://www.vklass.se/{student_url}")
    for line in r.text.split("\n"):
        if "ctl00_ContentPlaceHolder2_nameLabel" in line:
            name = line.split("</b>")[1][1:].split("</span>")[0]
        if "ctl00_ContentPlaceHolder2_mailLabel" in line:
            try:
                temp = line.split("E-post:: ")[1].split("</span></li>")[0]
                email = temp
            except Exception:
                pass

    student = {"name": name, "email": email, "class_name": class_name}
    print(student)
    STUDENTS.append(student)


def every_class(s, class_name, class_url):
    r = s.get(f"https://www.vklass.se/{class_url}")
    for line in r.text.split("\n"):
        if "ctl00_ContentPlaceHolder2_studentRepeater_" in line:
            student_url = line.split('href="')[1].split('">')[0]
            every_student(s, student_url, class_name)


for line_class_list in r_class_list.text.split("\n"):
    if "ctl00_ContentPlaceHolder2_classRepeater_" in line_class_list:
        class_url = line_class_list.split('href="')[1].split("&amp;")[0]
        class_name = line_class_list.split('">')[2].split("</a></td>")[0]

        every_class(s, class_name, class_url)


with open("students.csv", mode="w") as file:
    writer = csv.writer(file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)

    for student in STUDENTS:
        writer.writerow(
            [
                student["name"],
                "None" if student["email"] is None else student["email"],
                student["class_name"],
            ]
        )
