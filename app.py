import json
import os


from graph_utils.graph import build_graph


from dotenv import load_dotenv

load_dotenv()

os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

runnable = build_graph()

print('Type your questions about World Happiness Index.')

topic = input('Enter the topic of the PDF: ')

while True:
    user_input = input('Enter question ("q" to exit): ')
    if user_input.lower() == 'q':
        break

    out = runnable.invoke({
        'topic': topic,
        'input': user_input,
        'chat_history': []
    })
        
    print(json.loads(out['agent_out'])['answer'])
