import paramiko
import math
import shlex
import subprocess
from utils import get_new_filename
import os
import sys

current_directory, new_filename, new_log_filename = get_new_filename("video_generation")

DOCKER =  False
if os.environ.get('DOCKER'):
    DOCKER = True
    target_path = os.path.join(os.path.dirname(__file__), "../../../../../../app")
else:
    print("not docker")
    cd = os.getcwd()
    target_path = cd+ "/api"
    print("target_path", target_path)

# print current directory from os
# Copy selected.json and readyScript.txt to VM instance
command = f'scp "{target_path}/outputs/selected.json" username@Host Name:/home/username/videocreation/api/outputs'
process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# # Wait for the command to finish and capture the output
stdout, stderr = process.communicate()
current_directory, new_filename, new_log_filename = get_new_filename("subtitle")
command = f'scp "{target_path}/outputs/subtitle.txt" username@Host Name:/home/username/videocreation/api/outputs'
process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# # Wait for the command to finish and capture the output
stdout, stderr = process.communicate()


# # Print the output
print("Copied selected.json to GPU instance")
print(stdout.decode())
 
if stderr:
    print("Errors:")
    print(stderr.decode())


command = f'scp "{target_path}/outputs/readyScript.txt" username@Host Name:/home/username/videocreation/api/outputs'
process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Wait for the command to finish and capture the output
stdout, stderr = process.communicate()

# Print the output
print("Copied readyScript to GPU instance")
print(stdout.decode())

# Print any errors
if stderr:
    print("Errors:")
    print(stderr.decode())


# Connect to the GPU instance and run video_generation.py
hostname = 'Host Name'
port = 22
username = "username"
password = ""

ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
response = ""
max_char = 1000

input = "cd videocreation/api; python3 video_generation.py"
if DOCKER:
    sshdir = "/root/.ssh/id_rsa"
else:
    # depending on cd, 
    sshdir = f"{cd}/.ssh/id_rsa"
    print("sshdir", sshdir)
try:
    ssh_client.load_system_host_keys()
    ssh_client.connect(hostname, port, username, key_filename=sshdir )

    print("Running video_generation.py on GPU instance")
    stdin, stdout, stderr = ssh_client.exec_command(input)
    output = stdout.read().decode()
    error = stderr.read().decode()

    print(output)

except paramiko.AuthenticationException:
    print("Authentication failed. Please check your credentials.")
except paramiko.SSHException as ssh_ex:
    print(f"Unable to establish SSH connection: {ssh_ex}")
finally:
    ssh_client.close()

# Copy generated files and final video from the VM instance to the local machine
files_to_copy = [
    # "subtitle.txt",
    "prompts_list.txt",
    "prompts_list_raw.txt"
]

for file in files_to_copy:
    command = f'scp username@Host Name:/home/username/videocreation/api/outputs/{file} "{target_path}/outputs/"'
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    print(f"Copied {file} to local machine in api/outputs/ directory")
    print(stdout.decode())

    if stderr:
        print("Errors:")
        print(stderr.decode())

# Copy final.mp4 to the public folder on the local machine
print(target_path   )
if DOCKER:
    command = f'scp username@Host Name:/home/username/videocreation/public/final.mp4 "{target_path}/public/"'
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    print("Copied final.mp4 to local machine in public/ directory")
    print(stdout.decode())


    # rename the final.mp4 in the local machine using python
    os.rename(f"{target_path}/public/final.mp4", f"{target_path}/public/finalready.mp4")
    if stderr:
        print("Errors:")
        print(stderr.decode())

else:
    
    command = f'scp username@Host Name:/home/username/videocreation/public/final.mp4 "{cd}/public/"'
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    print("Copied final.mp4 to local machine in public/ directory")
    print(stdout.decode())


    # rename the final.mp4 in the local machine using python
    os.rename(f"{cd}/public/final.mp4", f"{cd}/public/finalready.mp4")
    if stderr:
        print("Errors:")
        print(stderr.decode())

print("Completed execution")