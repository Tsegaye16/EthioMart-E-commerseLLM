import json
import os
from pprint import pprint
from scripts.telegram_scrapper import TelegramScraper


def main():
    channels = [
        "@ZemenExpress", 
        "@nevacomputer", 
        "@MerttEka", 
        "@Shewabrand", 
        "@Fashiontera", 
        "@marakibrand"
    ]  # Add your target channels
    scraper = TelegramScraper()

    try:
        # Ensure the 'data' folder exists
        os.makedirs("data", exist_ok=True)

        for channel in channels:
            print(f"Fetching messages from {channel}...")
            messages = scraper.fetch_messages(channel, limit=200)

            # Save messages to a channel-specific JSON file
            file_name = f"data/{channel[1:]}.json"  # Remove '@' for the file name
            with open(file_name, "w", encoding="utf-8") as f:
                json.dump(messages, f, ensure_ascii=False, indent=4)
                print(f"Messages from {channel} saved to '{file_name}'.")

        print("\nAll messages successfully saved.")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        scraper.close()


if __name__ == "__main__":
    main()
