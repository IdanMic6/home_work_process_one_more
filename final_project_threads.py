import threading
import requests
 
total_chars = 0

def downloader(url, thread_id):
    global total_chars
    response = requests.get(url).json()  
    response_str = str(response)
    num_chars = len(response_str)
    total_chars += num_chars

    print("Thread " + str(thread_id) + " downloaded " + str(num_chars) + " chars from " + url)
    

def main():
    urls = [
        'https://jsonplaceholder.typicode.com/posts',
        'https://jsonplaceholder.typicode.com/comments',
        'https://jsonplaceholder.typicode.com/albums',
        'https://jsonplaceholder.typicode.com/photos',
        'https://jsonplaceholder.typicode.com/todos',
        'https://jsonplaceholder.typicode.com/users'
    ]

    threads = []
    for i, url in enumerate (urls):
        thread = threading.Thread(target=downloader, args=(url,i+1))
        thread.start()
        threads.append(thread)

    
    for thread in threads:
        thread.join()

    print("Total number of chars downloaded is: " + str(total_chars))

if __name__ == "__main__":
    main()
 

