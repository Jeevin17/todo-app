import json
import os
from rich import print
from rich.panel import Panel as panel
from rich.prompt import Prompt, Confirm
pr = Prompt()
con = Confirm()


FILE = "tasks.json"


def load_tasks():
    if not os.path.exists(FILE):
        return []
    try:
        with open(FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []


def save_tasks(tasks):
    with open(FILE, 'w') as f:
        json.dump(tasks, f, indent=4)
    print(panel.fit("[red]saved[/]"))


def remove_tasks(tasks):
    if not tasks:
        print(panel.fit("[red]Nothing to remove[/]"))
        return
    list_tasks(tasks)
    print(panel.fit("[cyan]YOU ARE TRYING TO DELETE.\
    \n for deleting single task press 1\
    \n for deleting entier task press 2"))
    first_choice = int(pr.ask("choose :", choices=["1","2"]))
    if first_choice == 1:
        selection = int(pr.ask("[red]please select task to\
                           delete in numbers: [/]"))-1
        if 0 <= selection < len(tasks):
            removed = tasks.pop(selection)
            save_tasks(tasks)
            print(panel.fit(f"[blue on white]removed [bold green]{removed}[/]\
                         from tasks[/]"))
    elif first_choice == 2:
        confirm = Confirm.ask("[bold red]Are you sure you want to delete ALL tasks?[/]")
        if confirm:
            tasks.clear()
            save_tasks(tasks)
            print(panel.fit("[green]All tasks deleted successfully![/]"))
        else:
            print(panel.fit("[yellow]Operation cancelled.[/]"))



def list_tasks(tasks):
    if not tasks:
        print(panel("[red]no tasks yet[/]"))
        return
    lines = []
    status_icons = {
     "not done": "❌",
     "in progress": "🕓",
     "completed": "✅"
    }
    for i, t in enumerate(tasks, start=1):
         icon = status_icons.get(t["status"], "❔")
         color = {
            "not done": "red",
            "in progress": "yellow",
            "completed": "green"}.get(t["status"], "white")
         lines.append(f"[{color}]{i}.{t['tasks']} {icon}{t['status']}[/]")
    content = "\n".join(lines)
    print(panel.fit(content,title="listing content"))


def add_tasks(tasks):
    try:
        task = pr.ask("[red]Enter a new task or <C-d> to exit: [/]")
        tasks.append({"tasks": task, "status": "not done"})
        print(panel.fit("[yellow] TASK SUCCESSFULLY UPDATED!!![/]"))
        save_tasks(tasks)
    except EOFError:
        print("\n")
        print(panel.fit("canceling the task...."))


def mark_done(tasks):
    if not tasks:
        print(panel.fit("[red]No tasks to update[/]"))
    list_tasks(tasks)
    selection = int(pr.ask("[blue]select: [/]")) - 1
    if 0 <= selection < len(tasks):
         print(panel.fit(
                "[yellow]Choose new status:[/]\n"
                "1. ✅ Completed\n"
                "2. 🕓 In Progress\n"
                "3. ❌ Not Done"
            ))

            
         choice = pr.ask("Enter choice (1/2/3): ", choices=["1", "2", "3"])

            
         status_map = {
                "1": "completed",
                "2": "in progress",
                "3": "not done"
            }
         tasks[selection]["status"] = status_map[choice]
         save_tasks(tasks)
         print(panel.fit("[green]Marked!!![/]"))


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def main():
    tasks = load_tasks()
    clear_screen()
    print(panel("[b]WELCOME[/]", title="TODO_APP"))
    while True:
        try:
            print(panel.fit("[red] choices avaible=\n 1. View tasks\n 2. Add task\n 3. Change status\n 4. Delete task \n 5. exit\n[/]"))
            choice = pr.ask("choose: ", choices=["1", "2", "3", "4", "5"], default="1")
            clear_screen()
            if choice == "1":
                list_tasks(tasks)
                continue
            elif choice == "2":
                add_tasks(tasks)
                continue
            elif choice == "3":
                mark_done(tasks)
                continue
            elif choice == "4":
                remove_tasks(tasks)
                continue
            elif choice == "5":
                print(panel.fit("[green]thankyou bye[/]"))
            break
        except KeyboardInterrupt:
            print("\n")
            print(panel("[green]goodbye!!!![/]"))
            break


if __name__ == "__main__":
    main()
