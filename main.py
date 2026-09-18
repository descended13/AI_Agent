import os
from dotenv import load_dotenv
from openai import OpenAI
import argparse
from prompts import SYSTEM_PROMPT
from call_functions import available_functions, call_function
import json

load_dotenv()
if os.environ.get("OPENROUTER_API_KEY") == None:
	raise RuntimeError("No api key found")
api_key = os.environ.get("OPENROUTER_API_KEY")

class OpenRouterAssistant:
    def __init__(self, api_key):
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )
        self.parser = argparse.ArgumentParser(description="Chatbot")
        self.parser.add_argument("user_prompt", type=str, help="User prompt")
        self.parser.add_argument("--verbose", action='store_true', help="Enable verbose output")
        self.content = self.parser.parse_args()
        self.messages = [
                    {
                            "role": "system", 
                            "content": SYSTEM_PROMPT,
                    },
                    {
                        "role": "user",
                        "content": f"{self.content.user_prompt}",
                    }
        ]
    def create_message(self):
        completion = self.client.chat.completions.create(
            model="openrouter/free",
            messages=self.messages,
            tools=available_functions,
            # temperature=0
            )
        return completion

    def process_message(self, message):
        if message.usage:
            prompt_tokens = "Prompt tokens: "+str(message.usage.prompt_tokens)
            response_tokens = "Response tokens: "+str(message.usage.completion_tokens)
            return prompt_tokens, response_tokens
        else:
             raise RuntimeError("No usage statistics")

    def verbose_helper(self,response):
        if self.content.verbose:
            prompt_tokens, response_tokens = assistant.process_message(response)
            print("User prompt: "+self.content.user_prompt)
            print(prompt_tokens)
            print(response_tokens)
            print(response.choices[0].message.content)
        else:
            print(response.choices[0].message.content)

    def function_caller(self,response):
         message = response.choices[0].message
         for tool_call in message.tool_calls:
            result_message = call_function(tool_call)
            if result_message.get('content') is None:
                raise Exception("There is nothing in the response")
            if self.content.verbose:
                print(f"-> {result_message['content']}")
            return tool_call, result_message

assistant = OpenRouterAssistant(api_key)
messages = []
for _ in range(20):  
    try:       
        response = assistant.create_message()
        # print = assistant.verbose_helper(response)
        tool_data = assistant.function_caller(response)
        message = response.choices[0].message
        if message.content:
            assistant.messages.append({"role": "assistant", "content": message.content})
            print(f"Assistant: {message.content}")
            
        if tool_data:
            tool_call, result_message = tool_data
            assistant.messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,  
                "content": result_message['content']
            })
    except Exception as e:
        f"Error: {str(e)}"
        break