import os

def get_subfolder_names(path):
    subfolders = [f.name for f in os.scandir(path) if f.is_dir()]
    return subfolders

if __name__ == "__main__":
    path = 'objs/02942699'
    subfolder_names = get_subfolder_names(path)
    print('[' + ', '.join(f'"{name}"' for name in subfolder_names) + ']')
