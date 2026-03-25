# TalentScout Hiring Assistant Chatbot

## Project Overview
The TalentScout Hiring Assistant is an intelligent chatbot designed to assist in the initial screening of candidates for technology placements. Built with Python and Streamlit, it uses a Large Language Model (LLM) to gather essential candidate information and generate tailored technical questions based on the candidate's declared tech stack. The chatbot ensures a coherent, context-aware conversation flow, providing a seamless user experience for recruitment screening.

## Installation Instructions
1. Clone or download the repository.
2. Ensure Python 3.8+ is installed.
3. Install dependencies: `pip install -r requirements.txt`
4. Set up Google API key: Copy `.env.example` to `.env` and add your `GOOGLE_API_KEY`
5. Run the app: `streamlit run main.py`

## Usage Guide
- Launch the app using the command above.
- Interact with the chatbot through the chat interface.
- The chatbot will guide you through providing personal information and tech stack.
- Answer the generated technical questions.
- Say "bye" or "exit" to end the conversation.

## Technical Details
- **Programming Language**: Python
- **Libraries**: Streamlit for UI, google-generativeai for LLM integration, python-dotenv for environment variables
- **Model**: Gemini Pro (via Google Generative AI)
- **Architecture**: Modular design with a HiringAssistant class handling conversation logic, session state management in Streamlit for context.

## Prompt Engineering
Prompts are designed to be clear and concise:
- For information gathering: Direct questions for each field.
- For question generation: "Generate 3-5 technical questions to assess proficiency in: [tech stack]. Make them relevant and challenging."
This ensures the LLM produces appropriate outputs without deviation.

## Challenges & Solutions
- **Context Management**: Used Streamlit session state to maintain conversation history and state.
- **LLM Integration**: Handled API errors with fallbacks to mock questions.
- **Sequential Info Gathering**: Implemented a state machine to collect info step-by-step.
- **Data Privacy**: All data is stored in memory only; no persistent storage implemented for compliance.


## Optional Enhancements
- Sentiment analysis could be added using NLP libraries.
- Multilingual support via LLM prompts.
- UI improvements with custom CSS in Streamlit.
