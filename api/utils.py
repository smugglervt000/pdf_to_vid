import os
import datetime


def get_new_filename(func_name):
    """Generate new filename with timestamp, based on whether the code is running in a Docker container."""

    timestamp = datetime.datetime.now().strftime("%d%H:%M")
    current_directory =  os.getcwd()
    print(os.environ.get("DOCKER"))
    print(current_directory)
    if os.environ.get("DOCKER"):
        new_filename = f"{current_directory}/outputs/{func_name}.txt"
        if not os.path.exists(f"{current_directory}/outputs"):
            os.makedirs(f"{current_directory}/outputs")
        if not os.path.exists(f"{current_directory}/logs"):
            os.makedirs(f"{current_directory}/logs")
        new_log_filename = f"{current_directory}/logs/{func_name}{timestamp}docker.txt"
    else:
        # Create new filename with timestamp
        current_directory = "api"
        new_log_filename = f"api/logs/{func_name}{timestamp}.txt"
        if not os.path.exists("api/logs"):
            os.makedirs("api/logs")
        new_filename = f"api/outputs/{func_name}.txt"
        # Save to outputs folder
        if not os.path.exists("api/outputs"):
            os.makedirs("api/outputs")

    return current_directory, new_filename, new_log_filename