from django.core.management.base import BaseCommand
from hostel_app.models import Room, StudentProfile, Complaint, RoomAllocation
from django.contrib.auth.models import User
import random

class Command(BaseCommand):
    help = 'Populates the database with sample data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Clearing old data...')
        RoomAllocation.objects.all().delete()
        Complaint.objects.all().delete()
        StudentProfile.objects.all().delete()
        Room.objects.all().delete()
        User.objects.exclude(is_superuser=True).delete()

        self.stdout.write('Creating rooms...')
        blocks = ['A', 'B', 'C']
        room_types = ['Single', 'Double', 'Shared']
        for i in range(1, 11):
            block = random.choice(blocks)
            r_type = random.choice(room_types)
            cap = 1 if r_type == 'Single' else (2 if r_type == 'Double' else 4)
            Room.objects.create(
                room_number=f"{block}{100+i}",
                block_name=f"Block {block}",
                floor=1,
                capacity=cap,
                room_type=r_type,
                status='Available'
            )

        self.stdout.write('Creating students...')
        names = ['Alice', 'Bob', 'Charlie', 'David', 'Eve']
        for i, name in enumerate(names):
            user = User.objects.create_user(username=name.lower(), password='password123', email=f'{name.lower()}@example.com')
            StudentProfile.objects.create(
                user=user,
                full_name=f"{name} Smith",
                department="CSE",
                year="3rd",
                phone_number=f"555-010{i}",
                address="123 Street",
                guardian_name="Parent"
            )
            
        self.stdout.write('Creating complaints...')
        users = User.objects.exclude(is_superuser=True)
        if users.exists():
            Complaint.objects.create(student=users[0], subject="Fan not working", description="Room 101 fan is broken.")

        self.stdout.write('Database populated successfully!')
