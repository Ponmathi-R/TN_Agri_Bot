import os
import time
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()

def scrape_complete_tn_portal():
    """
    Spins up Selenium to bypass portal firewalls and targets table cells 
    explicitly to extract full agricultural data without drops.
    """
    print("[*] Launching structured table web scraper...")
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    base_url = "https://www.tn.gov.in/scheme_list.php?dep_id=Mg=="
    driver.get(base_url)
    time.sleep(5)
    
    soup = BeautifulSoup(driver.page_source, "html.parser")
    links = []
    for anchor in soup.find_all("a", href=True):
        href = anchor["href"]
        if "scheme_details.php?id=" in href:
            full_url = f"https://www.tn.gov.in/{href}" if not href.startswith("http") else href
            if full_url not in links:
                links.append(full_url)
                
    print(f"[✓] Found {len(links)} available live scheme targets.")
    
    scraped_documents = []
    
    for index, url in enumerate(links):
        print(f"[*] Extracting full table matrix from scheme [{index + 1}/{len(links)}]: {url}")
        try:
            driver.get(url)
            time.sleep(3)
            detail_soup = BeautifulSoup(driver.page_source, "html.parser")
            
            # Target the structural data content table layout natively
            table = detail_soup.find("table")
            
            if table:
                scheme_data = [f"Source Link Reference: {url}"]
                rows = table.find_all("tr")
                
                for row in rows:
                    cells = row.find_all(["td", "th"])
                    if len(cells) >= 2:
                        label = cells[0].text.strip().replace("\n", " ")
                        value = cells[1].text.strip().replace("\n", " ")
                        if label and value:
                            scheme_data.append(f"{label}: {value}")
                
                full_document_text = "\n".join(scheme_data)
                scraped_documents.append(full_document_text)
            else:
                main_content = detail_soup.find("div", {"id": "content"}) or detail_soup.find("body")
                scraped_documents.append(f"Source Link Reference: {url}\nContent:\n{' '.join(main_content.text.split())}")
                
        except Exception as e:
            print(f"[!] Errored while pulling details from url {url}: {e}")
            
    driver.quit()
    return "\n\n========================================\n\n".join(scraped_documents)

if __name__ == "__main__":
    raw_portal_data = scrape_complete_tn_portal()
    
    if not raw_portal_data.strip():
        print("[!] No document data text could be compiled from web element layouts.")
        exit()
        
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=200,
        separators=["========================================", "\n\n", "\n"]
    )
    
    chunks = text_splitter.split_text(raw_portal_data)
    print(f"[✓] Processed database into {len(chunks)} explicit clean table chunks.")

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vector_db = FAISS.from_texts(texts=chunks, embedding=embeddings)
    
    DB_PATH = "faiss_agri_index"
    vector_db.save_local(DB_PATH)
    print(f"[✓] Success! Local Vector store generated flawlessly at './{DB_PATH}'")