"""
	This is Driven core.
	Driven, 2021. yepIwt
"""

import confs

import aiohttp
import asyncio
from vkwave.api import API
from vkwave.client import AIOHTTPClient

import os
import hashlib
import zipfile, shutil

class DrivenCore:

	def __init__(self, vk_api_token: str, local_dir_path: str, current_version_in_unix: int):
		api_session = API(tokens = vk_api_token, clients=AIOHTTPClient())
		self.vk_api = api_session.get_context()
		self.user_hash_id = None
		self.path = local_dir_path
		self.current_version = current_version_in_unix
		self.containers = []

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

	async def hash_user_id(self):
		vk_api_answer = await self.vk_api.docs.get(count = 1)
		try:
			vk_user_id = vk_api_answer.response.items[0].owner_id
			self.user_hash_id = hashlib.sha256(str(vk_user_id).encode('utf-8')).hexdigest()
		except:
			raise 'Добавьте хоть один файл в Вконтакте'

	async def upload_doc(self):

		if not self.user_hash_id:
			await self.hash_user_id()

		vk_api_answer = await self.vk_api.docs.get_upload_server()
		url_for_upload = vk_api_answer.response.upload_url

		try:
			f = open('decrypted.zip','rb')
		except:
			raise "Follow the algorithm!"

		async with aiohttp.ClientSession() as session:
			async with session.post(url_for_upload, data = {'file':f}) as resp:
				json = await resp.json()
				file_obj = json['file']

		await self.vk_api.docs.save(
				file = file_obj,
				title = "Контейнер Driven",
				tags = f"user{self.user_hash_id}",
		)

	async def get_all_containers(self):
		
		if not self.user_hash_id:
			await self.hash_user_id()

		vk_api_answer = await self.vk_api.docs.search(
			q = f"user{self.user_hash_id}",
			search_own = 1,
		)

		for item in vk_api_answer.response.items:
			container = {
				'version_in_unix': item.date,
				'url': item.url,
			}
			self.containers.append(container)

async def main():
	vk_token = ""
	local_dir_path = "C:\\Users\\Nikita\\Driven\\Local"
	vers = 1626472896

	dc = DrivenCore(vk_token, local_dir_path, vers)
	#await dc.upload_doc()
	#await dc.get_all_containers()

if __name__ == '__main__':
	asyncio.run(main())
	#dc.archive_local_directory()
	#shutil.rmtree(dc.path)
	#dc.unzip_local_directory()