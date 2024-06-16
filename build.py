import datetime

file_path = 'README.md'

new_line = f"This is a new line added on {datetime.datetime.utcnow().isoformat()}"

with open(file_path, 'a') as f:
    f.write('\n') 
    f.write(new_line)
    f.write('\n')  

print(f"Added the following line to {file_path}:\n{new_line}")
