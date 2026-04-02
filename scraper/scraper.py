"""
Web Scraper for Tanzanian Real Estate Websites
Scrapes property listings from major Tanzanian real estate platforms
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from fake_useragent import UserAgent
import json
import logging
from datetime import datetime
import re
from urllib.parse import urljoin, urlparse
import os

# Configure logging - Use console only for Render deployment
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

class TanzaniaRealEstateScraper:
    def __init__(self):
        self.ua = UserAgent()
        self.session = requests.Session()
        self.scraped_data = []
        self.failed_urls = []
        
        # Create logs directory if it doesn't exist
        os.makedirs('../logs', exist_ok=True)
        
        # Create data directories
        os.makedirs('../data/raw', exist_ok=True)
        os.makedirs('../data/cleaned', exist_ok=True)
        
    def setup_selenium_driver(self, headless=True):
        """Setup Selenium WebDriver"""
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument(f"--user-agent={self.ua.random}")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        try:
            driver = webdriver.Chrome(options=chrome_options)
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            return driver
        except Exception as e:
            logging.error(f"Failed to setup Selenium driver: {e}")
            return None
    
    def random_delay(self, min_delay=1, max_delay=3):
        """Add random delay to avoid being blocked"""
        delay = random.uniform(min_delay, max_delay)
        time.sleep(delay)
    
    def clean_price(self, price_text):
        """Extract and clean price from text"""
        if not price_text:
            return None
        
        # Remove common currency symbols and text
        price_text = re.sub(r'[Tt][Zz][Ss]|[,$\s]', '', price_text)
        
        # Extract numbers
        numbers = re.findall(r'\d+', price_text)
        
        if numbers:
            # Join all numbers and convert to int
            price = ''.join(numbers)
            try:
                return int(price)
            except ValueError:
                return None
        
        return None
    
    def clean_size(self, size_text):
        """Extract and clean size from text"""
        if not size_text:
            return None
        
        # Extract numbers and convert to float
        size_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:sqm|m2|square.?meter)', size_text.lower())
        if size_match:
            try:
                return float(size_match.group(1))
            except ValueError:
                return None
        
        return None
    
    def clean_bedrooms(self, bed_text):
        """Extract number of bedrooms from text"""
        if not bed_text:
            return None
        
        # Look for bedroom patterns
        bed_match = re.search(r'(\d+)\s*(?:bed|bedroom|br)', bed_text.lower())
        if bed_match:
            try:
                return int(bed_match.group(1))
            except ValueError:
                return None
        
        return None
    
    def clean_bathrooms(self, bath_text):
        """Extract number of bathrooms from text"""
        if not bath_text:
            return None
        
        # Look for bathroom patterns
        bath_match = re.search(r'(\d+)\s*(?:bath|bathroom)', bath_text.lower())
        if bath_match:
            try:
                return int(bath_match.group(1))
            except ValueError:
                return None
        
        return None
    
    def extract_location(self, location_text):
        """Extract location information"""
        if not location_text:
            return None, None, None
        
        # Common Tanzanian cities
        cities = ['dar es salaam', 'arusha', 'mwanza', 'dodoma', 'mbeya', 'morogoro', 'tanga', 'kigoma']
        location_text_lower = location_text.lower()
        
        city = None
        for c in cities:
            if c in location_text_lower:
                city = c.title()
                break
        
        # Try to extract ward/location
        wards = ['kinondoni', 'ilala', 'temeke', 'ubungo', 'mikocheni', 'masaki', 'oyster bay', 'upanga']
        ward = None
        for w in wards:
            if w in location_text_lower:
                ward = w.title()
                break
        
        return location_text.strip(), city, ward
    
    def scrape_kupatana(self, max_pages=5):
        """Scrape property listings from Kupatana.tz"""
        logging.info("Starting Kupatana scraper...")
        
        base_url = "https://kupatana.tz"
        property_listings = []
        
        try:
            driver = self.setup_selenium_driver()
            if not driver:
                return property_listings
            
            for page in range(1, max_pages + 1):
                url = f"{base_url}/tanzania/property-for-rent?sort=newest&page={page}"
                
                try:
                    logging.info(f"Scraping Kupatana page {page}")
                    driver.get(url)
                    self.random_delay(2, 4)
                    
                    # Wait for listings to load
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "listing"))
                    )
                    
                    # Get listings
                    listings = driver.find_elements(By.CLASS_NAME, "listing")
                    
                    for listing in listings:
                        try:
                            property_data = self.extract_kupatana_listing(listing, base_url)
                            if property_data:
                                property_listings.append(property_data)
                        except Exception as e:
                            logging.warning(f"Error extracting listing: {e}")
                            continue
                    
                    logging.info(f"Page {page}: Found {len(listings)} listings")
                    
                except TimeoutException:
                    logging.warning(f"Timeout on page {page}")
                    continue
                except Exception as e:
                    logging.error(f"Error on page {page}: {e}")
                    continue
            
            driver.quit()
            
        except Exception as e:
            logging.error(f"Kupatana scraper error: {e}")
        
        logging.info(f"Kupatana scraper completed. Total listings: {len(property_listings)}")
        return property_listings
    
    def extract_kupatana_listing(self, listing_element, base_url):
        """Extract data from a single Kupatana listing"""
        try:
            # Basic property info
            title_elem = listing_element.find_element(By.CLASS_NAME, "title")
            title = title_elem.text.strip()
            
            # Get link
            link_elem = title_elem.find_element(By.TAG_NAME, "a")
            property_url = link_elem.get_attribute('href')
            
            # Price
            try:
                price_elem = listing_element.find_element(By.CLASS_NAME, "price")
                price = self.clean_price(price_elem.text)
            except NoSuchElementException:
                price = None
            
            # Location
            try:
                location_elem = listing_element.find_element(By.CLASS_NAME, "location")
                location_text = location_elem.text.strip()
                location, city, ward = self.extract_location(location_text)
            except NoSuchElementException:
                location, city, ward = None, None, None
            
            # Description (might contain size, bedrooms info)
            try:
                desc_elem = listing_element.find_element(By.CLASS_NAME, "description")
                description = desc_elem.text.strip()
                
                # Extract size, bedrooms, bathrooms from description
                size = self.clean_size(description)
                bedrooms = self.clean_bedrooms(description)
                bathrooms = self.clean_bathrooms(description)
            except NoSuchElementException:
                description = None
                size = None
                bedrooms = None
                bathrooms = None
            
            # Property type (default to House, can be improved)
            property_type = "House"
            if "apartment" in title.lower() or "flat" in title.lower():
                property_type = "Apartment"
            elif "villa" in title.lower():
                property_type = "Villa"
            
            return {
                'title': title,
                'price_tzs': price,
                'location': location,
                'city': city,
                'ward': ward,
                'size_sqm': size,
                'bedrooms': bedrooms,
                'bathrooms': bathrooms,
                'property_type': property_type,
                'description': description,
                'source': 'Kupatana',
                'url': property_url,
                'scraped_date': datetime.now().isoformat()
            }
            
        except Exception as e:
            logging.warning(f"Error extracting listing data: {e}")
            return None
    
    def scrape_zoomtanzania(self, max_pages=5):
        """Scrape property listings from ZoomTanzania"""
        logging.info("Starting ZoomTanzania scraper...")
        
        base_url = "https://www.zoomtanzania.com"
        property_listings = []
        
        try:
            driver = self.setup_selenium_driver()
            if not driver:
                return property_listings
            
            for page in range(1, max_pages + 1):
                url = f"{base_url}/tz/property-for-rent.html?page={page}"
                
                try:
                    logging.info(f"Scraping ZoomTanzania page {page}")
                    driver.get(url)
                    self.random_delay(2, 4)
                    
                    # Wait for listings to load
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "category-list"))
                    )
                    
                    # Get listings
                    listings = driver.find_elements(By.CLASS_NAME, "category-list__item")
                    
                    for listing in listings:
                        try:
                            property_data = self.extract_zoomtanzania_listing(listing, base_url)
                            if property_data:
                                property_listings.append(property_data)
                        except Exception as e:
                            logging.warning(f"Error extracting listing: {e}")
                            continue
                    
                    logging.info(f"Page {page}: Found {len(listings)} listings")
                    
                except TimeoutException:
                    logging.warning(f"Timeout on page {page}")
                    continue
                except Exception as e:
                    logging.error(f"Error on page {page}: {e}")
                    continue
            
            driver.quit()
            
        except Exception as e:
            logging.error(f"ZoomTanzania scraper error: {e}")
        
        logging.info(f"ZoomTanzania scraper completed. Total listings: {len(property_listings)}")
        return property_listings
    
    def extract_zoomtanzania_listing(self, listing_element, base_url):
        """Extract data from a single ZoomTanzania listing"""
        try:
            # Title and link
            title_elem = listing_element.find_element(By.CLASS_NAME, "category-list__title")
            title = title_elem.text.strip()
            
            link_elem = title_elem.find_element(By.TAG_NAME, "a")
            property_url = link_elem.get_attribute('href')
            
            # Price
            try:
                price_elem = listing_element.find_element(By.CLASS_NAME, "category-list__price")
                price = self.clean_price(price_elem.text)
            except NoSuchElementException:
                price = None
            
            # Location
            try:
                location_elem = listing_element.find_element(By.CLASS_NAME, "category-list__location")
                location_text = location_elem.text.strip()
                location, city, ward = self.extract_location(location_text)
            except NoSuchElementException:
                location, city, ward = None, None, None
            
            # Additional details
            try:
                details_elem = listing_element.find_element(By.CLASS_NAME, "category-list__details")
                details_text = details_elem.text.strip()
                
                # Extract size, bedrooms, bathrooms
                size = self.clean_size(details_text)
                bedrooms = self.clean_bedrooms(details_text)
                bathrooms = self.clean_bathrooms(details_text)
            except NoSuchElementException:
                size = None
                bedrooms = None
                bathrooms = None
            
            # Property type
            property_type = "House"
            if "apartment" in title.lower() or "flat" in title.lower():
                property_type = "Apartment"
            elif "villa" in title.lower():
                property_type = "Villa"
            
            return {
                'title': title,
                'price_tzs': price,
                'location': location,
                'city': city,
                'ward': ward,
                'size_sqm': size,
                'bedrooms': bedrooms,
                'bathrooms': bathrooms,
                'property_type': property_type,
                'description': None,
                'source': 'ZoomTanzania',
                'url': property_url,
                'scraped_date': datetime.now().isoformat()
            }
            
        except Exception as e:
            logging.warning(f"Error extracting ZoomTanzania listing: {e}")
            return None
    
    def scrape_all_sources(self, max_pages=3):
        """Scrape all configured sources"""
        logging.info("Starting comprehensive scraping...")
        
        all_listings = []
        
        # Scrape Kupatana
        kupatana_listings = self.scrape_kupatana(max_pages)
        all_listings.extend(kupatana_listings)
        
        self.random_delay(5, 10)  # Delay between sources
        
        # Scrape ZoomTanzania
        zoomtanzania_listings = self.scrape_zoomtanzania(max_pages)
        all_listings.extend(zoomtanzania_listings)
        
        # Remove duplicates based on URL
        unique_listings = []
        seen_urls = set()
        
        for listing in all_listings:
            if listing['url'] not in seen_urls:
                unique_listings.append(listing)
                seen_urls.add(listing['url'])
        
        logging.info(f"Total unique listings scraped: {len(unique_listings)}")
        return unique_listings
    
    def save_data(self, listings, filename=None):
        """Save scraped data to CSV"""
        if not listings:
            logging.warning("No data to save")
            return
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"../data/raw/scraped_properties_{timestamp}.csv"
        
        df = pd.DataFrame(listings)
        df.to_csv(filename, index=False)
        
        logging.info(f"Data saved to {filename}")
        logging.info(f"Total records: {len(df)}")
        
        return filename
    
    def generate_summary_report(self, listings):
        """Generate a summary report of scraped data"""
        if not listings:
            return
        
        df = pd.DataFrame(listings)
        
        # Basic statistics
        total_listings = len(df)
        listings_with_price = df['price_tzs'].notna().sum()
        avg_price = df['price_tzs'].mean() if listings_with_price > 0 else 0
        
        # By city
        city_counts = df['city'].value_counts().head(5)
        city_prices = df.groupby('city')['price_tzs'].mean().head(5)
        
        # By property type
        type_counts = df['property_type'].value_counts()
        
        report = f"""
