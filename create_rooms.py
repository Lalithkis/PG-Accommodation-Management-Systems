import os
import django
import random

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hostel_project.settings")
django.setup()

from hostel_app.models import Room

# Define some sample data
block_names = ['A', 'B', 'C']
room_types = ['Single', 'Double', 'Shared']

def create_initial_rooms():
    if Room.objects.exists():
        print("Rooms already exist in the database. Skipping creation.")
        return

    print("Creating initial rooms...")
    rooms_to_create = []
    
    # Create 15 rooms across different blocks
    for i in range(1, 16):
        block = random.choice(block_names)
        room_num = f"{block}-{100 + i}"
        
        # Decide room type and capacity based on type
        r_type = random.choice(room_types)
        if r_type == 'Single':
            capacity = 1
        elif r_type == 'Double':
            capacity = 2
        else:
            capacity = 4
            
        # Create room object
        room = Room(
            room_number=room_num,
            block_name=f"Block {block}",
            floor=1,  # Simplified for example
            capacity=capacity,
            current_occupancy=0, # Start empty
            room_type=r_type,
            status='Available'
        )
        rooms_to_create.append(room)

    try:
        Room.objects.bulk_create(rooms_to_create)
        print(f"Successfully created {len(rooms_to_create)} rooms.")
    except Exception as e:
        print(f"Error creating rooms: {e}")

if __name__ == "__main__":
    create_initial_rooms()
