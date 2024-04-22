import os
import multiprocessing
import logging
import time
from boyer_moor import boyer_moor_search

# Import multiprocessing module
import multiprocessing

# Get the number of CPU cores
num_processors = multiprocessing.cpu_count()
print("Number of processors:", num_processors)


# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Define the keywords to search for
keywords = ["integers", "jumpStep", "pos"]

# Function to search for keywords in a file
def search_keywords_in_file(file_path, keyword, result_queue):
    try:
        file_name = os.path.basename(file_path)
        found_files = []
        with open(file_path, 'r') as file:
            for line in file:
                if boyer_moor_search(line, keyword):
                    found_files.append(file_path)
        result_queue.put((keyword, found_files))
        logging.debug(f"Processed file '{file_name}'")
    except Exception as e:
        logging.error(f"Error processing file '{file_path}': {str(e)}")

# Function to divide files between processes and search for keywords
def process_files(files, result_queue):
    processes = []
    start_time = time.time()
    for keyword in keywords:
        for file in files:
            process = multiprocessing.Process(target=search_keywords_in_file, args=(file, keyword, result_queue))
            process.start()
            processes.append(process)
    for process in processes:
        process.join()
    end_time = time.time()
    logging.info(f"Processed {len(files)} files in {end_time - start_time:.4f} seconds")

# Main function
def main():
    try:
        # List of files to process with path
        files = ["article-1.txt"]
        
        # Create a multiprocessing.Queue for inter-process communication
        result_queue = multiprocessing.Queue()
        
        # Measure and output execution time
        start_time = time.time()
        
        # Process files and search for keywords
        process_files(files, result_queue)
        
        # Collect search results from the queue
        result_dict = {}
        while not result_queue.empty():
            keyword, found_files = result_queue.get()
            if keyword in result_dict:
                result_dict[keyword].extend(found_files)
            else:
                result_dict[keyword] = found_files
        
        # Output total count of occurrences for each keyword
        for keyword, found_files in result_dict.items():
            logging.info(f"Keyword '{keyword}' found in {len(found_files)} files")
        
        # Output total execution time
        end_time = time.time()
        logging.info(f"Total execution time: {end_time - start_time:.4f} seconds")
        
        return result_dict
    
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return {}

if __name__ == "__main__":
    main()
