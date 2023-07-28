import requests
from bs4 import BeautifulSoup
from random import randint
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

class TextScrapper:
    def from_url(self, url, target_text):
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            text = soup.get_text()
            if target_text in text:
                return f"Target text found on page {url}"
            else:
                return None
        except Exception as e:
            print(f"An error occurred while trying to extract text from the URL {url}: {e}")
            return None

    def find_target_text(self, base_url, target_text, num_parallel_searches=61400):
        error_count = 0

        with open(r"    **your file destination and name here**    ", "w") as file:  # Open file for writing results
            for _ in range(num_parallel_searches):
                page_number = randint( 1, 36893488147419104)

                def perform_search(page_number):
                    url_to_scrape = f"{base_url}/?page={page_number}"
                    result = self.from_url(url_to_scrape, target_text)
                    tqdm.write(f"Checking page {page_number}...")
                    
                    if result is not None:
                        file.write(result + "\n")  # Write result to the file
                    
                    return result
                
                try:
                    with ThreadPoolExecutor(max_workers=num_parallel_searches) as executor:
                        futures = [executor.submit(perform_search, page_number)]

                        for future in as_completed(futures):
                            result = future.result()
                            if result is not None:
                                return result

                    error_count = 0
                except KeyboardInterrupt:
                    print("\nInterrupted. Stopping...")
                    break
                except ConnectionResetError as e:
                    error_count += 1
                    print(f"An error occurred: {e}")
                    if error_count >= 3:
                        print("Too many errors in a row. Stopping...")
                        break
                except Exception as e:
                    error_count = 0
                    print(f"An error occurred: {e}")

        return None


# Example usage:
base_url_to_scrape = "https://hashkeys.space/66/"
target_text = "	13zb1hQbWVsc2S7ZTZnP2G4undNNpdh5so"

scrapper = TextScrapper()
result = scrapper.find_target_text(base_url_to_scrape, target_text, num_parallel_searches=61400)
if result is not None:
    print(result)