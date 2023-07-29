#!/usr/bin/env python3
import os
import shutil

source_file = "/home/osmc/settings.xml"
destination_file = "/home/osmc/.kodi/userdata/addon_data/script.extendedinfo/settings.xml"

def copy_if_not_exist(source, destination):
	if not os.path.exists(destination):
		if not os.path.exists(source_file):
			return
		else:
			shutil.copy2(source, destination)
			print("File copied successfully.")


if __name__ == "__main__":
	copy_if_not_exist(source_file, destination_file)