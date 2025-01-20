import React from "react";
import TelegramFetcher from "./components/scrapp_telegram";

const App = () => {
  return (
    <div>
      <h1 style={{ textAlign: "center", margin: 20 }}>Telegram Data Scraper</h1>
      <TelegramFetcher />
    </div>
  );
};

export default App;
