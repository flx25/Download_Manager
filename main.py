import requests
import concurrent.futures
import re
import threading
import os

download_list = []

def get_filename(link):
		index = link.rfind("/") + 1
		if (index != -1):
			substring = link[index:]
			return substring
		else:
			user_input = input(f"Enter the name for your download from {link}: ")
			return user_input


def extract_numbers(command):
	numbers = re.findall(r'\d+', command)
	return [int(num) for num in numbers]

def check_url(url):
	try:
		response = requests.get(url)
		# Check if the response status code is in the range of successful codes
		if response.status_code // 100 == 2:
			print("URL can be reached and was sucessfully added.")
			return(1)
		else:
			print("The URL is reachable but returned a wrong status code.")
			return(0)
	except requests.RequestException as e:
		print(f"Error connecting to the URL {url}: {e}")

def download_file(url, name):
	print(f"Download started: {url} as {name}")
	try:
		response = requests.get(url)
		response.raise_for_status()

		with open(name, 'wb') as file:
			file.write(response.content)

		print(f"Downloaded {url} to {name}\n")

	except requests.RequestException as e:
		print(f"Error downloading the file from {url}: {e}")
		if os.path.exists(name):
			os.remove(name)



def read_in_list():
	try:
		with open("download_list.txt", "r") as file:
			for line in file:
				download_list.append(line.strip())
		if download_list:
			print("List has been loaded.")
	except FileNotFoundError:
		return


def main_loop():
	if download_list:
		print ("Files in List:")
		for index, item in enumerate(download_list):
			print(f"{index + 1}. {item}")
		print("\n")
	user_input = input("Enter the URL you want to add, rm removes one or more URLs, start <number> starts your download(s), clear clears the download list, refresh refreshes the current downloads, exit closes the programm.\n\n")
	return user_input

if __name__ == "__main__":
	print("Welcome to the To the Download Manager!")
	read_in_list()
	while True:
		result = main_loop()

		if result.lower() == 'exit':
			print("\nThanks for using the Download Manager, your list has been saved!")
			file_path = "download_list.txt"
			with open(file_path, "w") as file:
				for item in download_list:
					file.write(item + "\n")
			break
		elif result.lower().startswith('rm'):
			numbers = sorted(extract_numbers(result), reverse=True)
			for number in numbers:
				if number <= len(download_list):
					download_list.pop(number-1)
		elif result.lower() == 'clear':
			download_list.clear()
			print("Your list has been cleared.")
		elif result.lower().startswith('start'):
			numbers = sorted(extract_numbers(result), reverse=True)
			for index in numbers:
				if index <= len(download_list):
					with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
						futures = [executor.submit(download_file, download_list[index -1], get_filename(download_list[index -1]))]
			for number in numbers:
				if number <= len(download_list):
					download_list.pop(number-1)
		elif check_url(result):
			download_list.append(result)



