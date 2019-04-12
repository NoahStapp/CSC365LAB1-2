import pandas as pd
import numpy as np
import itertools
import math


class Student:
    def __init__(self, lastName, firstName, grade, classroom, bus, GPA):
        self.lastName = lastName
        self.firstName = firstName
        self.grade = grade
        self.classroom = classroom
        self.bus = bus
        self.GPA = GPA


class Teacher:
    def __init__(self, lastName, firstName, classroom):
        self.lastName = lastName
        self.firstName = firstName
        self.classroom = classroom


def createStudents(inputFile):
    students = pd.read_csv(inputFile, header=None, delimiter=", ", engine="python")

    students.columns = ["lastName", "firstName", "grade", "classroom", "bus", "GPA"]
    return students


def createTeachers(inputFile):
    teachers = pd.read_csv(inputFile, header=None, delimiter=", ", engine="python")
    teachers.columns = ["lastName", "firstName", "classroom"]

    return teachers


def main():
    students = createStudents("list.txt")
    teachers = createTeachers("teachers.txt")

    while 1:
        user_input = input("").split(" ")

        if user_input[0] == "Q" or user_input[0] == "Quit":
            break
        elif (user_input[0] == "S:" or user_input[0] == "Student:") and user_input[
            1
        ].isalpha():
            if len(user_input) == 2:
                studentInfo(students, teachers, user_input[1].upper())
            else:
                studentInfoBusRoute(students, user_input[1].upper())
        elif (user_input[0] == "T:" or user_input[0] == "Teacher:") and user_input[
            1
        ].isalpha():
            teacherStudents(students, teachers, user_input[1].upper())
        elif (user_input[0] == "B:" or user_input[0] == "Bus:") and user_input[
            1
        ].isnumeric():
            busRoute(students, int(user_input[1]))
        elif (
            user_input[0] == "A:"
            or user_input[0] == "Average:"
            and user_input[1].isnumeric()
        ):
            avgGradeLevel(students, int(user_input[1]))
        elif user_input[0] == "I" or user_input[0] == "Info":
            for i in [1, 2, 3, 4, 6]:
                studentsPerGrade(students, i)
        elif (user_input[0] == "G:" or user_input[0] == "Grade:") and user_input[
            1
        ].isnumeric():
            if len(user_input) == 3:
                if user_input[2] == "H" or user_input[2] == "High":
                    minMaxGradeLevel(students, teachers, int(user_input[1]), "max")
                elif user_input[2] == "L" or user_input[2] == "Low":
                    minMaxGradeLevel(students, teachers, int(user_input[1]), "min")
            else:
                gradeLevel(students, int(user_input[1]))
        elif (
            user_input[0] == "G:"
            or user_input[0] == "Grade:"
            and (user_input[1] == "Teachers" or user_input[1] == "T")
        ):
            teachersPerGrade(students, teachers, int(user_input[2]))
        elif user_input[0] == "C:" or user_input[0] == "Classroom:":
            if user_input[1] == "Students" or user_input[1] == "S":
                studentsPerClassroom(students, teachers, int(user_input[2]))
            elif user_input[1] == "Teachers" or user_input[1] == "T":
                teachersPerClassroom(students, teachers, int(user_input[2]))
        elif user_input[0] == "E" or user_input[0] == "Enrollment":
            enrollmentByClassroom(students, teachers)
        elif (user_input[0] == "R:" or user_input[0] == "RangeQuartiles:") and len(
            user_input
        ) == 2:
            if user_input[1] == "G" or user_input[1] == "Grade":
                IQR(students, teachers, "grade")
            if user_input[1] == "B" or user_input[1] == "Bus":
                IQR(students, teachers, "bus")
            if user_input[1] == "T" or user_input[1] == "Teacher":
                IQR(students, teachers, "teacher")
        elif (user_input[0] == "D:" or user_input[0] == "Deviation:") and len(
            user_input
        ) == 2:
            if user_input[1] == "G" or user_input[1] == "Grade":
                standardDeviation(students, teachers, "grade")
            elif user_input[1] == "B" or user_input[1] == "Bus":
                standardDeviation(students, teachers, "bus")
            elif user_input[1] == "T" or user_input[1] == "Teacher":
                standardDeviation(students, teachers, "teacher")
        elif (user_input[0] == "M:" or user_input[0] == "MeanGPA:") and len(
            user_input
        ) == 2:
            if user_input[1] == "G" or user_input[1] == "Grade":
                calculateMeanGPA(students, teachers, "grade")
            elif user_input[1] == "B" or user_input[1] == "Bus":
                calculateMeanGPA(students, teachers, "bus")
            elif user_input[1] == "T" or user_input[1] == "Teacher":
                calculateMeanGPA(students, teachers, "teacher")


