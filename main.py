import sys
import threading
import time
from datetime import datetime
from services.task_service import TaskService
from models.task import Task

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

# abstraction: I instantiated the service here so the main file doesn't need to touch sql directly
task_service = TaskService()

def print_header():
    print(f"{Colors.HEADER}")
    print(r"""
  _______        _      _______             _             
 |__   __|      | |    |__   __|           | |            
    | | __ _ ___| | __    | |_ __ __ _  ___| | _____ _ __ 
    | |/ _` / __| |/ /    | | '__/ _` |/ __| |/ / _ \ '__|
    | | (_| \__ \   <     | | | | (_| | (__|   <  __/ |   
    |_|\__,_|___/_|\_\    |_|_|  \__,_|\___|_|\_\___|_|   
                                                          
    v1.0 - Python Command Line Interface
    """)
    print(f"{Colors.ENDC}")
    print("="*60)

def validate_date(date_str):
    try:
        dt = datetime.strptime(date_str, '%Y-%m-%d')
        # validation: I added a check to ensure tasks aren't scheduled in the past
        if dt.date() < datetime.now().date():
            print(f"{Colors.WARNING}[!] Date cannot be in the past.{Colors.ENDC}")
            return None
        return dt
    except ValueError:
        return None

def background_backup_process():
    # multithreading: running this on a separate thread so it doesn't freeze the cli
    while True:
        time.sleep(300) 
        pass 

def add_task_flow():
    print(f"\n{Colors.BLUE}--- ADD NEW TASK ---{Colors.ENDC}")
    print(f"{Colors.WARNING}(Type 'm' at any prompt to cancel){Colors.ENDC}")
    
    title = input("\nTask Name: ").strip()
    # ux: allowed instant cancellation if I hit enter or type 'm'
    if title.lower() == 'm' or not title: return 

    desc = input("Description: ").strip()
    if desc.lower() == 'm': return

    while True:
        date_input = input("Due Date (YYYY-MM-DD): ").strip()
        if date_input.lower() == 'm': return

        if validate_date(date_input):
            due_date = date_input
            break
        print(f"{Colors.WARNING}[!] Invalid format/day. Use YYYY-MM-DD.{Colors.ENDC}")

    priority_input = input("Priority (Low/Medium/High) [Default: Medium]: ").strip().capitalize()
    if priority_input.lower() == 'm': return

    priority = priority_input if priority_input in ['Low', 'Medium', 'High'] else 'Medium'

    # encapsulation: I created a task object here to keep the data structured
    new_task = Task(title=title, description=desc, due_date=due_date, priority=priority)
    if task_service.add_task(new_task):
        print(f"{Colors.GREEN}[SUCCESS] Task saved successfully.{Colors.ENDC}")
    else:
        print(f"{Colors.FAIL}[ERROR] Failed to save task.{Colors.ENDC}")
    
    input("\nPress Enter to continue...")

def list_tasks_flow():
    current_filter = None
    filter_label = "ALL TASKS"
    tasks = task_service.get_all_tasks(current_filter)

    while True:
        print(f"\n{Colors.BLUE}--- {filter_label} ---{Colors.ENDC}")
        
        if not tasks:
            print(f"{Colors.FAIL}No tasks found matching criteria.{Colors.ENDC}")
        else:
            print(f"{Colors.BOLD}{'ID':<5} {'Task Name':<25} {'Due Date':<12} {'Priority':<10} {'Status'}{Colors.ENDC}")
            print("-" * 65)
            for t in tasks:
                status_color = Colors.GREEN if t.status == 'Completed' else Colors.WARNING
                
                # logic: I added a visual check here to highlight overdue tasks in red
                task_date = t.due_date if isinstance(t.due_date, datetime) else datetime.strptime(str(t.due_date), '%Y-%m-%d').date()
                today = datetime.now().date()
                
                date_display = str(t.due_date)
                if task_date < today and t.status != 'Completed':
                    date_display = f"{Colors.FAIL}{str(t.due_date)}{Colors.ENDC}"

                print(f"{t.id:<5} {t.title[:23]:<25} {date_display:<21} {t.priority:<10} {status_color}{t.status}{Colors.ENDC}")

        print("-" * 65)
        print()
        print(f"Filters:  [{Colors.BOLD}P{Colors.ENDC}]ending   [{Colors.BOLD}I{Colors.ENDC}]n Progress   [{Colors.BOLD}C{Colors.ENDC}]ompleted   [{Colors.BOLD}A{Colors.ENDC}]ll")
        print(f"Actions:  {Colors.BOLD}Type ID number{Colors.ENDC} to view details, or Enter for Menu")
        
        while True:
            choice = input("\n> Select option: ").strip().lower()

            if choice == '': return 

            if choice in ['p', 'i', 'c', 'a']:
                if choice == 'p': current_filter = 'Pending'; filter_label = "PENDING TASKS"
                elif choice == 'i': current_filter = 'In Progress'; filter_label = "IN PROGRESS"
                elif choice == 'c': current_filter = 'Completed'; filter_label = "COMPLETED TASKS"
                elif choice == 'a': current_filter = None; filter_label = "ALL TASKS"
                tasks = task_service.get_all_tasks(current_filter)
                break 

            elif choice.isdigit():
                # oop: accessed the task object attributes directly
                selected_task = next((t for t in tasks if str(t.id) == choice), None)
                if selected_task:
                    print(f"\n{Colors.BLUE}--- TASK DETAILS ---{Colors.ENDC}")
                    print(f"{Colors.BOLD}ID:{Colors.ENDC}          {selected_task.id}")
                    print(f"{Colors.BOLD}Name:{Colors.ENDC}        {selected_task.title}")
                    print(f"{Colors.BOLD}Description:{Colors.ENDC} {selected_task.description}")
                    print(f"{Colors.BOLD}Due Date:{Colors.ENDC}    {selected_task.due_date}")
                    print(f"{Colors.BOLD}Priority:{Colors.ENDC}    {selected_task.priority}")
                    print(f"{Colors.BOLD}Status:{Colors.ENDC}      {selected_task.status}")
                    input("\nPress Enter to return to list...")
                    break 
                else:
                    print(f"{Colors.FAIL}[!] Task ID {choice} not found. Try again.{Colors.ENDC}")
                    continue 
            else:
                print(f"{Colors.WARNING}Invalid command.{Colors.ENDC}")

