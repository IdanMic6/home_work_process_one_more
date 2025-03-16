import multiprocessing
import requests

def downloader(url, thread_id, total_chars, lock):
    response = requests.get(url).json()  
    response_str = str(response)
    num_chars = len(response_str)
    
    
    with lock:
        total_chars.value += num_chars

    
    print("Process " + str(thread_id) + " downloaded " + str(num_chars) + " chars from " + url)

def main():
    
    urls = [
        'https://jsonplaceholder.typicode.com/posts',
        'https://jsonplaceholder.typicode.com/comments',
        'https://jsonplaceholder.typicode.com/albums',
        'https://jsonplaceholder.typicode.com/photos',
        'https://jsonplaceholder.typicode.com/todos',
        'https://jsonplaceholder.typicode.com/users'
    ]
     
    
    total_chars = multiprocessing.Value('i', 0)  
    
   
    lock = multiprocessing.Lock()

    processes = []
    for i, url in enumerate(urls):
        process = multiprocessing.Process(target=downloader, args=(url, i+1, total_chars, lock))
        process.start()
        processes.append(process)

   
    for process in processes:
        process.join()

    
    print("Total number of chars downloaded is: " + str(total_chars.value))

if __name__ == "__main__":
    main()
