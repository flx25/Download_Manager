import requests
from concurrent.futures import ThreadPoolExecutor
import re
import threading

download_list = []
currently_downloading=[]
currently_downloading_lock = threading.Lock()

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
		print("Error connecting to the URL {url}: {e}")

#def download(url):


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
	with currently_downloading_lock:
		if currently_downloading:
			print ("Currently downloading:")
			for index, item in enumerate(currently_downloading):
				print(f"{index + 1}. {item}")
	user_input = input("Enter the URLS you want to add, rm removes one or more urls, start starts all or specified downloads, clear clears the download list, refresh refreshes the current downloads, exit closes the programm.\n")
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
			numbers = sorted(extract_numbers(result), reverse=False)
			print (numbers)
			with currently_downloading_lock:
				for index in numbers:
					if index <= len(download_list):
						currently_downloading.append(download_list[index -1])
			numbers = sorted(numbers,reverse=True)
			for number in numbers:
				if number <= len(download_list):
					download_list.pop(number-1)




		elif check_url(result):
			download_list.append(result)



