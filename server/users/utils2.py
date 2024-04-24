from dotenv import load_dotenv
import os
import openai
import ast
from openai import OpenAI
import time
from tavily import TavilyClient
from reportlab.lib.pagesizes import letter
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import mm
from serpapi import GoogleSearch
import requests
import json
import google.generativeai as genai
from tavily import TavilyClient
import os
import re


load_dotenv()

openai_api_key1 = os.environ.get('OPENAI_API_KEY1')
openai_api_key2 = os.environ.get('OPENAI_API_KEY2')
openai_api_key3 = os.environ.get('OPENAI_API_KEY3')
tavily_api_key1 = os.environ.get('TAVILY_API_KEY1')
tavily_api_key2 = os.environ.get('TAVILY_API_KEY2')
tavily_api_key3 = os.environ.get('TAVILY_API_KEY3')
serper_api_key1 = os.environ.get('SERPER_API_KEY1')
serper_api_key2 = os.environ.get('SERPER_API_KEY2')
google_api_key1 =  os.environ.get('GOOGLE_API_KEY1')
google_api_key2 =  os.environ.get('GOOGLE_API_KEY2')
google_api_key3 =  os.environ.get('GOOGLE_API_KEY3')
print('API KEYS', google_api_key1, google_api_key2, google_api_key3)
genai.configure(api_key=google_api_key1)

google_serp_api_key = os.environ.get('GOOGLE_SERP_API_KEY')

# Set up the model
GENERATION_CONFIG = {
  "temperature": 0.9,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 2048,
}

SAFETY_SETTINGS = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_NONE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_NONE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_NONE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_NONE"
  },
]

model = genai.GenerativeModel('gemini-1.0-pro', generation_config=GENERATION_CONFIG, safety_settings=SAFETY_SETTINGS,)

def get_dict_from_json(response):
    pattern = re.compile(r'{.*}', re.DOTALL)
    match = pattern.search(response.text)
    if match:
        matched_json = match.group()
        cleaned_json = matched_json.replace('\\n', '').replace('\n', '').replace('*', '')
        try:
            data_dict = json.loads(cleaned_json)
            return data_dict
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
    else:
        print("No valid JSON found in the input string.")

def generate_module_summary(topic, level):
    print('USING GEMINI...')
    prompt_module_generation = """You are an educational assistant with knowledge in various domains. \
You will be provided with a topic and your task is to generate suitable number of module names \
that are related to the topic and a brief summary on each module. \
Make sure that each Module name should not be a subset of any other modules. \
The difficulty and level of the modules that are generated should be of {level}. \
The output should be in json format where each key corresponds to the complete module name and the \
values are the brief summary of that module.
```
Topic: {topic}
```"""
    response = model.generate_content(prompt_module_generation.format(topic=topic, level=level))
    output = get_dict_from_json(response)

    return output

def generate_submodules(module_name):
    prompt_submodules = """You are an educational assistant having knowledge in various domains. \
You will be provided with a module name and your task is to generate suitable number of \
'Sub-Modules' names that are related to the module. \
The output should be in json format where each key corresponds to the \
sub-module number and the values are the sub-module names.
Module Name: {module_name}
"""
    response = model.generate_content(prompt_submodules.format(module_name = module_name))
    output = get_dict_from_json(response)

    return output