def studentInfo(students, teachers, name):
    dataFromStudents = students.loc[students["lastName"] == name][
        ["lastName", "firstName", "grade", "classroom"]
    ].values

    if len(dataFromStudents) > 0:
        dataFromTeachers = teachers.loc[
            teachers["classroom"] == dataFromStudents[0][3]
        ][["lastName", "firstName"]].values

        data = np.r_[dataFromStudents[0], dataFromTeachers[0]]
        print(data)


def studentInfoBusRoute(students, name):
    data = students.loc[students["lastName"] == name][
        ["lastName", "firstName", "bus"]
    ].values
    if len(data) > 0:
        print(data[0])


def teacherStudents(students, teachers, lastName):
    teacherClassroom = teachers.loc[teachers["lastName"] == lastName][
        "classroom"
    ].values

    if len(teacherClassroom) > 0:
        print(
            students.loc[students["classroom"] == teacherClassroom[0]][
                ["lastName", "firstName"]
            ].values
        )


def busRoute(students, busRoute):
    data = students.loc[students["bus"] == busRoute][["lastName", "firstName"]].values
    print(data)


def gradeLevel(students, grade):
    data = students.loc[students["grade"] == grade][["lastName", "firstName"]].values
    print(data)


def avgGradeLevel(students, grade):
    print(students.loc[students["grade"] == grade]["GPA"].mean())


def minMaxGradeLevel(students, teachers, grade, flag):
    if students[students["grade"] == grade].size:
        if flag == "max":
            dataFromStudents = students.loc[
                students.loc[students["grade"] == grade]["GPA"].idxmax()
            ][["lastName", "firstName", "GPA", "bus", "classroom"]].values
            if len(dataFromStudents) > 0:
                dataFromTeachers = teachers.loc[
                    teachers["classroom"] == dataFromStudents[4]
                ][["lastName", "firstName"]].values

                dataFromStudents = np.delete(dataFromStudents, 4)

                data = np.r_[dataFromStudents, dataFromTeachers[0]]
                print(data)
        else:
            dataFromStudents = students.loc[
                students.loc[students["grade"] == grade]["GPA"].idxmin()
            ][["lastName", "firstName", "GPA", "bus", "classroom"]].values
            if len(dataFromStudents) > 0:
                dataFromTeachers = teachers.loc[
                    teachers["classroom"] == dataFromStudents[4]
                ][["lastName", "firstName"]].values

                dataFromStudents = np.delete(dataFromStudents, 4)

                data = np.r_[dataFromStudents, dataFromTeachers[0]]
                print(data)


def studentsPerGrade(students, grade):
    print(grade, ": ", len(students.loc[students["grade"] == grade].values))


# NR-1
def studentsPerClassroom(students, teachers, classroom):
    student = students.loc[students["classroom"] == classroom][
        ["lastName", "firstName"]
    ]
    print(student.values)


# NR-2
def teachersPerClassroom(students, teachers, classroom):
    teacher = teachers.loc[teachers["classroom"] == classroom][
        ["lastName", "firstName"]
    ]
    print(teacher.values)


# NR-3
def teachersPerGrade(students, teachers, grade):
    classrooms = list(set(students[students["grade"] == grade]["classroom"].values))
    print(teachers[teachers["classroom"].isin(classrooms)].values)


# NR-4
def enrollmentByClassroom(students, teachers):
    print(students["classroom"].value_counts().sort_index(ascending=True))


# NR-5, calculate IQR for GPA of an analytic field
def IQR(students, teachers, field):
    if field == "grade":
        print(students.groupby("grade").quantile([0.25, 0.5, 0.75])["GPA"])
    if field == "bus":
        print(students.groupby("bus").quantile([0.25, 0.5, 0.75])["GPA"])
    if field == "teacher":
        complete_df = pd.merge(teachers, students, on="classroom")
        print(
            complete_df.groupby(["lastName_x", "firstName_x"]).quantile(
                [0.25, 0.5, 0.75]
            )["GPA"]
        )


# NR-5, calculate mean GPA of an analytic field
def calculateMeanGPA(students, teachers, field):
    if field == "grade":
        print(students.groupby('grade')['GPA'].mean())
    if field == "bus":
        print(students.groupby('bus')['GPA'].mean())
    if field == "teacher":
        complete_df = pd.merge(teachers, students, on="classroom")
        print(complete_df.groupby(["lastName_x", "firstName_x"])['GPA'].mean())


# NR-5, calculate standard deviation of an analytic field
def standardDeviation(students, teachers, field):
    if field == "grade":
        for i in [1, 2, 3, 4, 6]:
            mean = 0
            standard_deviations = []
            student_gpas = students.loc[students["grade"] == i]["GPA"]
            mean = sum(student_gpas) / len(student_gpas)
            for gpa in student_gpas:
                standard_deviations.append(math.pow(gpa - mean, 2))
            standard_deviation = math.sqrt(
                sum(standard_deviations) / len(standard_deviations)
            )
            print("Standard deviation of grade ", i, ": ", standard_deviation)
    # elif field == "bus":


if __name__ == "__main__":
    main()
