import tkinter as tk
import threading
import time

def background_task():
    while True:
        print("Background thread: Running task")
        time.sleep(1)  # Sleep for 1 second in each iteration

# Function to start the background task in a thread
def start_background_task():
    global background_thread
    background_thread = threading.Thread(target=background_task)
    background_thread.daemon = True  # Set the thread as a daemon
    background_thread.start()

# Create the main Tkinter window
background_thread = threading.Thread(target=background_task)
background_thread.daemon = True  # Set the thread as a daemon
background_thread.start()
root = tk.Tk()
root.title("Background Task Example")

# Create a button to start the background task
start_button = tk.Button(root, text="Start Background Task", command=start_background_task)
start_button.pack()

# Start the Tkinter event loop
root.mainloop()