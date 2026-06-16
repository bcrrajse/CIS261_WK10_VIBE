#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

DATA_FILE = Path("student_grades.txt")

@dataclass
class Student:
    name: str
    student_id: str
    test1: float
    test2: float
    test3: float
    average: float = field(init=False)
    grade: str = field(init=False)

    def __post_init__(self) -> None:
        self.average = self.calculate_average()
        self.grade = self.calculate_grade()

    def calculate_average(self) -> float:
        return round((self.test1 + self.test2 + self.test3) / 3.0, 2)

    def calculate_grade(self) -> str:
        if self.average >= 90:
            return "A"
        if self.average >= 80:
            return "B"
        if self.average >= 70:
            return "C"
        if self.average >= 60:
            return "D"
        return "F"

    def to_record(self) -> str:
        return (
            f"{self.name}|{self.student_id}|"
            f"{self.test1:.2f}|{self.test2:.2f}|{self.test3:.2f}|"
            f"{self.average:.2f}|{self.grade}"
        )

    @staticmethod
    def from_record(line: str) -> Optional["Student"]:
        parts = [part.strip() for part in line.split("|")]
        if len(parts) != 7:
            return None
        try:
            name, student_id, test1, test2, test3, average, grade = parts
            student = Student(name, student_id, float(test1), float(test2), float(test3))
            if f"{student.average:.2f}" != f"{float(average):.2f}" or student.grade != grade:
                return None
            return student
        except ValueError:
            return None


def load_students() -> List[Student]:
    students: List[Student] = []
    if not DATA_FILE.exists():
        return students

    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            for line_number, line in enumerate(file, start=1):
                line = line.strip()
                if not line:
                    continue
                student = Student.from_record(line)
                if student is None:
                    print(f"Warning: Skipped invalid record on line {line_number}.")
                    continue
                students.append(student)
    except OSError as error:
        print(f"Error loading records: {error}")
    return students


def save_students(students: List[Student]) -> None:
    try:
        with DATA_FILE.open("w", encoding="utf-8") as file:
            for student in students:
                file.write(student.to_record() + "\n")
    except OSError as error:
        print(f"Error saving records: {error}")


def get_float(prompt: str) -> float:
    while True:
        value = input(prompt).strip()
        if value.upper() == "ESC":
            raise KeyboardInterrupt
        try:
            number = float(value)
            if number < 0 or number > 100:
                print("Please enter a score between 0 and 100.")
                continue
            return number
        except ValueError:
            print("Invalid input. Enter a numeric score or ESC to cancel.")


def add_student(students: List[Student]) -> None:
    print("\nAdd New Student Record")
    print("Enter ESC at any prompt to cancel.")
    try:
        name = input("Student name: ").strip()
        if not name or name.upper() == "ESC":
            print("Add student cancelled.")
            return

        student_id = input("Student ID: ").strip()
        if not student_id or student_id.upper() == "ESC":
            print("Add student cancelled.")
            return

        test1 = get_float("Test 1 score: ")
        test2 = get_float("Test 2 score: ")
        test3 = get_float("Test 3 score: ")
    except KeyboardInterrupt:
        print("Add student cancelled.")
        return

    student = Student(name, student_id, test1, test2, test3)
    students.append(student)
    print(f"Student '{student.name}' added with average {student.average:.2f} and grade {student.grade}.")


def display_students(students: List[Student]) -> None:
    if not students:
        print("\nNo student records available.")
        return

    print("\nStudent Records")
    print("{:<20} {:<12} {:>7} {:>7} {:>7} {:>9} {:>6}".format(
        "Name", "ID", "Test 1", "Test 2", "Test 3", "Average", "Grade"
    ))
    print("-" * 72)
    for student in students:
        print(
            f"{student.name:<20} {student.student_id:<12} "
            f"{student.test1:7.2f} {student.test2:7.2f} {student.test3:7.2f} "
            f"{student.average:9.2f} {student.grade:>6}"
        )


def display_statistics(students: List[Student]) -> None:
    if not students:
        print("\nNo students to calculate statistics.")
        return

    averages = [student.average for student in students]
    highest = max(averages)
    lowest = min(averages)
    class_average = sum(averages) / len(averages)

    print("\nClass Statistics")
    print(f"Highest average: {highest:.2f}")
    print(f"Lowest average:  {lowest:.2f}")
    print(f"Class average:   {class_average:.2f}")


def search_student(students: List[Student]) -> None:
    if not students:
        print("\nNo student records available.")
        return

    query = input("Enter student name to search: ").strip()
    if not query:
        print("Search cancelled.")
        return

    matches = [student for student in students if query.lower() in student.name.lower()]
    if not matches:
        print(f"No students found matching '{query}'.")
        return

    print(f"\nFound {len(matches)} matching record(s):")
    display_students(matches)


def print_menu() -> None:
    print("\nStudent Grade Calculator")
    print("1. Add new student record")
    print("2. Display all student records")
    print("3. Display class statistics")
    print("4. Search student by name")
    print("ESC. Exit program")


def main() -> None:
    students = load_students()
    if students:
        print(f"Loaded {len(students)} record(s) from '{DATA_FILE}'.")
    else:
        print("No existing student records found. Starting fresh.")

    while True:
        print_menu()
        choice = input("Choose an option: ").strip()
        if not choice:
            continue

        if choice.upper() == "ESC":
            print("Saving records and exiting...")
            save_students(students)
            break

        if choice == "1":
            add_student(students)
            continue
        if choice == "2":
            display_students(students)
            continue
        if choice == "3":
            display_statistics(students)
            continue
        if choice == "4":
            search_student(students)
            continue

        print("Invalid selection. Enter 1-4 or ESC to exit.")

    print("Goodbye.")


if __name__ == "__main__":
    main()
