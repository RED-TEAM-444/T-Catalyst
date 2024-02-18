import subprocess
import multiprocessing
from multiprocessing import Process
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import re
import os

def run_nmap_commands(commands, target, position, output_queue):
    # ASCII art
    ascii_art = '''
    

	┏┳┓  ┏┓┏┓┏┳┓┏┓┓ ┓┏┏┓┏┳┓
	 ┃ ━━┃ ┣┫ ┃ ┣┫┃ ┗┫┗┓ ┃ 
	 ┻   ┗┛┛┗ ┻ ┛┗┗┛┗┛┗┛ ┻ 
                       
    '''
    try:
        # Construct terminal command with ASCII art and Nmap commands
        terminal_command = f"gnome-terminal --geometry={position} -- bash -c 'echo \"{ascii_art}\"; "
        for command in commands:
            terminal_command += f"nmap {command} {target}; "
        terminal_command += "read -p \"Press Enter to close...\"'"
        process = subprocess.Popen(terminal_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output, _ = process.communicate()
        output_queue.put(output)
    except Exception as e:
        print(f"An error occurred: {e}")

def parse_nmap_output(output):
    # Regular expression pattern for extracting information from Nmap output
    port_pattern = re.compile(r"(\d+)/\w+\s+(open)\s+(\w+)")
    parsed_results = []

    # Iterate over lines in the output
    for line in output.split('\n'):
        # Match port information
        port_match = port_pattern.match(line)
        if port_match:
            port_number = port_match.group(1)
            port_status = port_match.group(2)
            protocol = port_match.group(3)
            parsed_results.append({"Port": port_number, "Status": port_status, "Protocol": protocol})

    return parsed_results

def create_pdf_from_outputs(output_queue):
    try:
        # Create a PDF file
        c = canvas.Canvas("nmap_outputs.pdf", pagesize=letter)

        # Write raw output to PDF
        y_position = 750  # Initial y position
        line_height = 15  # Height of each line of text
        page_threshold = 50  # Threshold for starting a new page
        current_page = 1

        while not output_queue.empty():
            if y_position < page_threshold:
                # Start a new page if the current page is full
                c.showPage()
                c.setFont("Helvetica", 12)
                y_position = 750  # Reset y position for new page
                current_page += 1

            output = output_queue.get()
            for line in output.split('\n'):
                # Write each line of output to PDF
                c.drawString(50, y_position, line[:90])  # Adjust line length if needed
                y_position -= line_height  # Move to next line

            y_position -= line_height  # Add extra space between sets of results

        # Save PDF file
        c.save()

        print(f"PDF created successfully with {current_page} page(s).")
    except Exception as e:
        print(f"Error creating PDF: {e}")

def main():
    try:
        target = input("Enter the URL or IP of the target: ").strip()
        if not target:
            print("Invalid input. Please enter a valid URL or IP address.")
            return

        # List of 50 Nmap commands
        nmap_commands = [
            "-sS", "-sT", "-sF", "-sX", "-sN", "-sA", "-sW",
            "-O", "-F", "-sV", "-A", "-T4"
        ]

        # Split the commands into 4 groups
        group_size = len(nmap_commands) // 4
        groups = [nmap_commands[i:i + group_size] for i in range(0, len(nmap_commands), group_size)]

        # Open four terminal windows and execute the commands in each group
        positions = ["80x24+10+10", "80x24+10+300", "80x24+800+10", "80x24+800+300"]
        output_queue = multiprocessing.Queue()
        processes = []
        for i in range(4):
            p = Process(target=run_nmap_commands, args=(groups[i], target, positions[i], output_queue))
            p.start()
            processes.append(p)

        # Wait for all processes to finish
        for p in processes:
            p.join()

        # Create PDF from outputs
        create_pdf_from_outputs(output_queue)

        input("Press Enter to exit...")
    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

