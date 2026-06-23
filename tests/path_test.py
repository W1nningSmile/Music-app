from pathlib import Path

album_list = ([])
path = 'songs/Album'

for item in Path(path).iterdir():
    album_list.append(item.name)

for item in Path(f"{path}/{album_list[0]}").iterdir():
    print(item)