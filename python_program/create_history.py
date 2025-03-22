import json

with open("python_program/words.txt", "r") as f:
    words = f.readline().split("   ")
    
history = {word: [0, 0] for word in words}
with open("history.json", "w") as f:
    json.dump(history, f, indent=4)