def generate_content(output, module_name, api_key_to_use):
    prompt_content_gen = """I'm seeking your expertise on the sub-module : {sub_module_name} \which comes under the module: {module_name}.\
As a knowledgeable educational assistant, I trust in your ability to provide \
a comprehensive explanation of this sub-module. Think about the sub-module step by step and design the best way to explain the sub-module to a student. \
Your response should cover essential aspects such as definition, in-depth examples, and any details crucial for understanding the topic. \
Please generate quality content on the sub-module ensuring the response is sufficiently detailed covering all the relevant topics related to the {sub_module_name}.

In your response, organize the information into subsections for clarity and elaborate on each subsection with suitable examples if and only if it is necessary. \
Include specific hypothetical scenario-based examples (only if it is necessary) or important sub-sections related to the subject to enhance practical understanding. \
If applicable, incorporate real-world examples, applications or use-cases to illustrate the relevance of the topic in various contexts. Additionally, incorporate anything \
that helps the student to better understand the topic. \
Ensure all the relevant aspects and topics related to the sub-module is covered in your response. \
Conclude your response by suggesting relevant URLs for further reading to empower users with additional resources on the subject. \
Please format your output as valid JSON, with the following keys: title_for_the_content (suitable title for the sub-module), \
content(an introduction of the sub-module), subsections (a list of dictionaries with keys - title and content), and urls (a list).
Be a good educational assistant and craft the best way to explain the {sub_module_name}.
"""
    all_content = []
    flag = 1 if api_key_to_use== 'first' else (2 if api_key_to_use=='second' else 3 )
    print(f'THREAD {flag} RUNNING...')
    google_api_key = google_api_key1 if flag == 1 else(google_api_key2 if flag == 2 else google_api_key3)
    genai.configure(api_key=google_api_key)
    for key,val in output.items():
        model = genai.GenerativeModel('gemini-1.0-pro', generation_config=GENERATION_CONFIG, safety_settings=SAFETY_SETTINGS,)
        response = model.generate_content(prompt_content_gen.format(sub_module_name = val, module_name = module_name))
        content_output = get_dict_from_json(response)
        content_output['subject_name'] = val
        print(content_output)
        all_content.append(content_output)
    return all_content

def generate_module_summary_from_web(topic, level):
    print('USING GEMINI')
    tavily_client = TavilyClient(api_key=tavily_api_key1)
    search_result = tavily_client.get_search_context(topic, search_depth="advanced", max_tokens=4000)

    module_generation_prompt = """As an educational assistant, your goal is to craft a suitable number of {level} Level \
  educational module names and brief summaries based on a given topic and search results. \
  Ensure the module names are relevant to the topic and provide a concise summary for each. \
  Format the output in JSON, with each key representing a complete module name and its corresponding value being the brief summary.

Topic: {topic}

Search Results: {search_result}

Follow the provided JSON format diligently, incorporating information from the search results into \
the summaries and ensuring the modules are appropriately {level} in difficulty.
"""
    response = model.generate_content(module_generation_prompt.format(topic= topic, search_result = search_result, level = level))
    output = get_dict_from_json(response)

    return output

def generate_submodules_from_web(module_name, summary):
    tavily_client = TavilyClient(api_key=tavily_api_key1)
    search_result = tavily_client.get_search_context(module_name + summary, search_depth="advanced", max_tokens=4000)

    sub_module_generation_prompt= """You are an educational assistant named ISAAC. \
You will be provided with a module name and information on that module from the internet.
Your task is to generate a suitable number of 'Sub-Modules' names that are related to the modules.  \
The output should be in json format where each key corresponds to the \
sub-module number and the values are the sub-module names.

Module Name: {module_name}

Search Results: {search_result}

Follow the provided JSON format diligently.
    """
    response = model.generate_content(sub_module_generation_prompt.format(module_name = module_name, search_result = search_result))
    output = get_dict_from_json(response)

    return output

