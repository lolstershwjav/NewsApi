import requests
import csv

API_KEY = "ACTUAL API KEY"  # Replace with your actual API key

def fetch_top_headlines(api_key, country, categories, sources):
    url = f"https://newsdata.io/api/1/news?country={country}&category={','.join(categories)}&apiKey={api_key}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        headlines = response.json().get('results', [])
        return [headline for headline in headlines if headline.get('source_id') in sources]
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return []

def main():
    categories = ["business", "technology"]
    sources = ["investorplace", "forbes", "morningstar"]

    with open("csv_files/newsData.csv", mode="w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["Title", "Description", "Content", "Source", "Publication Date", "Image URL", "Category", "Link", "Keywords"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        headlines = fetch_top_headlines(API_KEY, country="us", categories=categories, sources=sources)
        for headline in headlines:
            keywords = ', '.join(headline.get('keywords', []))

            writer.writerow({
                "Title": headline['title'],
                "Description": headline.get('description', ''),
                "Content": headline.get('content', ''),
                "Source": headline.get('source_id', 'Unknown Source'),
                "Publication Date": headline.get('pubDate', ''),
                "Image URL": headline.get('image_url', ''),
                "Category": headline['category'],
                "Link": headline.get('link', ''),
                "Keywords": keywords
            })

if __name__ == "__main__":
    main()
