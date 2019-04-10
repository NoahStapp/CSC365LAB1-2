import pandas as pd
import numpy as np
import itertools


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
            for i in range(0, 7):
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


if __name__ == "__main__":
    main()