def generate_content_from_web(sub_module_name, module_name, api_key_to_use):
    print('USING GEMINI...')
    content_generation_prompt = """I'm seeking your expertise on the subject of {sub_module_name} which comes under the module: {module_name}.\
As a knowledgeable educational assistant, I trust in your ability to provide \
a comprehensive explanation of this sub-module. Think about the sub-module step by step and design the best way to explain the sub-module to a student. \
Your response should cover essential aspects such as definition, in-depth examples, and any details crucial for understanding the topic. \
You have access to the subject's information which you have to use while generating the educational content. \
Please generate quality content on the sub-module ensuring the response is sufficiently detailed covering all the relevant topics related to the sub-module.

SUBJECT INFORMATION : ```{search_result}```

--------------------------------
In your response, organize the information into subsections for clarity and elaborate on each subsection with suitable examples if and only if it is necessary. \
Include specific hypothetical scenario-based examples (only if it is necessary) or important sub-sections related to the {sub_module_name} to enhance practical understanding. \
If applicable, incorporate real-world examples, applications or use-cases to illustrate the relevance of the topic in various contexts. Additionally, incorporate anything \
that helps the student to better understand the topic. \
Ensure all the relevant aspects and topics related to the {sub_module_name} is covered in your response. \
Conclude your response by suggesting relevant URLs for further reading to empower users with additional resources on the subject. \
Please format your output as valid JSON, with the following keys: title_for_the_content (suitable title for the sub-module), \
content(an introduction of the sub-module), subsections (a list of dictionaries with keys - title and content), and urls (only a single list).
Be a good educational assistant and craft the best way to explain the {sub_module_name}."""
    flag = 1 if api_key_to_use== 'first' else (2 if api_key_to_use=='second' else 3 )
    print(f'THREAD {flag} RUNNING...')
    tavily_api_key = tavily_api_key1 if flag == 1 else(tavily_api_key2 if flag == 2 else tavily_api_key3)
    google_api_key = google_api_key1 if flag == 1 else(google_api_key2 if flag == 2 else google_api_key3)
    genai.configure(api_key=google_api_key)
    all_content = []
    tavily_client = TavilyClient(api_key=tavily_api_key)
    for key, val in sub_module_name.items():    
        print('Searching content for module:', key)
        search_result = tavily_client.get_search_context(val+module_name, search_depth="advanced", max_tokens=8000)
        model = genai.GenerativeModel('gemini-1.0-pro', generation_config=GENERATION_CONFIG, safety_settings=SAFETY_SETTINGS,)
        response = model.generate_content(content_generation_prompt.format(sub_module_name = val, search_result = search_result, module_name=module_name))
        output = get_dict_from_json(response)
        print('Module Generated:', key, '!')
        output['subject_name'] = val
        print(output)
        all_content.append(output)
        time.sleep(3)

    return all_content

def trending_module_summary_from_web(domain):
    query = 'Latest Techniques introduced in the field of ' + domain
    tavily_client = TavilyClient(api_key=tavily_api_key1)
    search_result = tavily_client.get_search_context(query, search_depth="advanced", max_tokens=4000)
    module_generation_prompt = """As an educational assistant, your goal is to craft 4-6 \
  educational module names and brief summaries based on the search results. \
  Ensure the module names are relevant and provide a concise summary for each. \
  The summary should highlight the key aspects of the modules in a way that interests the students into learning them. Example of a key: \
  'Module 1: Advanced Test Automation Techniques' and example of the corresponding summary: \
  'This module covers advanced automation techniques such as data-driven testing, cross-browser testing, and integrating automation into the CI/CD pipeline.', 'Module 2: Performance Testing and Tuning': 'This module focuses on advanced performance testing tools, techniques for load testing, stress testing, and tuning strategies to optimize software performance.'
  Format the output in JSON, with each key representing a complete module name and its corresponding value being the brief summary.

Search Results: {search_result}

Follow the provided JSON format diligently, incorporating information from the search results into the summaries.
"""
    client = OpenAI(api_key=openai_api_key1)
    completion = client.chat.completions.create(
            model = 'gpt-3.5-turbo-1106',
            messages = [
                {'role':'user', 'content': module_generation_prompt.format(search_result = search_result)},
            ],
            response_format = {'type':'json_object'},
            seed = 42,
)
    output = ast.literal_eval(completion.choices[0].message.content)
    
    return output

# def module_image_from_web(module):
#     params = {
#     "q": module,
#     "engine": "google_images",
#     "ijn": "0",
#     "api_key": google_serp_api_key
#     }

#     search = GoogleSearch(params)
#     results = search.get_dict()
#     image_results = results["images_results"]
#     image_links = [i['original'] for i in image_results[:10]]
#     return image_links