def update_task_flow():
    print(f"\n{Colors.BLUE}--- UPDATE TASK ---{Colors.ENDC}")
    
    tasks = task_service.get_all_tasks()
    if not tasks:
        print(f"{Colors.WARNING}No tasks available to update.{Colors.ENDC}")
        input("Press Enter to continue...")
        return

    print(f"{'ID':<5} {'Task Name':<25} {'Due Date':<12} {'Priority':<10} {'Status'}")
    print("-" * 65)
    for t in tasks:
        print(f"{t.id:<5} {t.title[:23]:<25} {str(t.due_date):<12} {t.priority:<10} {t.status}")

    print(f"\n{Colors.WARNING}(Press Enter to cancel){Colors.ENDC}")
    task_id = input(f"{Colors.BOLD}Enter Task ID to update: {Colors.ENDC}")
    if not task_id: return

    current_task = next((t for t in tasks if str(t.id) == task_id), None)
    if not current_task:
        print(f"{Colors.FAIL}[ERROR] Task ID {task_id} not found.{Colors.ENDC}")
        input("Press Enter to continue...")
        return

    print(f"\n{Colors.BOLD}Current Description:{Colors.ENDC} {current_task.description}")
    print(f"\n{Colors.WARNING}--- Enter New Details (Leave blank to keep current) ---{Colors.ENDC}")
    
    title = input("New Task Name: ").strip()
    if not title: title = current_task.title 

    desc = input("New Description: ").strip()
    if not desc: desc = current_task.description

    while True:
        date_input = input("New Due Date (YYYY-MM-DD): ").strip()
        if not date_input:
            due_date = current_task.due_date
            break
        valid_date = validate_date(date_input)
        if valid_date:
            due_date = date_input
            break
        print(f"{Colors.WARNING}[!] Invalid format. Use YYYY-MM-DD.{Colors.ENDC}")

    priority_input = input("New Priority (Low/Medium/High): ").strip().capitalize()
    if not priority_input:
        priority = current_task.priority
    elif priority_input in ['Low', 'Medium', 'High']:
        priority = priority_input
    else:
        priority = current_task.priority

    if task_service.update_task(task_id, title, desc, due_date, priority):
        print(f"{Colors.GREEN}[SUCCESS] Task updated.{Colors.ENDC}")
    else:
        print(f"{Colors.FAIL}[ERROR] Update failed.{Colors.ENDC}")
    
    input("\nPress Enter to continue...")

def mark_task_complete_flow():
    print(f"\n{Colors.BLUE}--- COMPLETE TASK ---{Colors.ENDC}")
    tasks = task_service.get_all_tasks()
    
    pending_tasks = [t for t in tasks if t.status != 'Completed']

    if not pending_tasks:
        print(f"{Colors.GREEN}All tasks are already completed!{Colors.ENDC}")
        input("Press Enter to continue...")
        return

    print(f"{'ID':<5} {'Task Name':<25} {'Due Date':<12} {'Status'}")
    print("-" * 50)
    for t in pending_tasks:
        print(f"{t.id:<5} {t.title[:23]:<25} {str(t.due_date):<12} {t.status}")

    print(f"\n{Colors.WARNING}(Press Enter to cancel){Colors.ENDC}")
    tid = input(f"{Colors.BOLD}Enter Task ID to complete: {Colors.ENDC}")
    if not tid: return

    if task_service.mark_task_complete(tid):
        print(f"{Colors.GREEN}[SUCCESS] Task marked as Completed.{Colors.ENDC}")
    else:
        print(f"{Colors.FAIL}[ERROR] Failed.{Colors.ENDC}")
    
    input("\nPress Enter to continue...")

