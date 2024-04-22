import os
import threading
import logging
import time
from boyer_moor import boyer_moor_search

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Define the keywords to search for 
keywords = ["integers", "jumpStep", "pos"]

# Function to search for keywords in a file
def search_keywords_in_file(file_path, keyword, counter):
    file_name = os.path.basename(file_path)
    count = 0
    with open(file_path, 'r') as file:
        for line in file:
            if boyer_moor_search(line, keyword):
                count += 1
    logging.debug(f"Processed file '{file_name}' for keyword '{keyword}'")
    counter[keyword] += count

# Function to divide files between threads and search for keywords
def process_files(files, keyword_count):
    threads = []
    start_time = time.time()
    thread_counter = 0
    for file in files:
        for keyword in keywords:
            thread = threading.Thread(target=search_keywords_in_file, args=(file, keyword, keyword_count))
            thread.start()
            threads.append(thread)
            thread_counter += 1
    for thread in threads:
        thread.join()
    end_time = time.time()
    logging.info(f"Processed {len(files)} files in {end_time - start_time:.4f} seconds")
    return thread_counter - 1

# Main function
def main():
    try:
        # List of files to process(with Path)
        files = ["article-1.txt"]
        
        # Measure and output execution time
        start_time = time.time()
        
        # Count keywords in files
        keyword_count = {keyword: 0 for keyword in keywords}
        total_threads = process_files(files, keyword_count)
        
        # Output keyword counts
        for keyword, count in keyword_count.items():
            logging.info(f"Keyword '{keyword}' found {count} times")
        
        # Output total execution time
        end_time = time.time()
        logging.info(f"Total execution time: {end_time - start_time:.4f} seconds")
        logging.info(f"Number of threads created: {total_threads}")
    
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
