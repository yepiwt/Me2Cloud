"""
	This is Driven core.
	Driven, 2021. yepIwt
"""

import confs

from vkwave.api import API
from vkwave.client import AIOHTTPClient

import os
import zipfile, shutil

class DrivenCore:

	def __init__(self, vk_api_token: str, local_dir_path: str, current_version_in_unix: int):
		api_session = API(tokens = vk_api_token, clients=AIOHTTPClient())
		self.vk_api = api_session.get_context()
		self.path = local_dir_path
		self.current_version = current_version_in_unix

	def archive_local_directory(self):
		with zipfile.ZipFile('decrypted.zip', 'w', zipfile.ZIP_DEFLATED) as ziph:
			for root, dirs, files in os.walk(self.path):
				for file in files:
					ziph.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), os.path.join(self.path, '..')))
			ziph.close()

	def unzip_local_directory(self):
		path_to_uzip = os.path.join(os.path.dirname(self.path), '')
		with zipfile.ZipFile('decrypted.zip', 'r') as file:
			file.extractall(path_to_uzip)

if __name__ == '__main__':
	#vk_token = ""
	#local_dir_path = "C:\\Users\\Nikita\\Driven\\Local"
	#vers = 1626472896
	dc = DrivenCore(vk_token, local_dir_path, vers)
	
	#dc.archive_local_directory()
	#shutil.rmtree(dc.path)
	#dc.unzip_local_directory()