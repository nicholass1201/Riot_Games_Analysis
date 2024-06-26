# Riot Games Analysis

This project is a web application that provides an analysis generated by OpenAI's GPT-3.5 model on the player's performance in a League of Legends game. The application consists of a React frontend and a FastAPI backend.

## Features

- Fetches match data using the Riot Games API.
- Analyzes match data using OpenAI's GPT-3.5 model.
- Provides detailed and humorous commentary on player performance.
- Supports custom games with specific messaging.
- Retains user data across page refreshes using localStorage.

## Technologies

- **Front End**: React
- **Back End**: FastAPI
- **APIs**: Riot Games API, OpenAI API
- **Language Model Integration**: LangChain

## Installation

### Back End

1. Navigate to the `backend` directory.
2. Create a `.env` file and add your API keys in this format:
    ```
    RIOT_API_KEY=your_riot_api_key
    OPENAI_API_KEY=your_openai_api_key
    ```
3. Install the dependencies:
    ```
    pip install fastapi uvicorn pydantic requests python-dotenv langchain-openai
    ```
4. Run the FastAPI server:
    ```
    uvicorn main:app --reload
    ```

### Front End

1. Navigate to the `frontend` directory.
2. Install npm packages:
    ```
    npm install
    ```
3. Start the React application:
    ```
    npm start
    ```

## Usage

1. Navigate to [http://localhost:3000](http://localhost:3000) in your desired browser.
2. Enter your League of Legends player name and tag, then click "Submit".
3. Select a match from the list and click "Analyze".
4. View the detailed match analysis generated by GPT-3.5 as well as the data graph.

## Example

### Match Analysis

The carry of this match was undoubtedly NickNickNick on Aatrox. With 14 kills, 12 deaths, and 9 assists, NickNickNick dealt a whopping 52,628 damage to champions, earned 16,087 gold, and reached level 18. Despite his deaths, his significant damage output and gold earned make him the standout player in this game. It's safe to say that NickNickNick carried his team to victory with his performance. On the other hand, the most useless player in this match was AmazonFireTV on Bard. With only 1 kill, 6 deaths, and a staggering 31 assists, AmazonFireTV's damage dealt to champions was a mere 15,646, and he earned 11,263 gold. His vision score of 96 may have been impressive, but his lackluster performance in terms of kills and damage dealt makes him the least useful human being in this game. Maybe Bard's skills were better suited for playing instruments rather than battling on the Rift. In conclusion, while NickNickNick shone as the carry with his Aatrox performance, AmazonFireTV's Bard failed to make a significant impact in the match. Remember, in League of Legends, sometimes it's better to stick to playing music rather than trying to be a hero on the battlefield.

## License

This project is licensed under the MIT License.
