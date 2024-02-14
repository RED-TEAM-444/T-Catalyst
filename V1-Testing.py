import subprocess

def run_nmap_command(command, target, position):
    terminal_command = f"gnome-terminal --geometry={position} -- bash -c 'nmap {command} {target}; read -p \"Press Enter to close...\"'"
    subprocess.Popen(terminal_command, shell=True)

def main():
    target = input("Enter the URL or IP of the target: ")

    # List of 8 Nmap commands
    nmap_commands = [
        "-sS", "-sT", "-sU", "-sF", "-sX", "-sN", "-sA", "-sW"
    ]

    # Open two terminal windows on the left side and two on the right side
    left_positions = ["80x24+10+10", "80x24+10+300"]  # Specify left side positions
    right_positions = ["80x24+800+10", "80x24+800+300"]  # Specify right side positions

    for i in range(4):
        if i < 2:
            run_nmap_command(nmap_commands[i], target, left_positions[i])
        else:
            run_nmap_command(nmap_commands[i], target, right_positions[i-2])

    input("Press Enter to exit...")

if __name__ == "__main__":
    main()