def delete_task_flow():
    while True:
        print(f"\n{Colors.BLUE}--- DELETE TASK ---{Colors.ENDC}")
        tasks = task_service.get_all_tasks()
        if not tasks:
            print(f"{Colors.WARNING}No tasks available to delete.{Colors.ENDC}")
            input("Press Enter to continue...")
            return

        print(f"{'ID':<5} {'Task Name':<25} {'Due Date':<12} {'Status'}")
        print("-" * 50)
        for t in tasks:
            print(f"{t.id:<5} {t.title[:23]:<25} {str(t.due_date):<12} {t.status}")

        print(f"\n{Colors.WARNING}(Press Enter to cancel){Colors.ENDC}")
        task_id = input(f"{Colors.BOLD}Enter Task ID to delete: {Colors.ENDC}").strip()
        if not task_id: break

        task_to_delete = next((t for t in tasks if str(t.id) == task_id), None)
        if not task_to_delete:
            print(f"{Colors.FAIL}[ERROR] ID {task_id} not found.{Colors.ENDC}")
            continue 

        confirm = input(f"{Colors.FAIL}Are you sure you want to delete '{task_to_delete.title}'? (y/n): {Colors.ENDC}")
        if confirm.lower() == 'y':
            if task_service.delete_task(task_id):
                print(f"{Colors.GREEN}[SUCCESS] Task '{task_to_delete.title}' was deleted.{Colors.ENDC}")
            else:
                print(f"{Colors.FAIL}[ERROR] Database error.{Colors.ENDC}")
        else:
            print("Deletion cancelled.")
        
        print("\n------------------------------------------------")
        loop_choice = input("Press Enter to delete another, or type 'm' to return to menu: ").strip().lower()
        if loop_choice == 'm': break

def show_analytics():
    print(f"\n{Colors.BLUE}--- ANALYTICS DASHBOARD ---{Colors.ENDC}")
    tasks = task_service.get_all_tasks()
    
    if not tasks:
        print("No data available.")
        input("Press Enter to continue...")
        return

    # 1. calculate stats
    total = len(tasks)
    completed = sum(1 for t in tasks if t.status == 'Completed')
    high = sum(1 for t in tasks if t.priority == 'High')
    medium = sum(1 for t in tasks if t.priority == 'Medium')
    low = sum(1 for t in tasks if t.priority == 'Low')
    
    completion_rate = (completed / total) * 100 if total > 0 else 0

    def draw_bar(count, total_count, color=Colors.GREEN):
        if total_count == 0: return ""
        length = int((count / total_count) * 20) 
        return color + "█" * length + Colors.ENDC

    print(f"\n{Colors.BOLD}OVERALL STATUS:{Colors.ENDC}")
    print(f"Total Tasks: {total}")
    print(f"Completion:  {completion_rate:.1f}%")
    print(f"[{draw_bar(completed, total)}{' ' * (20 - int(completion_rate/5))} ]")

    print(f"\n{Colors.BOLD}PRIORITY BREAKDOWN:{Colors.ENDC}")
    print(f"High:    {high:<3} {draw_bar(high, total, Colors.FAIL)}")
    print(f"Medium:  {medium:<3} {draw_bar(medium, total, Colors.WARNING)}")
    print(f"Low:     {low:<3} {draw_bar(low, total, Colors.BLUE)}")

    input("\nPress Enter to continue...")

def main():
    backup_thread = threading.Thread(target=background_backup_process, daemon=True)
    backup_thread.start()

    while True:
        print_header()
        print("1. Add Task")
        print("2. List Tasks")
        print("3. Update Task")
        print("4. Mark Task Complete")
        print("5. Delete Task")
        print(f"{Colors.BOLD}6. View Analytics{Colors.ENDC}")
        print("7. Exit")
        
        choice = input("\nSelect an option: ")

        if choice == '1': add_task_flow()
        elif choice == '2': list_tasks_flow()
        elif choice == '3': update_task_flow()
        elif choice == '4': mark_task_complete_flow()
        elif choice == '5': delete_task_flow()
        elif choice == '6': show_analytics()
        elif choice == '7':
            print("Exiting application...")
            sys.exit()
        else:
            print("Invalid option, try again.")

if __name__ == "__main__":
    main()