def module_image_from_web(submodules):
    print('FETCHING IMAGES...')
    keys_list = list(submodules.keys())
    images_list=[]
    for key in keys_list:
        url = "https://google.serper.dev/images"
        payload = json.dumps({
            "q": submodules[key]
        })
        headers = {
            'X-API-KEY': serper_api_key1,
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        json_response = json.loads(response.text)
        image_results = json_response["images"]
        image_links = [i["imageUrl"] for i in image_results]
        images_list.append(image_links)
    return images_list

def module_videos_from_web(submodules):
    print('FETCHING VIDEOS...')
    keys_list = list(submodules.keys())
    videos_list=[]
    for key in keys_list:
        params = {
        "q": submodules[key],
        "engine": "google_videos",
        "ijn": "0",
        "api_key": google_serp_api_key
        }

        search = GoogleSearch(params)
        results = search.get_dict()
        video_results = results["video_results"]
        yt_links = [i['link'] for i in video_results[:10]]
        videos_list.append(yt_links)
    return videos_list


def generate_pdf(pdf_file_path, modulename, module_summary, submodule_content, src_lang, video_urls):
    # Register Unicode fonts
    pdfmetrics.registerFont(TTFont('NotoSansDevanagari', 'Fonts/NotoSansDevanagari-Regular.ttf'))
    pdfmetrics.registerFont(TTFont('DejaVuSansCondensed', 'Fonts/DejaVuSansCondensed.ttf'))

    # Create a PDF document
    pdf = SimpleDocTemplate(pdf_file_path, pagesize=letter)

    # Define styles for different headings and content
    styles = {
        'Heading1': ParagraphStyle(name='Heading1', fontName='DejaVuSansCondensed', fontSize=16, spaceAfter=16, spaceBefore=16, bold=True),
        'Heading2': ParagraphStyle(name='Heading2', fontName='DejaVuSansCondensed', fontSize=14, spaceAfter=14, spaceBefore=14),
        'Heading3': ParagraphStyle(name='Heading3', fontName='DejaVuSansCondensed', fontSize=12, spaceAfter=12, spaceBefore=12),
        'Devanagari_Heading1': ParagraphStyle(name='Devanagari_Heading1', fontName='NotoSansDevanagari', fontSize=16, spaceAfter=16, spaceBefore=16, bold=True),
        'Devanagari_Heading2': ParagraphStyle(name='Devanagari_Heading2', fontName='NotoSansDevanagari', fontSize=14, spaceAfter=14, spaceBefore=14, bold=True),
        'Devanagari_Heading3': ParagraphStyle(name='Devanagari_Heading3', fontName='NotoSansDevanagari', fontSize=12, spaceAfter=12, spaceBefore=12, bold=True),
        'Normal': ParagraphStyle(name='Normal', fontName='DejaVuSansCondensed', fontSize=8, spaceAfter=8, spaceBefore=8),
        'URL': ParagraphStyle(name='URL', textColor=colors.blue, underline=True, spaceAfter=8),
    }

    # Build the PDF document
    content = [
        Image('client/src/assets/images/logo.png', width=440, height=237),
        Paragraph("Disclaimer: This content is generated by AI.", styles['Heading3']),
        Paragraph(modulename, styles['Heading1' if src_lang == 'en' else 'Devanagari_Heading1']),
        Paragraph("Module Summary:", styles['Heading2' if src_lang == 'en' else 'Devanagari_Heading2']),
        Paragraph(module_summary, styles['Heading3' if src_lang == 'en' else 'Devanagari_Heading3']),
    ]

    # Add submodule content
    for i, entry in enumerate(submodule_content):
        content.append(Paragraph(entry['subject_name'], styles['Heading2' if src_lang == 'en' else 'Devanagari_Heading2']))
        content.append(Paragraph(entry['content'], styles['Heading3' if src_lang == 'en' else 'Devanagari_Heading3']))

        # Check if there are subsections
        if 'subsections' in entry:
            for subsection in entry['subsections']:
                content.append(Paragraph(subsection['title'], styles['Heading2' if src_lang == 'en' else 'Devanagari_Heading2']))
                content.append(Paragraph(subsection['content'], styles['Heading3' if src_lang == 'en' else 'Devanagari_Heading3']))
        
        # Check if there are URLs
        if 'urls' in entry:
            content.append(Paragraph("Reference:", styles['Heading3']))
            for url in entry['urls']:
                content.append(Paragraph(url, styles['URL']))

        if video_urls[i]:
            content.append(Paragraph("Video Links:", styles['Heading3']))
            for url in video_urls[i]:
                content.append(Paragraph(url, styles['URL']))

    pdf.build(content, onFirstPage=add_page_number, onLaterPages=add_page_number)

def add_page_number(canvas, docs):
    # Add page numbers
    page_num = canvas.getPageNumber()
    text = "Page %d" % page_num
    canvas.drawRightString(200*mm, 20*mm, text)


def generate_quiz(sub_modules):
    quiz_prompt = """As an educational chatbot named ISSAC, your task is to create a set of 10 theoretical quiz questions \
with multiple-choice options that should cover all the sub-modules. The questions should be theoretical-based and difficult to \
efficiently test the theoretical knowledge of the student. \
Ensure that the output is a valid JSON format, with a single 'quizData' which is a list of dictionaries structured as follows:
```
  "question": "The question here",
  "options": ["Option A", "Option B", "Option C", "Option D"],
  "correct_option": "The correct option string here."
  "explanation": "Explanation for Question 1"

  ...[and so on]
```

Create a set of 10 quiz questions following the above-mentioned format.
```
Sub Modules : {sub_modules}
```
"""
    client = OpenAI(api_key=openai_api_key1)
    completion = client.chat.completions.create(
                model = 'gpt-3.5-turbo-1106',
                messages = [
                    {'role':'user', 'content': quiz_prompt.format(sub_modules = sub_modules)},
                ],
                response_format = {'type':'json_object'},
                seed = 42
    )
    
    print(completion.choices[0].message.content)
    output = ast.literal_eval(completion.choices[0].message.content)
    
    return output

def generate_quiz_from_web(sub_modules):
    tavily_client = TavilyClient(api_key=tavily_api_key1)
    search_result = tavily_client.get_search_context(','.join(sub_modules), search_depth="advanced", max_tokens=4000)

    quiz_prompt_for_web = """As an educational chatbot named ISAAC, your task is to create a set of 10 theoretical quiz questions \
with multiple-choice options that should cover all the sub-modules. You will be given information from the internet related to the sub-modules. \
Use this information to create the quiz questions. The questions should be theoretical-based and difficult to \
efficiently test the theoretical knowledge of the student. \

Sub Modules : {sub_modules}

Search Result = {search_result}


Ensure that the output is a valid JSON format, with a single 'quizData' which is a list of dictionaries structured as follows:
```
  "question": "The question here",
  "options": ["Option A", "Option B", "Option C", "Option D"],
  "correct_option": "The correct option string here."
  "explanation": "Explanation for Question 1"

  ...[and so on]
```

Create a set of 10 quiz questions following the above-mentioned format.

"""

    client = OpenAI(api_key=openai_api_key1)
    completion = client.chat.completions.create(
                model = 'gpt-3.5-turbo-1106',
                messages = [
                    {'role':'user', 'content': quiz_prompt_for_web.format(sub_modules = sub_modules, search_result = search_result)},
                ],
                response_format = {'type':'json_object'},
                seed = 42
    )
    
    print(completion.choices[0].message.content)
    output = ast.literal_eval(completion.choices[0].message.content)

    return output

def generate_applied_quiz(sub_modules):
    quiz_prompt = """As an educational chatbot named ISSAC, your task is to create a set of 10 creative \
        and application-based quiz questions with multiple-choice options that should be based on the sub-modules \
        as well as any related sub-topic. Create questions in a scenario-based manner like the ones in a word problem \
        or applied problems (starting with 'suppose...', 'imagine...', 'if...' or 'let's say...') to efficiently test the understanding of concepts and principles to solve real-world \
        or hypothetical situations based on the sub modules. The questions should be descriptive and lengthy to give \
        a complete scenario to the student. \
        Ensure that the output is a valid JSON format, with a single 'quizData' which is a list of dictionaries structured as follows:
```
  "question": "The question here",
  "options": ["Option A", "Option B", "Option C", "Option D"],
  "correct_option": "The correct option string here."
  "explanation": "Explanation for Question 1"

  ...[and so on]
```

Create a set of 10 quiz questions that are in the described manner and follow the above-mentioned format.

Sub Modules : {sub_modules}
"""
    client = OpenAI(api_key=openai_api_key1)
    completion = client.chat.completions.create(
                model = 'gpt-3.5-turbo-1106',
                messages = [
                    {'role':'user', 'content': quiz_prompt.format(sub_modules = sub_modules)},
                ],
                response_format = {'type':'json_object'},
                seed = 42
    )

    print(completion.choices[0].message.content)
    output = ast.literal_eval(completion.choices[0].message.content)

    return output

def generate_applied_quiz_from_web(sub_modules):
    tavily_client = TavilyClient(api_key=tavily_api_key1)
    search_result = tavily_client.get_search_context(','.join(sub_modules), search_depth="advanced", max_tokens=4000)
    quiz_prompt_for_web = """
    As an educational chatbot named ISAAC, your task is to create a diverse set of 10 creative and application-based quiz questions \
with multiple-choice options that should be based on the sub-modules. You will be given information from the internet related to the sub-modules. \
Use this information to create the quiz questions.

Sub Modules : {sub_modules}

Search Result = ```{search_result}```


Create questions in a scenario-based manner like the ones in a word problem or applied problems
to efficiently test the understanding of concepts and principles to solve real-world or hypothetical situations based on the sub modules. \
The questions should be descriptive and should provide hypothetical scenarios to give a complete scenario to the student. \

Ensure that the output is a valid JSON format, with a single 'quizData' which is a list of dictionaries structured as follows:
```
  "question": "The question here",
  "options": ["Option A", "Option B", "Option C", "Option D"],
  "correct_option": "The correct option string here."
  "explanation": "Explanation for Question 1"

  ...[and so on]
```

Create a set of 10 questions that follow the described manner and the above-mentioned format.
"""
    client = OpenAI(api_key=openai_api_key1)
    completion = client.chat.completions.create(
                model = 'gpt-3.5-turbo-1106',
                messages = [
                    {'role':'user', 'content': quiz_prompt_for_web.format(sub_modules = sub_modules, search_result = search_result)},
                ],
                response_format = {'type':'json_object'},
                seed = 42
    )

    print(completion.choices[0].message.content)
    output = ast.literal_eval(completion.choices[0].message.content)

    return output

def generate_conversation_quiz(sub_modules):
    quiz_prompt = """You are an educational examiner and your task is to ask various conceptual questions to a student(asking them to explain or elaborate their answers) \
based on the specified list of topics. \
Imagine as if you are talking to the student while asking the questions.
Ensure that the output is a valid JSON format, with the keys being the question number and values being the questions.

Create a set of 1 concept-based quiz questions in the above-mentioned format.
```
Sub Modules : {sub_modules}
```
"""
    client = OpenAI(api_key=openai_api_key1)
    completion = client.chat.completions.create(
                model = 'gpt-3.5-turbo-1106',
                messages = [
                    {'role':'user', 'content': quiz_prompt.format(sub_modules = sub_modules)},
                ],
                response_format = {'type':'json_object'},
                seed = 42
    )

    print(completion.choices[0].message.content)
    output = ast.literal_eval(completion.choices[0].message.content)
    output_list = list(output.values())

    return output_list

def generate_conversation_quiz_from_web(sub_modules):
    tavily_client = TavilyClient(api_key=tavily_api_key1)
    search_result = tavily_client.get_search_context(','.join(sub_modules), search_depth="advanced", max_tokens=4000)
    quiz_prompt = """You are an educational examiner and your task is to ask various conceptual questions to a student (asking them to explain or elaborate their answers) \
based on the specified list of topics. \
Imagine as if you are talking to the student while asking the questions. You will be given information from the internet related to the sub-modules. \
Use this information to create the questions.

Sub Modules : ```{sub_modules}```

Search Result = ```{search_result}```

Ensure that the output is a valid JSON format, with the keys being the question number and values being the questions.

Create a set of 1 concept-based quiz questions in the above-mentioned format.

"""
    client = OpenAI(api_key=openai_api_key1)
    completion = client.chat.completions.create(
                model = 'gpt-3.5-turbo-1106',
                messages = [
                    {'role':'user', 'content': quiz_prompt.format(sub_modules = sub_modules, search_result = search_result)},
                ],
                response_format = {'type':'json_object'},
                seed = 42
    )

    print(completion.choices[0].message.content)
    output = ast.literal_eval(completion.choices[0].message.content)
    output_list = list(output.values())

    return output_list

def evaluate_conversation_quiz(question_and_response):
    questions = [list(i.keys())[0] for i in question_and_response]
    answers = [list(i.values())[0] for i in question_and_response]
    evaluation_prompt = """ You are a strict grader. You will be given a set of questions asked by an examiner along with the corresponding set of answers that \
    was given by the student. Your task is to provide an overall grade to the specified parameters for the answers on a scale of 1 to 10, \
    with 0 being very bad and 10 being the best. \
    You are supposed to provide an aggregate score to all the answers at once. Don't score each answer separately. The description of the parameters is provided to you. \
    Here is the description of the parameters:
```
Accuracy: The answer should be accurate and correct, with no factual errors or misunderstandings.
Completeness: The answer should cover all the relevant aspects of the question and provide a comprehensive response.
Clarity: The answer should be clear and easy to understand, with well-organized thoughts and ideas. If the question is technical, technical terms should be preferred.
Relevance: The answer should stay focused on the question and not include irrelevant information or tangents.
Understanding: The answer should demonstrate a deep understanding of the topic, with thoughtful analysis and insights.
```

List of questions asked by the examiner: ```{questions}```
Corresponding list of answers: ```{answers}```

Please provide a strict overall score to the parameters accordingly as well as feedback to the user on the parts they can improve on. If the answers are short and incomplete \
provide a low score in the respective parameters and give an appropriate feedback. Also, specify the questions in case the user gave a wrong answer to it.

Make sure your output is a valid json where the keys are the accuracy, \
completeness, clarity, relevance, understanding and feedback.
"""
    client = OpenAI(api_key=openai_api_key1)
    completion = client.chat.completions.create(
                model = 'gpt-3.5-turbo-1106',
                messages = [
                    {'role':'user', 'content': evaluation_prompt.format(questions = questions, answers = answers)},
                ],
                response_format = {'type':'json_object'},
                seed = 42
    )

    print(completion.choices[0].message.content)
    output = ast.literal_eval(completion.choices[0].message.content)

    return output

def generate_recommendations(user_course, user_interest, past_module_names = None):
    if not past_module_names:
        print('RECOMMENDATIONS WITHOUT PAST MODULES')
        recc_prompt = '''You will be provided with a student's area of interest and course he is enrolled in \
        and your task is to generate recommendations of similar courses for the user. Generate 10 module names \
        that are the most similar to these parameters. The output should be in json format \
        where each key corresponds to the recommended course name and the value is a short description about \
        the recommeded course.
        User Course: {user_course}
        User Interests: {user_interest}

        Example output:
        ```json
        course name here : course summary here
        ```
'''

        client = OpenAI(api_key = openai_api_key1)

        completion = client.chat.completions.create(
                    model = 'gpt-3.5-turbo-1106',
                    messages = [
                        {'role':'user', 'content': recc_prompt.format(user_course = user_course, user_interest= user_interest)},
                    ],
                    response_format = {'type':'json_object'},
                    seed = 42
        )
        output = ast.literal_eval(completion.choices[0].message.content)

    else:
        print('RECOMMENDATIONS WITH PAST MODULES')
        recc_prompt = '''You will be provided with a student's area of interest, course he is enrolled in \
        as well as past module names the user has completed. Your task is to generate recommendations of similar courses for the user. Generate 10 module names \
        that are the most similar to these parameters. The output should be in json format \
        where each key corresponds to the recommended course name and the value is a short description about \
        the recommeded course.
        User Course: {user_course}
        User Interests: {user_interest}
        Past Module Names: {past_module_names}

        Example output:
        ```json
        course name here : course summary here
        ```
        '''
        client = OpenAI(api_key = openai_api_key1)

        completion = client.chat.completions.create(
                    model = 'gpt-3.5-turbo-1106',
                    messages = [
                        {'role':'user', 'content': recc_prompt.format(user_course = user_course, user_interest = user_interest, past_module_names = past_module_names)},
                    ],
                    response_format = {'type':'json_object'},
                    seed = 42
        )
        incomplete_output = ast.literal_eval(completion.choices[0].message.content)
        print("incomplete",incomplete_output)
        output=""
        if "Recommended Courses" in incomplete_output.keys():
            output = incomplete_output['Recommended Courses']
        else:
            output = incomplete_output

    return output

def generate_module_from_textbook(topic, vectordb):
  relevant_docs = vectordb.similarity_search('Important modules or topics on '+ topic)
  rel_docs = [doc.page_content for doc in relevant_docs]
  context = '\n'.join(rel_docs)
  module_generation_prompt = """You are an educational assistant with knowledge in various domains. A student is seeking your expertise \
  to learn a given topic. You will be provided with context from their textbook \
  and your task is to design course modules to complete all the major concepts about the topic in the textbook. Craft a suitable number of \
  module names for the student to learn the topic they wish. \
  Ensure the module names are relevant to the topic using the context provided to you. \
  You MUST only use the knowledge provided in the context to craft the module names. \
  The output should be in json format where each key corresponds to the \
  sub-module number and the values are the sub-module names. Do not consider summary or any irrelevant topics as module names.

Topic: {topic}

Context: {context}

Follow the provided JSON format diligently."""
  response = model.generate_content(module_generation_prompt.format(topic= topic, context = context))
  output = get_dict_from_json(response)

  return output

def generate_content_from_textbook(module_name, output, profile, vectordb, api_key_to_use):
    prompt= """I'm seeking your expertise on the subject of {sub_module_name} which comes under the module: {module_name}.\
As a knowledgeable educational assistant, I trust in your ability to provide \
a comprehensive explanation of this sub-module. Think about the sub-module step by step and design the best way to explain the sub-module to me. \
Your response should cover essential aspects such as definition, in-depth examples, and any details crucial for understanding the topic. \
You have access to the subject's information which you have to use while generating the educational content. \
Please generate quality content on the sub-module ensuring the response is sufficiently detailed covering all the relevant topics related to the {sub_module_name}. You will also \
be provided with my course requirements and needs. Structure the course according to my needs.

MY COURSE REQUIREMENTS : {profile}

SUBJECT INFORMATION : {context}

--------------------------------
In your response, organize the information into subsections for clarity and elaborate on each subsection with suitable examples if and only if it is necessary. \
If applicable, incorporate real-world examples, applications or use-cases to illustrate the relevance of the topic in various contexts. Additionally, incorporate anything \
that helps the student to better understand the topic. \
Please format your output as valid JSON, with the following keys: title_for_the_content (suitable title for the sub-module), \
content(the main content of the sub-module), subsections (a list of dictionaries with keys - title and content).
Be a good educational assistant and craft the best way to explain the {sub_module_name} following my course requirement strictly..
  """
    
    all_content = []
    flag = 1 if api_key_to_use== 'first' else (2 if api_key_to_use=='second' else 3 )
    print(f'THREAD {flag} RUNNING...')
    google_api_key = google_api_key1 if flag == 1 else(google_api_key2 if flag == 2 else google_api_key3)
    genai.configure(api_key=google_api_key)
    for key,val in output.items():
        relevant_docs = vectordb.similarity_search(val)
        rel_docs = [doc.page_content for doc in relevant_docs]
        context = '\n'.join(rel_docs)

        model = genai.GenerativeModel('gemini-1.0-pro', generation_config=GENERATION_CONFIG, safety_settings=SAFETY_SETTINGS,)
        response = model.generate_content(prompt.format(sub_module_name = val, module_name = module_name, profile= profile, context=context))

        print("Thread 1: Module Generated: ",key,"!")   
        content_output = get_dict_from_json(response)
        print('CONTENT OUTPUT\n\n', content_output)
        content_output['subject_name'] = val
        print(content_output)
        all_content.append(content_output)

    return all_content