import json

x = {"Artist":"Yeat"}
y = json.dumps(x, indent = 4)
print(y)

file = open("songs/Album/Afterlyfe/info.txt", "wt")
file.write(y)