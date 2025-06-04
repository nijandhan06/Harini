import requests
from datetime import datetime, date, timedelta
import json
from enum import Enum

# Base URL of your FastAPI application
BASE_URL = "http://127.0.0.1:8000"

class Endpoint(Enum):
    CREATE = 1
    GET_ALL = 2
    GET_BY_ID = 3
    UPDATE = 4
    DELETE = 5
    GET_BY_STATUS = 6
    GET_BY_DUE_DATE = 7
    SEARCH = 8

def print_response(response):
    """Helper function to print response details"""
    print(f"Status Code: {response.status_code}")
    try:
        print("Response JSON:", json.dumps(response.json(), indent=2))
    except ValueError:
        print("Response Text:", response.text)
    print("-" * 50)

def get_task_data_from_user():
    """Get task details from user input"""
    print("\nEnter task details:")
    title = input("Title (required): ").strip()
    while not title:
        print("Title cannot be empty!")
        title = input("Title (required): ").strip()
    
    description = input("Description (optional): ").strip() or None
    
    status = input("Status (pending/completed, default: pending): ").strip().lower()
    while status and status not in ["pending", "completed"]:
        print('Status must be either "pending" or "completed"')
        status = input("Status (pending/completed): ").strip().lower()
    status = status or "pending"
    
    due_date = None
    due_date_str = input("Due date (YYYY-MM-DD, optional): ").strip()
    if due_date_str:
        try:
            due_date = date.fromisoformat(due_date_str)
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD")
            due_date_str = input("Due date (YYYY-MM-DD, optional): ").strip()
            if due_date_str:
                due_date = date.fromisoformat(due_date_str)
    
    priority = input("Priority (low/medium/high, default: medium): ").strip().lower()
    while priority and priority not in ["low", "medium", "high"]:
        print('Priority must be either "low", "medium", or "high"')
        priority = input("Priority (low/medium/high): ").strip().lower()
    priority = priority or "medium"
    
    return {
        "title": title,
        "description": description,
        "status": status,
        "due_date": due_date.isoformat() if due_date else None,
        "priority": priority
    }

def call_endpoint(endpoint: Endpoint, **kwargs):
    """Switch case implementation for calling different endpoints"""
    task_id = kwargs.get('task_id')
    task_data = kwargs.get('task_data')
    status = kwargs.get('status')
    due_date = kwargs.get('due_date')
    search_term = kwargs.get('search_term')

    response = None
    
    match endpoint:
        case Endpoint.CREATE:
            response = requests.post(f"{BASE_URL}/tasks/", json=task_data)
        case Endpoint.GET_ALL:
            response = requests.get(f"{BASE_URL}/tasks/")
        case Endpoint.GET_BY_ID:
            response = requests.get(f"{BASE_URL}/tasks/{task_id}")
        case Endpoint.UPDATE:
            response = requests.put(f"{BASE_URL}/tasks/{task_id}", json=task_data)
        case Endpoint.DELETE:
            response = requests.delete(f"{BASE_URL}/tasks/{task_id}")
        case Endpoint.GET_BY_STATUS:
            response = requests.get(f"{BASE_URL}/tasks/status/{status}")
        case Endpoint.GET_BY_DUE_DATE:
            response = requests.get(f"{BASE_URL}/tasks/due/{due_date}")
        case Endpoint.SEARCH:
            response = requests.get(f"{BASE_URL}/tasks/search/{search_term}")
        case _:
            print("Invalid endpoint")
    
    if response is not None:
        print_response(response)
        return response
    return None

def show_menu():
    """Display menu and handle user choices"""
    while True:
        print("\nTo-Do List Management System")
        print("1. Create a new task")
        print("2. View all tasks")
        print("3. View a specific task")
        print("4. Update a task")
        print("5. Delete a task")
        print("6. View tasks by status")
        print("7. View tasks by due date")
        print("8. Search tasks")
        print("0. Exit")
        
        choice = input("Enter your choice (0-8): ").strip()
        
        try:
            choice = int(choice)
            if choice == 0:
                print("Exiting...")
                break
            elif choice == 1:
                task_data = get_task_data_from_user()
                call_endpoint(Endpoint.CREATE, task_data=task_data)
            elif choice == 2:
                call_endpoint(Endpoint.GET_ALL)
            elif choice == 3:
                task_id = input("Enter task ID: ").strip()
                call_endpoint(Endpoint.GET_BY_ID, task_id=task_id)
            elif choice == 4:
                task_id = input("Enter task ID to update: ").strip()
                task_data = get_task_data_from_user()
                call_endpoint(Endpoint.UPDATE, task_id=task_id, task_data=task_data)
            elif choice == 5:
                task_id = input("Enter task ID to delete: ").strip()
                call_endpoint(Endpoint.DELETE, task_id=task_id)
            elif choice == 6:
                status = input("Enter status to filter (pending/completed): ").strip().lower()
                while status not in ["pending", "completed"]:
                    print('Status must be either "pending" or "completed"')
                    status = input("Enter status to filter (pending/completed): ").strip().lower()
                call_endpoint(Endpoint.GET_BY_STATUS, status=status)
            elif choice == 7:
                due_date = input("Enter due date (YYYY-MM-DD): ").strip()
                try:
                    date.fromisoformat(due_date)  # Validate date format
                    call_endpoint(Endpoint.GET_BY_DUE_DATE, due_date=due_date)
                except ValueError:
                    print("Invalid date format. Please use YYYY-MM-DD")
            elif choice == 8:
                search_term = input("Enter search term: ").strip()
                call_endpoint(Endpoint.SEARCH, search_term=search_term)
            else:
                print("Invalid choice. Please enter a number between 0 and 8.")
        except ValueError:
            print("Invalid input. Please enter a number.")

if __name__ == "__main__":
    show_menu()