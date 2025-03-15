import multiprocessing
import requests

def downloader(url, thread_id, total_chars, lock):
    # Sending a GET request and reading the response as JSON
    response = requests.get(url).json()  
    response_str = str(response)
    num_chars = len(response_str)
    
    # Updating the shared total_chars safely using the lock
    with lock:
        total_chars.value += num_chars

    # Printing the result for the current process
    print("Process " + str(thread_id) + " downloaded " + str(num_chars) + " chars from " + url)

def main():
    # List of URLs to download
    urls = [
        'https://jsonplaceholder.typicode.com/posts',
        'https://jsonplaceholder.typicode.com/comments',
        'https://jsonplaceholder.typicode.com/albums',
        'https://jsonplaceholder.typicode.com/photos',
        'https://jsonplaceholder.typicode.com/todos',
        'https://jsonplaceholder.typicode.com/users'
    ]
     
    # Creating a shared variable to store total characters count
    total_chars = multiprocessing.Value('i', 0)  # 'i' stands for integer, initial value is 0
    
    # Creating a lock to synchronize access to shared data
    lock = multiprocessing.Lock()

    processes = []
    for i, url in enumerate(urls):
        # Creating a new process for each URL
        process = multiprocessing.Process(target=downloader, args=(url, i+1, total_chars, lock))
        process.start()
        processes.append(process)

    # Waiting for all processes to finish
    for process in processes:
        process.join()

    # Printing the total number of characters downloaded
    print("Total number of chars downloaded is: " + str(total_chars.value))

if __name__ == "__main__":
    main()