📊 SCRAPING SUMMARY REPORT
==========================

📈 Total Listings: {total_listings}
💰 Listings with Price: {listings_with_price}
💵 Average Price: {avg_price:,.0f} TZS

🏙️ TOP 5 CITIES BY LISTINGS:
{city_counts.to_string()}

💲 TOP 5 CITIES BY AVERAGE PRICE:
{city_prices.to_string()}

🏠 PROPERTY TYPES:
{type_counts.to_string()}

📅 Scraped on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        # Save report
        report_filename = f"../outputs/charts/scraping_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(report_filename, 'w') as f:
            f.write(report)
        
        logging.info("Summary report generated")
        print(report)

def main():
    """Main scraping function"""
    print("🏠 Tanzania Real Estate Scraper")
    print("=" * 40)
    
    # Initialize scraper
    scraper = TanzaniaRealEstateScraper()
    
    # Scrape all sources
    print("🔍 Starting web scraping...")
    listings = scraper.scrape_all_sources(max_pages=3)
    
    if listings:
        # Save data
        filename = scraper.save_data(listings)
        print(f"✅ Data saved to: {filename}")
        
        # Generate summary report
        scraper.generate_summary_report(listings)
        
        # Show sample data
        print("\n📋 Sample Data:")
        df = pd.DataFrame(listings)
        print(df.head().to_string())
        
    else:
        print("❌ No data was scraped")

if __name__ == "__main__":
    main()
