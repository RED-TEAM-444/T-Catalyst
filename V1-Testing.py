import subprocess

def run_nmap_command(command, target, position):
    # ASCII art
    ascii_art = '''
    

	┏┳┓  ┏┓┏┓┏┳┓┏┓┓ ┓┏┏┓┏┳┓
	 ┃ ━━┃ ┣┫ ┃ ┣┫┃ ┗┫┗┓ ┃ 
	 ┻   ┗┛┛┗ ┻ ┛┗┗┛┗┛┗┛ ┻ 
                       
    '''
    # Construct terminal command with ASCII art and Nmap command
    terminal_command = f"gnome-terminal --geometry={position} -- bash -c 'echo \"{ascii_art}\"; nmap {command} {target}; read -p \"Press Enter to close...\"'"
    subprocess.Popen(terminal_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def main():
    try:
        target = input("Enter the URL or IP of the target: ").strip()
        if not target:
            print("Invalid input. Please enter a valid URL or IP address.")
            return

        # List of 8 Nmap commands
        nmap_commands = ["-sS", "-sT", "-sU", "-sF", "-sX", "-sN", "-sA", "-sW"]

        # Open two terminal windows on the left side and two on the right side
        left_positions = ["80x24+10+10", "80x24+10+300"]  # Specify left side positions
        right_positions = ["80x24+800+10", "80x24+800+300"]  # Specify right side positions

        for i in range(4):
            if i < 2:
                run_nmap_command(nmap_commands[i], target, left_positions[i])
            else:
                run_nmap_command(nmap_commands[i], target, right_positions[i-2])

        input("Press Enter to exit...")
    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
