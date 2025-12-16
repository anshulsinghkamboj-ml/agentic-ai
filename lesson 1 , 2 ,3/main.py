from agent_loop import run_agent
from dotenv import load_dotenv
import os
load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
if __name__ == "__main__":
    result = run_agent()
    print("FINAL RESULT:\n", result)
