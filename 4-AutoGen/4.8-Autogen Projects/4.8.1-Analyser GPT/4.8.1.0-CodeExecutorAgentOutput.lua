--------------- Output-1 ---------------
content='''Here is the code
```python
print("Hello, World!")
```
'''

The result is Response(chat_message=
TextMessage(
    id='31dfa222-216f-43f7-a50a-3cd79ba55359',
    source='CodeExecutorAgent', models_usage=None, metadata={}, created_at=datetime.datetime(2025, 7, 21, 17, 59, 49, 854537, tzinfo=datetime.timezone.utc),
    content='Hello, World!\n', type='TextMessage'), inner_messages=None)

--------------- Output-2 ---------------
content='''Here is the code
```python
print("Hello, World, how are you?!")
```
'''

The result is Response(chat_message=
TextMessage(
    id='d54d4864-0610-42be-9568-4eb09b2cf1a7', 
    source='CodeExecutorAgent', models_usage=None, metadata={}, created_at=datetime.datetime(2025, 7, 21, 18, 34, 14, 291326, tzinfo=datetime.timezone.utc), 
    content='Hello, World, how are you?!\n', type='TextMessage'), inner_messages=None)

--------------- Output-3 ---------------
content='''Here is the code
```python
a=5
```
'''

The result is Response(chat_message=
TextMessage(id='cb307bd4-1786-4b66-9605-0c39342a1fc7', 
source='CodeExecutorAgent', models_usage=None, metadata={}, created_at=datetime.datetime(2025, 7, 24, 18, 8, 20, 227946, tzinfo=datetime.timezone.utc), 
content='The script ran but produced no output to console. \
         The POSIX exit code was: 0. If you were expecting output, consider revising the script \
         to ensure content is printed to stdout.', type='TextMessage'), inner_messages=None)

--------------- Output-4 ---------------
content='''Here is the code
```python
a=a+b
```
'''

The result is Response(chat_message=
TextMessage(id='7e185e43-47a7-4a1f-9b1e-5300d1820537', 
source='CodeExecutorAgent', models_usage=None, metadata={}, created_at=datetime.datetime(2025, 7, 24, 18, 13, 5, 58760, tzinfo=datetime.timezone.utc), 
content='The script ran, then exited with an error (POSIX exit code: 1)\n\
         Its output was:\nTraceback (most recent call last):\n  \
         File "/workspace/tmp_code_26d7d94d15ecbb22b047fd703c19380ddf827ffad4bb8860c4858060a78b892f.python", \
         line 1, in <module>\n    a=a+b\n      ^\nNameError: name \'a\' is not defined\n', type='TextMessage'), inner_messages=None)