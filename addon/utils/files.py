import bpy
import pathlib
import sys
import subprocess


def get_default_folder():
    temporary_directory = bpy.context.preferences.filepaths.temporary_directory
    return str(pathlib.Path(temporary_directory).joinpath("PowerSave"))


def add_to_recent_files():
    try:
        with open(bpy.utils.user_resource('CONFIG', "recent-files.txt"), "r+") as recent_files:
            lines = [bpy.data.filepath]

            for line in recent_files:
                line = line.rstrip("\r\n")

                if line != bpy.data.filepath:
                    lines.append(line)

            content = "\n".join(lines)

            recent_files.seek(0, 0)
            recent_files.write(content)

    except:
        print("Failed to add to recent files")


def open_project_folder():
    path = str(pathlib.Path(bpy.data.filepath).parent)

    if sys.platform == "win32":
        subprocess.Popen(["explorer", path])

    elif sys.platform == "linux":
        subprocess.Popen(["xdg-open", path])

    elif sys.platform == "darwin":
        subprocess.Popen(["open", path])

    else:
        print("Failed to open project folder")