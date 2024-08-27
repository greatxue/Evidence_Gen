import os
os.environ['DASHSCOPE_API_KEY'] = 'sk-da1b1321d9d344a6ae18e27fac23c6ae'
from http import HTTPStatus
import dashscope

def call_with_messages():
    messages = [
        {'role': 'user', 'content': 'Question: What is the capital of France?\nOptions:\nA. Berlin\nB. Paris\nC. Madrid\nD. Rome\nPlease directly answer the letter standing for the choice.'}]
    response = dashscope.Generation.call(
        'qwen1.5-7b-chat',
        messages=messages,
        result_format='message',  # set the result is message format.
    )
    if response.status_code == HTTPStatus.OK:
        print(response)
    else:
        print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
            response.request_id, response.status_code,
            response.code, response.message
        ))


if __name__ == '__main__':
    call_with_messages()