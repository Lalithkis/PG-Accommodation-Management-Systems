from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Room, RoomAllocation, Complaint, StudentProfile
from .forms import UserRegistrationForm, RoomForm, ComplaintForm

def home(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registration successful! Please login.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def student_dashboard(request):
    if request.user.is_staff:
        return redirect('admin_dashboard')
    
    # Check if student has a room allocated
    try:
        allocation = RoomAllocation.objects.get(student=request.user, status='Approved')
        room = allocation.room
    except RoomAllocation.DoesNotExist:
        room = None
    
    available_rooms_count = Room.objects.filter(status='Available').count()
    pending_applications = RoomAllocation.objects.filter(student=request.user, status='Pending').count()
    
    return render(request, 'student_dashboard.html', {
        'room': room,
        'available_rooms_count': available_rooms_count,
        'pending_applications': pending_applications
    })

@login_required
def room_list(request):
    rooms = Room.objects.all()
    # Check current application status
    has_pending = RoomAllocation.objects.filter(student=request.user, status='Pending').exists()
    has_room = RoomAllocation.objects.filter(student=request.user, status='Approved').exists()
    
    return render(request, 'pg_room_list.html', {
        'rooms': rooms,
        'has_pending': has_pending,
        'has_room_allocated': has_room
    })

@login_required
def apply_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    
    # Check if already applied or has room
    if RoomAllocation.objects.filter(student=request.user, status__in=['Pending', 'Approved']).exists():
        messages.warning(request, 'You already have a pending application or an allocated room.')
        return redirect('room_list')
        
    if room.status == 'Full':
        messages.error(request, 'Room is full.')
        return redirect('room_list')

    RoomAllocation.objects.create(student=request.user, room=room)
    messages.success(request, 'Application submitted successfully.')
    return redirect('dashboard') # Or confirmation page

@login_required
def my_room(request):
    try:
        allocation = RoomAllocation.objects.get(student=request.user, status='Approved')
        room = allocation.room
        roommates = RoomAllocation.objects.filter(room=room, status='Approved').exclude(student=request.user)
    except RoomAllocation.DoesNotExist:
        room = None
        roommates = []
        
    return render(request, 'my_room.html', {'room': room, 'roommates': roommates})

@login_required
def complaints_list(request):
    complaints = Complaint.objects.filter(student=request.user).order_by('-created_at')
    return render(request, 'complaints.html', {'complaints': complaints})

@login_required
def submit_complaint(request):
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.student = request.user
            complaint.save()
            messages.success(request, 'Complaint submitted.')
            return redirect('complaints')
    else:
        form = ComplaintForm()
    return render(request, 'submit_complaint.html', {'form': form})

# Admin Views

def is_admin(user):
    return user.is_staff

@user_passes_test(is_admin)
def admin_dashboard(request):
    total_tenants = RoomAllocation.objects.filter(status='Approved').count()
    total_rooms = Room.objects.count()
    available_rooms = Room.objects.filter(status='Available').count()
    occupied_rooms = Room.objects.filter(status='Full').count() # Or calculated differently
    pending_apps = RoomAllocation.objects.filter(status='Pending').count()
    pending_complaints = Complaint.objects.filter(status='Pending').count()
    
    return render(request, 'admin_dashboard.html', {
        'total_tenants': total_tenants,
        'total_rooms': total_rooms,
        'available_rooms': available_rooms,
        'occupied_rooms': occupied_rooms,
        'pending_apps': pending_apps,
        'pending_complaints': pending_complaints
    })

@user_passes_test(is_admin)
def manage_rooms(request):
    rooms = Room.objects.all().order_by('block_name', 'room_number')
    return render(request, 'manage_rooms.html', {'rooms': rooms})

@user_passes_test(is_admin)
def add_room(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Room added successfully.')
            return redirect('manage_rooms')
    else:
        form = RoomForm()
    return render(request, 'room_form.html', {'form': form, 'title': 'Add Room'})

@user_passes_test(is_admin)
def edit_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            messages.success(request, 'Room updated.')
            return redirect('manage_rooms')
    else:
        form = RoomForm(instance=room)
    return render(request, 'room_form.html', {'form': form, 'title': 'Edit Room'})

@user_passes_test(is_admin)
def delete_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    room.delete() # Careful with existing allocations!
    messages.success(request, 'Room deleted.')
    return redirect('manage_rooms')

@user_passes_test(is_admin)
def manage_students(request):
    allocations = RoomAllocation.objects.filter(status='Approved').select_related('student__studentprofile', 'room')
    return render(request, 'manage_students.html', {'allocations': allocations})

@user_passes_test(is_admin)
def manage_allocations(request):
    allocations = RoomAllocation.objects.all().order_by('-allocated_date') # Or filter pending
    return render(request, 'manage_allocations.html', {'allocations': allocations})

@user_passes_test(is_admin)
def approve_reject_allocation(request, allocation_id, action):
    allocation = get_object_or_404(RoomAllocation, id=allocation_id)
    room = allocation.room
    
    if action == 'approve':
        if room.current_occupancy < room.capacity:
            allocation.status = 'Approved'
            allocation.save()
            
            room.current_occupancy += 1
            if room.current_occupancy >= room.capacity:
                room.status = 'Full'
            room.save()
            messages.success(request, 'Application approved.')
        else:
            messages.error(request, 'Room is full. Cannot approve.')
    
    elif action == 'reject':
        allocation.status = 'Rejected'
        allocation.save()
        messages.info(request, 'Application rejected.')
        
    return redirect('manage_allocations')

@user_passes_test(is_admin)
def manage_complaints(request):
    complaints = Complaint.objects.all().order_by('-created_at')
    return render(request, 'manage_complaints.html', {'complaints': complaints})

@user_passes_test(is_admin)
def resolve_complaint(request, complaint_id):
    complaint = get_object_or_404(Complaint, id=complaint_id)
    complaint.status = 'Resolved'
    complaint.save()
    messages.success(request, 'Complaint marked as resolved.')
    return redirect('manage_complaints')
