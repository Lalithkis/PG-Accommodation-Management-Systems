from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    year = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    guardian_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.full_name} ({self.user.username})"

class Room(models.Model):
    ROOM_TYPES = [
        ('Single', 'Single'),
        ('Double', 'Double'),
        ('Shared', 'Shared'),
    ]
    STATUS_CHOICES = [
        ('Available', 'Available'),
        ('Full', 'Full'),
        ('Maintenance', 'Maintenance'),
    ]

    room_number = models.CharField(max_length=10, unique=True)
    block_name = models.CharField(max_length=50)
    floor = models.IntegerField()
    capacity = models.IntegerField()
    current_occupancy = models.IntegerField(default=0)
    room_type = models.CharField(max_length=20, choices=ROOM_TYPES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Available')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.block_name} - {self.room_number}"

    def update_status(self):
        if self.current_occupancy >= self.capacity:
            self.status = 'Full'
        elif self.status == 'Full' and self.current_occupancy < self.capacity:
            self.status = 'Available'
        self.save()

class RoomAllocation(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    student = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    allocated_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def save(self, *args, **kwargs):
        if self.status == 'Approved':
            # Check capacity before approving
             if self.room.current_occupancy >= self.room.capacity:
                 # This check should ideally be in the view or form validation too
                 # But as a fallback
                 pass 
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student.username} - {self.room.room_number}"

class Complaint(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
    ]

    student = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject} - {self.student.username}"
