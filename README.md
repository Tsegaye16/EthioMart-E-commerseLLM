# EthioMart-E-commerseLLM

## Amharic Data Processing and Telegram Scraper

This project is designed to scrape messages from Telegram channels, preprocess Amharic text, and analyze or tokenize the text for further usage. It is particularly tailored for handling Amharic text with proper normalization, cleaning, and tokenization.

---

## Features

- **Telegram Scraper**:

  - Fetch messages from specific Telegram channels using the Telethon library.
  - Supports media handling and metadata tracking for incremental scraping.

- **Data Preprocessing**:

  - Cleans Amharic text by removing unwanted characters, spaces, and English words.
  - Normalizes Amharic text and prepares it for further analysis.
  - Uses `nltk` and custom regex-based cleaning for Amharic-specific text.

- **Amharic Tokenization**:

  - Leverages the `AmharicSegmenter` library for tokenizing Amharic sentences and words.
  - Generates tokenized versions of the cleaned text.

- **Metadata Management**:

  - Keeps track of the last fetched and preprocessed message IDs for incremental processing.

- **Data Export**:
  - Saves cleaned and tokenized Amharic data into a CSV file for further usage or analysis.

---

## Installation

### Prerequisites

- Python 3.8 or higher
- Telegram API credentials (`API_ID` and `API_HASH`)
- Libraries: `Telethon`, `NLTK`, `langdetect`, `pandas`, `AmharicSegmenter`

### Steps

1. Clone the repository:

   ```bash
   git clone https://github.com/Tsegaye16/EthioMart-E-commerseLLM
   cd EthioMart-E-commerseLLM
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory and add your Telegram API credentials:

   ```env
   API_ID=your_api_id
   API_HASH=your_api_hash
   ```

4. Ensure `nltk` is set up:
   ```bash
   python -m nltk.downloader punkt
   ```

---

## Usage

### 1. Scraping Telegram Messages

Modify the `channels` list in the `main` function with the desired Telegram channels:

```python
channels = [
    "@ZemenExpress",
    "@nevacomputer",
    "@MerttEka",
    "@Shewabrand",
    "@Fashiontera",
    "@marakibrand"
]
```

Run the scraper:

```bash
python main.py
```

### 2. Preprocessing Amharic Data

The scraper automatically preprocesses messages after fetching. The preprocessed data will be saved in the `data/preprocessed` folder as JSON files.

### 3. Exporting Data

After preprocessing, run the following command to export the cleaned and tokenized data into a CSV file:

```bash
python export_to_csv.py
```

---

## File Structure

```
.EthioMart-E-commerseLLM
├── data/
│   ├── raw/                  # Raw scraped data
│   ├── preprocessed/         # Preprocessed data
│   └── Amharic_data.csv      # cleaned  data
│   └── tokenized_data.csv    # Final Cleaned and tokenized data
├── downloads                 # Contains the row data that fetched from Telegran channels
├── metadata/                 # Metadata for tracking processed messages
├── notebooks
│   └── tokenize.ipynb        # It tokens the Amharic text
├── scripts/
│   ├── data_preprocessor.py  # Handles text cleaning and normalization
│   ├── telegram_scraper.py   # Handles Telegram data fetching
├── .env
├── requirements.txt          # List of dependencies
├── main.py                   # Main script to run the pipeline
└── README.md                 # Project documentation
```

---

## Customization

- **Adding Channels**: Update the `channels` list in the `main` function.
- **Regex for Cleaning**: Modify `_normalize_text` in `DataPreprocessor` for custom Amharic text normalization.
- **Tokenization**: Extend or customize `tokenize_amharic` for specific tokenization needs.

---

## Dependencies

- **Core Libraries**:

  - [Telethon](https://docs.telethon.dev/)
  - [NLTK](https://www.nltk.org/)
  - [langdetect](https://pypi.org/project/langdetect/)
  - [pandas](https://pandas.pydata.org/)

- **Custom Libraries**:
  - [AmharicSegmenter](https://github.com/)

---

## Notes

- Ensure that the Telegram API credentials are correct to avoid connection issues.
- For Amharic text tokenization, make sure `AmharicSegmenter` is correctly installed and configured.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Contributing

Feel free to fork this repository, open issues, and submit pull requests for improvements or bug fixes.

---

## Contact

For questions or suggestions, reach out to **_abewatsegaye16@gmail.com_**
