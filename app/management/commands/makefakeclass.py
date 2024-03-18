from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from faker import Faker

from accounts.models import MyUser
from app.models.course import Course
from app.models.section import Section
from app.models.course_member import CourseMember, UserRole


class Command(BaseCommand):
    help = "Creates a fake class of CourseMembers (students)"

    def add_arguments(self, parser):
        parser.add_argument("course_id", type=int, help="The course id")
        parser.add_argument("num_students", type=int, help="Number of students")
        parser.add_argument("num_sections", type=int, help="Number of sections")

    def create_course(self, course_id: int) -> Course:
        faker = Faker()
        course_name = (
            faker.word(
                ext_word_list=["COSC", "BIO", "MATH", "PYSO", "HEAL"]
            ).capitalize()
            + " "
            + str(course_id)
        )
        course, created = Course.objects.get_or_create(
            id=course_id, defaults={"name": course_name}
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Course "{course_name}" created.'))
        return course

    def create_section(self, course: Course, section_number: int) -> Section:
        faker = Faker()
        section_name = (
            faker.word(ext_word_list=["Lab", "Tutorial", "Seminar"])
            + " "
            + str(section_number)
        )
        section_description = faker.sentence()
        section, created = Section.objects.get_or_create(
            course=course,
            name=section_name,
            defaults={"description": section_description},
        )
        return section

    def create_student(self, course: Course, sections: list) -> MyUser:
        faker = Faker()
        email = faker.email()
        username = faker.user_name()
        while MyUser.objects.filter(email=email).exists():
            email = faker.email()
        while MyUser.objects.filter(username=username).exists():
            username = faker.user_name()

        student = MyUser.objects.create_user(
            username=username,
            email=email,
            first_name=faker.first_name(),
            last_name=faker.last_name(),
            password=faker.password(),
        )
        course_member, created = CourseMember.objects.get_or_create(
            user=student, course=course, defaults={"role": UserRole.STUDENT}
        )
        section_names = []
        for section in sections:
            course_member.sections.add(section)
            section_names.append(section.name)
        if created:
            self.stdout.write(
                self.style.SUCCESS(
                    f'Student "{student.username}" added to course "{course_member.course}" section "{", ".join(section_names)}"'
                )
            )
        return student

    @transaction.atomic
    def handle(self, *args, **options):
        course_id = options["course_id"]
        num_students = options["num_students"]
        num_sections = options["num_sections"]

        course = self.create_course(course_id)
        sections = [
            self.create_section(course, section_number)
            for section_number in range(1, num_sections + 1)
        ]

        self.stdout.write(
            self.style.SUCCESS(
                f'Course "{course.name}" has {str(sections)} as sections.'
            )
        )
        faker = Faker()
        for _ in range(num_students):
            num_sections_for_student = faker.random_int(min=1, max=len(sections))
            sections_for_student = faker.random_elements(
                elements=sections, length=num_sections_for_student, unique=True
            )
            self.create_student(course, sections_for_student)

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully added {num_students} students to course "{course.name}".'
            )
        )
