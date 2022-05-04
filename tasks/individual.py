#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
import sys
from typing import List
import xml.etree.ElementTree as ET


@dataclass(frozen=True)
class Student:
    name: str
    group: int
    grade: str


@dataclass
class Group:
    students: List[Student] = field(default_factory=lambda: [])

    def add(self, name, group, grade):
        self.students.append(
            Student(
                name=name,
                group=group,
                grade=grade,
            )
        )
        self.students.sort(key=lambda student: student.name)

    def __str__(self) -> str:
        # Заголовок таблицы.
        table = []
        line = '+-{}-+-{}-+-{}-+-{}-+'.format(
            '-' * 4,
            '-' * 30,
            '-' * 20,
            '-' * 15
        )
        table.append(line)
        table.append(
            '| {:^4} | {:^30} | {:^20} | {:^15} |'.format(
                "No",
                "Ф.И.О.",
                "Группа",
                "Успеваемость"
            )
        )
        table.append(line)
        # Вывести данные о всех сотрудниках.
        for idx, Student in enumerate(self.students, 1):
            table.append(
                '| {:>4} | {:<30} | {:<20} | {:>15} |'.format(
                    idx,
                    Student.name,
                    Student.group,
                    Student.grade
                )
            )
        table.append(line)
        return '\n'.join(table)

    def select(self):
        count = 0
        result = []
        # Проверить сведения студентов из списка.
        for student in self.students:
            grade = list(map(int, student.grade.split()))
            if sum(grade) / max(len(grade), 1) >= 4.0:
                count += 1
                result.append(student)
            return result

    def load(self, filename):
        with open(filename, "r", encoding="utf-8") as fin:
            xml = fin.read()

            parser = ET.XMLParser(encoding="utf-8")
            tree = ET.fromstring(xml, parser=parser)

            self.students = []
            for student_element in tree:
                name, group, grade = None, None, None

                for element in student_element:
                    if element.tag == 'name':
                        name = element.text
                    elif element.tag == 'group':
                        group = int(element.text)
                    elif element.tag == 'grade':
                        grade = element.text

                    if name is not None and group is not None \
                            and grade is not None:
                        self.students.append(
                            Student(
                                name=name,
                                group=group,
                                grade=grade
                            )
                        )

    def save(self, filename: str) -> None:
        root = ET.Element('students')
        for Student in self.students:
            student_element = ET.Element('Student')

            name_element = ET.SubElement(student_element, 'name')
            name_element.text = Student.name

            post_element = ET.SubElement(student_element, 'group')
            post_element.text = int(Student.group)

            year_element = ET.SubElement(student_element, 'grade')
            year_element.text = Student.grade

            root.append(student_element)

        tree = ET.ElementTree(root)
        with open(filename, "w", encoding="utf-8") as fout:
            tree.write(fout, encoding="utf-8", xml_declaration=True)


if __name__ == '__main__':
    Group = Group()
    while True:
        command = input(">>> ").lower()

        # Выполнить действие в соответствие с командой.
        if command == 'exit':
            break

        elif command == 'add':
            # Запросить данные о студенте.
            name = input("Фамилия и инициалы? ")
            group = int(input("Группа? "))
            grade = input("Оценки ")

            Group.add(name, group, grade)

        elif command == 'list':
            # Вывести список.
            print(Group)

        elif command.startswith('select '):
            parts = command.split(maxsplit=1)
            # Запросить студента.
            selected = Group.select(parts[1])

        elif command.startswith('load '):
            # Разбить команду на части для имени файла.
            parts = command.split(maxsplit=1)
            # Загрузить данные из файла.
            Group.load(parts[1])

        elif command.startswith('save '):
            # Разбить команду на части для имени файла.
            parts = command.split(maxsplit=1)
            # Сохранить данные в файл.
            Group.save(parts[1])

        elif command == 'help':
            # Вывести справку о работе с программой.
            print("Список команд:\n")
            print("add - добавить студента;")
            print("list - вывести список студентов;")
            print("select <1> - запросить студентов со средним баллом >=4;")
            print("load <имя_файла> - загрузить данные из файла;")
            print("save <имя_файла> - сохранить данные в файл;")
            print("help - отобразить справку;")
            print("exit - завершить работу с программой.")

        else:
            print(f"Неизвестная команда {command}", file=sys.stderr)
