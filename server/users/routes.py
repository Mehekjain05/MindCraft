from flask import request, session, jsonify,  Blueprint, send_file
from server import db, bcrypt
from server.models import User, Topic, Module, Query, CompletedModule, OngoingModule,PersonalizedCompletedModule,PersonalizedModule,PersonalizedOngoingModule
from concurrent.futures import ThreadPoolExecutor
import os
from flask_cors import cross_origin
from server.users.utils2 import *
from deep_translator import GoogleTranslator
from lingua import LanguageDetectorBuilder
from iso639 import Lang
from server.recommender_system.recommendations import recommend_module, popular_topics
from sqlalchemy import desc
from gtts import gTTS
from io import BytesIO
from datetime import datetime
from werkzeug.utils import secure_filename
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
import secrets
import string

users = Blueprint(name='users', import_name=__name__)

# Detector for language detection
detector = LanguageDetectorBuilder.from_all_languages().with_preloaded_language_models().build()

device_type = 'cpu'

model_name = "BAAI/bge-small-en-v1.5"

encode_kwargs = {'normalize_embeddings': True} # set True to compute cosine similarity

EMBEDDINGS = HuggingFaceBgeEmbeddings(
    model_name=model_name,
    model_kwargs={'device': device_type },
    encode_kwargs=encode_kwargs
)


FEATURE_DOCS_PATH = 'assistant_data/Description.pdf'
loader = PyPDFLoader(FEATURE_DOCS_PATH)
docs = loader.load()
docs_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
split_docs = docs_splitter.split_documents(docs)
NYAYMITRA_FEATURES_VECTORSTORE = FAISS.from_documents(split_docs, EMBEDDINGS)
NYAYMITRA_FEATURES_VECTORSTORE.save_local('assistant_data/faiss_index_assistant')
print('CREATED VECTORSTORE')
VECTORDB = FAISS.load_local('assistant_data/faiss_index_assistant', EMBEDDINGS, allow_dangerous_deserialization=True)



tools = [
    # {
    #     'type': 'function',
    #     'function': {

    #         'name': 'retrieval_augmented_generation',
    #         'description': 'Use to answer questions about the MindCraft platform. ONLY use this to retrieve information about the platform. Do not use this to answer questions that are not about the platform.',
    #         'parameters': {
    #             'type': 'object',
    #             'properties': {
    #                 'query': {
    #                     'type': 'string',
    #                     'description': 'The query to use for searching the information database of Mindcraft'
    #                 },
    #             },
    #             'required': ['query']
    #         }
    #     }
    # },
    {
        'type': 'function',
        'function': {
            'name': 'get_context_from_page',
            'description': 'Get information about the current page that the user is exploring. Used to answer user queries related to the current page they\'re exploring.',

            }
    }
]

# register route  --> take username from client only store in database if username is not taking
@users.route('/register',methods=['POST'])
@cross_origin(supports_credentials=True)
def register():
    # take user input
    fname = request.form['firstName']  # Access the 'fname' variable from the JSON data
    lname = request.form['lastName']
    email = request.form['email']
    password = request.form['password']
    country = request.form['country']
    state = request.form['state']
    city = request.form['city']
    gender = request.form['gender']
    age = request.form['age']
    college_name = request.form['college']
    course_name = request.form['course']
    interests = request.form['interest']
    student_id_file = request.files['collegeId']
    # check if user has already registered by same email
    print("id of the colege------",request.form)
    user_exists = User.query.filter_by(email=email).first() is not None

    if user_exists:
        return jsonify({"message": "User already exists", "response":False}), 201
    
    # hash password, create new user save to database
    hash_pass = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(fname=fname, lname=lname, email=email, password=hash_pass, country=country, state=state, city=city, gender=gender, age=age, college_name=college_name, course_name=course_name, interests=interests, student_id=student_id_file.read())
    db.session.add(new_user)
    db.session.commit()

    response = jsonify({"message": "User created successfully", "id":new_user.user_id, "email":new_user.email, "response":True}), 200
    return response


# login route  --> add username to session and make it unique in user model
@users.route('/login', methods=['POST'])
@cross_origin(supports_credentials=True)
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    # check user is registered or not
    user = User.query.filter_by(email=email).first()
    if user is None:
        return jsonify({"message": "Unregistered email id", "response":False}), 200
    
    # check password
    if not bcrypt.check_password_hash(user.password, password.encode('utf-8')):
        return jsonify({"message": "Incorrect password", "response":False}), 200
    
    # start user session
    session["user_id"] = user.user_id
    print("user id in session:-",session.get('user_id'))
    profile = f"This a profile of user, Name: {user.fname} {user.lname}, Email: {user.email}, Country: {user.country}, Age: {user.age}, Ongoing Course Name: {user.course_name}, User Interest: {user.interests}"
    print("Profile",profile)
    # create assistant for user
    client = OpenAI(api_key = openai_api_key1)
    assistant = client.beta.assistants.create(
        name="MINDCRAFT",
        instructions=f"You are ISSAC, a helpful assistant for the website Mindcraft. Use the functions provided to you to answer user's question about the Mindcraft platform. {profile}",
        model="gpt-3.5-turbo-1106",
        tools=tools
    )
    thread = client.beta.threads.create()

    session['thread_id'] = thread.id
    session['assistant_id'] = assistant.id


    return jsonify({"message": "User logged in successfully", "email":user.email, "response":True}), 200


@users.route('/user_profile', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def user_profile():
    # check if user is logged in
    user_id = session.get("user_id", None)
    if user_id is None:
        return jsonify({"message": "User not logged in", "response":False}), 401
    
    # check if user exists
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"message": "User not found", "response":False}), 404
    
    if request.method == 'POST':
        data = request.json
        print("data is printed---------",data)
        user.fname = data.get("fname")
        user.lname = data.get("lname")
        user.email = data.get("email")
        user.country = data.get("country")
        user.state = data.get("state")
        user.gender = data.get("gender")
        user.city = data.get("city")
        user.age = data.get("age")
        user.interests = data.get("interests")
        user.college_name = data.get("college_name")
        user.course_name = data.get("course_name")
        db.session.commit()
    
    user_info = {}
    user_info['fname'] = user.fname
    user_info['lname'] = user.lname
    user_info['email'] = user.email
    user_info['country'] = user.country
    user_info['state'] = user.state
    user_info['city'] = user.city
    user_info['age'] = user.age
    user_info['gender'] = user.gender
    user_info['interests'] = user.interests
    user_info['date_joined'] = user.date_joined
    user_info['college_name'] = user.college_name
    user_info['course_name'] = user.course_name

    return jsonify({"message": "User found", "user_info":user_info, "response":True}), 200


@users.route('/user_dashboard', methods=['GET'])
@cross_origin(supports_credentials=True)
def getuser():
    # check if user is logged in
    user_id = session.get("user_id", None)
    if user_id is None:
        return jsonify({"message": "User not logged in", "response":False}), 401
    
    # check if user exists
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"message": "User not found", "response":False}), 404
    
    completed_modules = []
    ongoing_modules = []

    user_ongoing_modules = user.user_onmodule_association
    user_completed_modules = user.user_module_association
    user_course = user.course_name
    user_interest = user.interests
    all_ongoing_modules_names = ""
  
    for comp_module in user_ongoing_modules:
        temp = {}
        module = Module.query.get(comp_module.module_id)
        topic = Topic.query.get(module.topic_id)
        temp['module_name'] = module.module_name
        temp['topic_name'] = topic.topic_name
        temp['module_summary'] = module.summary
        temp['level'] = module.level
        all_ongoing_modules_names += f"{module.module_name},"
        c_module = CompletedModule.query.filter(CompletedModule.module_id==comp_module.module_id,CompletedModule.user_id==user_id).first()
        if c_module:
            if c_module.theory_quiz_score is not None and c_module.application_quiz_score is not None and c_module.assignment_score is not None:
                temp['quiz_score'] = [c_module.theory_quiz_score, c_module.application_quiz_score, c_module.assignment_score]
                completed_modules.append(temp)
            else:
                temp['date_started'] = comp_module.date_started.strftime("%d/%m/%Y %H:%M")
                quiz_list = [c_module.theory_quiz_score, c_module.application_quiz_score, c_module.assignment_score]
                temp['quiz_score'] = [x for x in quiz_list if x is not None]
                ongoing_modules.append(temp)
        else:
            temp['date_started'] = comp_module.date_started.strftime("%d/%m/%Y %H:%M")
            temp['quiz_score'] = []
            ongoing_modules.append(temp)
            

        
    query_message = ""
    user_queries = user.user_query_association
    # if user_queries is None:
    #     query_message = "You have not searched for any topic yet. Please search for a topic to get recommendations."
    #     recommended_topics = popular_topics()
    #     recommended_topic_names = [Topic.query.get(topic_id).topic_name for topic_id in recommended_topics]

    #     return jsonify({"message": "User found", "query_message":query_message,"recommended_topics":recommended_topic_names, "user_ongoing_modules":ongoing_modules, "user_completed_module":completed_modules, "response":True}), 200
    # else:
    # latest_query = Query.query.filter_by(user_id=1).order_by(desc(Query.date_search)).first() 
    # base_module = Module.query.filter_by(topic_id=latest_query.topic_id).first()
    # recommended_modules = recommend_module(base_module.module_id)
    recommended_modules = generate_recommendations(user_course, user_interest, all_ongoing_modules_names)
    print(recommended_modules)
    print("Ongoing :-----------",ongoing_modules)
    # recommended_module_summary = {}
    # for module_id in recommended_modules:
    #     module = Module.query.get(module_id)
    #     recommended_module_summary[module.module_name] = module.summary
        
    return jsonify({"message": "User found", "query_message":query_message,"recommended_topics":recommended_modules, "user_ongoing_modules":ongoing_modules, "user_completed_module":completed_modules, "response":True}), 200

# logout route
@users.route('/logout', methods=['GET'])
@cross_origin(supports_credentials=True)
def logout():
    session.pop("user_id", None)
    return jsonify({"message": "User logged out successfully", "response":True}), 200



# delete user route --> user dependent queries and completed topics will also be deleted no need to delete them separately
@users.route('/delete', methods=['DELETE'])
@cross_origin(supports_credentials=True)
def delete():
    # check if user is logged in
    user_id = session.get("user_id", None)
    if user_id is None:
        return jsonify({"message": "User not logged in", "response":False}), 401
    
    # check if user exists
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"message": "User not found", "response":False}), 404
    
    # select all queries and completed topics by user and delete them
    # user_saved_queries = user.queries
    # user_saved_topics = user.completed_topics

    db.session.delete(user)
    # db.session.delete(user_saved_queries)
    # db.session.delete(user_saved_topics)
    db.session.commit()

    # return response
    return jsonify({"message": "User deleted successfully", "response":True}), 200


@users.route('/query2/trending/<string:domain>', methods=['GET'])
@cross_origin(supports_credentials=True)
def trending_data(domain):
    text=trending_module_summary_from_web(domain)
    print(text)
    return jsonify({"message": "Query successful", "domain": domain,  "content": text, "response":True}), 200


@users.route('/query2/trending/<string:domain>/<string:module_name>/<string:summary>/<string:source_lang>', methods=['GET'])
@cross_origin(supports_credentials=True)
def trending_query(domain, module_name, summary, source_lang):
    # check if user is logged in
    user_id = session.get("user_id", None)
    if user_id is None:
        return jsonify({"message": "User not logged in", "response":False}), 401
    
    # check if user exists
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"message": "User not found", "response":False}), 404
    
    topic = Topic.query.filter_by(topic_name=domain.lower()).first()
    if topic is None:
        topic = Topic(topic_name=domain.lower())
        db.session.add(topic)
        db.session.commit()

    module = Module.query.filter_by(module_name=module_name, topic_id=topic.topic_id, level='trending', websearch=True).first()
    if module is not None:
        trans_submodule_content = translate_submodule_content(module.submodule_content, source_lang)
        print(f"Translated submodule content: {trans_submodule_content}")
        return jsonify({"message": "Query successful", "images": module.image_urls, "content": trans_submodule_content, "response": True}), 200
    
    # add module to database
    new_module = Module(module_name=module_name, topic_id=topic.topic_id, level='trending', websearch=True, summary=summary)
    db.session.add(new_module)
    db.session.commit()

    images = module_image_from_web(module.module_name)
    with ThreadPoolExecutor() as executor:
        submodules = generate_submodules_from_web(module.module_name,module.summary)
        print(submodules)
        keys_list = list(submodules.keys())
        submodules_split_one = {key: submodules[key] for key in keys_list[:3]}
        submodules_split_two = {key: submodules[key] for key in keys_list[3:]}
        future_content_one = executor.submit(generate_content_from_web, submodules_split_one, 'first')
        future_content_two = executor.submit(generate_content_from_web, submodules_split_two, 'second')

        content_one = future_content_one.result()
        content_two = future_content_two.result()

        content = content_one + content_two 

        module.submodule_content = content
        module.image_urls = images
        db.session.commit()

        # translate submodule content to the source language
        trans_submodule_content = translate_submodule_content(content, source_lang)
        print(f"Translated submodule content: {trans_submodule_content}")

        return jsonify({"message": "Query successful", "images": module.image_urls, "content": trans_submodule_content, "response": True}), 200

def translate_module_summary(content, target_language):
    if target_language=='en':
        return content
    
    trans_content = {}
    for key, value in content.items():
        trans_key = GoogleTranslator(source='en', target=target_language).translate(str(key))
        trans_content[trans_key] = GoogleTranslator(source='en', target=target_language).translate(str(value))
    return trans_content

def translate_submodule_content(content, target_language):
    if target_language=='en':
        return content
    
    trans_content = []
    for entry in content:
        temp = {}
        for key, value in entry.items():
            if key == 'urls':
                temp[key] = value
                continue
            if key == 'subsections':
                temp[key] = []
                for subsection in value:
                    temp_subsections = {}
                    for sub_key, sub_value in subsection.items():
                        temp_subsections[sub_key] = GoogleTranslator(source='auto', target=target_language).translate(str(sub_value))
                    temp[key].append(temp_subsections)
            else:
                temp[key] = GoogleTranslator(source='auto', target=target_language).translate(str(value))
        trans_content.append(temp)
    return trans_content

def translate_quiz(quiz_data, target_language):
    if target_language=='en':
        return quiz_data
    
    trans_quiz=[]
    for entry in quiz_data:
        temp = {}
        for key, val in entry.items():
            if key != 'options':
                temp[key] = GoogleTranslator(source='auto', target=target_language).translate(str(val))
            else:
                temp[key] = []
                for option in val:
                    temp[key].append(GoogleTranslator(source='auto', target=target_language).translate(str(option)))

        trans_quiz.append(temp)
    
    return trans_quiz

def translate_assignment(questions, target_language):
    if target_language=='en':
        return questions
    
    trans_questions=[]
    for entry in questions:
        trans_questions.append(GoogleTranslator(source='auto', target=target_language).translate(str(entry)))

    return trans_questions

def translate_responses(responses, target_language):
    if target_language=='en':
        return responses
    
    trans_response = []
    for entry in responses:
        temp = {}
        for key, val in entry.items():
            temp[key] = GoogleTranslator(source='auto', target=target_language).translate(str(val))
        trans_response.append(temp)
    
    return trans_response

def translate_evaluations(evaluations, target_language):
    if target_language=='en':
        return evaluations
    
    trans_eval = {}
    for key, val in evaluations.items():
        trans_eval[key] = GoogleTranslator(source='auto', target=target_language).translate(str(val))

    return trans_eval

@users.route('/query2/doc-upload/<string:topicname>/<string:level>/<string:source_lang>',methods=['POST'])
def doc_query_topic(topicname,level,source_lang):
    user_id = session.get('user_id')
    print(session.get('user_id'))
    if user_id is None:
        return jsonify({"message": "User not logged in", "response":False}), 401
    
    # check if user exists
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"message": "User not found", "response":False}), 404
    websearch ='false'
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    if not os.path.exists("uploads"):
        os.makedirs("uploads")
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join("uploads", filename))
    
    DOCS_PATH = os.path.join("uploads", filename)
    loader = PyPDFLoader(DOCS_PATH)
    docs = loader.load()
    docs_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    split_docs = docs_splitter.split_documents(docs)
    TEXTBOOK_VECTORSTORE = FAISS.from_documents(split_docs, EMBEDDINGS)
    TEXTBOOK_VECTORSTORE.save_local('user_docs')
    print('CREATED VECTORSTORE')
    VECTORDB_TEXTBOOK = FAISS.load_local('user_docs', EMBEDDINGS, allow_dangerous_deserialization=True)

    # language detection for input provided
    if source_lang == 'auto':
        source_language = Lang(str(detector.detect_language_of(topicname)).split('.')[1].title()).pt1
        print(f"Source Language: {source_language}")
    else:
        source_language=source_lang
        print(f"Source Language: {source_language}")

    # translate other languages input to english
    trans_topic_name = GoogleTranslator(source='auto', target='en').translate(topicname)
    print(f"Translated topic name: {trans_topic_name}")

    # check if topic exists in database along with its modulenames and summaries
    topic = Topic.query.filter_by(topic_name=trans_topic_name.lower()).first()
    if topic is None:
            topic = Topic(topic_name=trans_topic_name.lower())
            db.session.add(topic)
            db.session.commit()
            print(f"topic added to database: {topic}")

    
    module_summary_content = generate_module_from_textbook(trans_topic_name,level,VECTORDB_TEXTBOOK)    
    print("Content",module_summary_content)
    module_ids = {}
    for modulename, modulesummary in module_summary_content.items():
        new_module = Module(
            module_name=modulename,
            topic_id=topic.topic_id,
            websearch=websearch,
            level=level,
            summary=modulesummary
        )
        db.session.add(new_module)
        db.session.commit()
        module_ids[modulename] = new_module.module_id

    # add user query to database
    new_user_query = Query(user_id=user.user_id, topic_id=topic.topic_id, level=level, websearch=websearch, lang=source_language)
    db.session.add(new_user_query)
    db.session.commit()

    trans_moduleids = {}
    if source_language !='en':
        for key, value in module_ids.items():
            trans_key = GoogleTranslator(source='en', target=source_language).translate(str(key))
            trans_moduleids[trans_key]=value
        module_ids=trans_moduleids
    # translate module summary content to source language
    trans_module_summary_content = translate_module_summary(module_summary_content, source_language)
    print(f"Translated module summary content: {trans_module_summary_content}")

    return jsonify({"message": "Query successful", "topic_id":topic.topic_id, "topic":trans_topic_name, "source_language":source_language, "module_ids":module_ids, "content": trans_module_summary_content, "response":True}), 200


@users.route('/query2/doc-upload',methods=['POST'])
def personalized_module():
    user_id = session.get('user_id')
    print(session.get('user_id'))
    if user_id is None:
        return jsonify({"message": "User not logged in", "response":False}), 401
    
    # check if user exists
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"message": "User not found", "response":False}), 404
    
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    if not os.path.exists("uploads"):
        os.makedirs("uploads")
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join("uploads", filename))
    title = request.form['title']
    description = request.form['description']
    session['user_profile']=description
    session['title']=title
    DOCS_PATH = os.path.join("uploads", filename)
    loader = PyPDFLoader(DOCS_PATH)
    docs = loader.load()
    docs_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    split_docs = docs_splitter.split_documents(docs)
    TEXTBOOK_VECTORSTORE = FAISS.from_documents(split_docs, EMBEDDINGS)
    TEXTBOOK_VECTORSTORE.save_local('user_docs')
    print('CREATED VECTORSTORE')
    VECTORDB_TEXTBOOK = FAISS.load_local('user_docs', EMBEDDINGS, allow_dangerous_deserialization=True)
    submodules = generate_module_from_textbook(title,VECTORDB_TEXTBOOK)
    values_list = list(submodules.values())
    session['submodules']=submodules
    return jsonify({"message": "Query successful","submodules":values_list,"response":True}), 200

@users.route('/query2/doc_generate_content',methods=['GET'])
def personalized_module_content():
    user_id = session.get("user_id", None)
    if user_id is None:
        return jsonify({"message": "User not logged in", "response": False}), 401
    
    # check if user exists
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"message": "User not found", "response": False}), 404
    source_language ="en"
    characters = string.ascii_letters + string.digits  # Alphanumeric characters
    key = ''.join(secrets.choice(characters) for _ in range(7))
    title=session['title']
    description=session['user_profile']
    VECTORDB_TEXTBOOK = FAISS.load_local('user_docs', EMBEDDINGS, allow_dangerous_deserialization=True)
    # new_module = PersonalizedModule(
    #     module_code=key,
    #     module_name=modulename,
    #     summary=modulesummary
    # )
    # db.session.add(new_module)
    # db.session.commit()
    # check if submodules are saved in the database for the given module_id
    print("language",source_language)
    with ThreadPoolExecutor() as executor:
        submodules = session['submodules']
        keys_list = list(submodules.keys())
        future_images_list = executor.submit(module_image_from_web, submodules)
        future_video_list = executor.submit(module_videos_from_web, submodules)
        submodules_split_one = {key: submodules[key] for key in keys_list[:3]}
        submodules_split_two = {key: submodules[key] for key in keys_list[3:]}
        future_content_one = executor.submit(generate_content_from_textbook,title ,submodules_split_one,description,VECTORDB_TEXTBOOK,'first')
        future_content_two = executor.submit(generate_content_from_textbook,title ,submodules_split_two,description,VECTORDB_TEXTBOOK,'second')

    # Retrieve the results when both functions are done
    content_one = future_content_one.result()
    content_two = future_content_two.result()

    content = content_one + content_two
    images_list = future_images_list.result()
    video_list = future_video_list.result()

    # new_module.submodule_content = content
    # new_module.image_urls = images_list
    # new_module.video_urls = video_list
    # db.session.commit()

    # add module to ongoing modules for user
    # ongoing_module = PersonalizedOngoingModule(user_id=user.user_id, module_id=new_module.module_id)
    # db.session.add(ongoing_module)
    # db.session.commit()
    # translate submodule content to the source language
    trans_submodule_content = translate_submodule_content(content, source_language)
    print(f"Translated submodule content: {trans_submodule_content}")
    
    return jsonify({"message": "Query successful", "images": images_list,"videos": video_list, "content": trans_submodule_content, "response": True}), 200

# query route --> if websearch is true then fetch from web and feed into model else directly feed into model
# save frequently searched queries in database for faster retrieval
@users.route('/query2/<string:topicname>/<string:level>/<string:websearch>/<string:source_lang>', methods=['GET'])
@cross_origin(supports_credentials=True)
def query_topic(topicname,level,websearch,source_lang):
    # check if user is logged in
    user_id = session.get('user_id')
    print(session.get('user_id'))
    if user_id is None:
        return jsonify({"message": "User not logged in", "response":False}), 401
    
    # check if user exists
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"message": "User not found", "response":False}), 404

    # language detection for input provided
    if source_lang == 'auto':
        source_language = Lang(str(detector.detect_language_of(topicname)).split('.')[1].title()).pt1
        print(f"Source Language: {source_language}")
    else:
        source_language=source_lang
        print(f"Source Language: {source_language}")

    trans_topic_name = ""
    # translate other languages input to english
    if source_lang!="en":
        trans_topic_name = GoogleTranslator(source=source_lang, target='en').translate(topicname)
        print(f"Translated topic name: {trans_topic_name}")
    else:
        trans_topic_name = topicname
# check if topic exists in database along with its modulenames and summaries
    topic = Topic.query.filter_by(topic_name=trans_topic_name.lower()).first()
    if topic is None:
            topic = Topic(topic_name=trans_topic_name.lower())
            db.session.add(topic)
            db.session.commit()
            print(f"topic added to database: {topic}")
    else:
        modules = Module.query.filter_by(topic_id=topic.topic_id, websearch=websearch, level=level).all()
        if modules:
            module_ids = {module.module_name:module.module_id for module in modules}
            module_summary_content = {module.module_name:module.summary for module in modules}
            trans_module_summary_content = translate_module_summary(module_summary_content, source_language)
            print(f"Translated module summary content: {trans_module_summary_content}")
            trans_moduleids = {}
            if source_language !='en':
                for key, value in module_ids.items():
                    trans_key = GoogleTranslator(source='en', target=source_language).translate(str(key))
                    trans_moduleids[trans_key]=value
                module_ids=trans_moduleids
            return jsonify({"message": "Query successful", "topic_id":topic.topic_id, "topic":trans_topic_name, "source_language":source_language, "module_ids":module_ids, "content": trans_module_summary_content, "response":True}), 200


    if(websearch=="true"):
        print("web search ture:-")
        module_summary_content = generate_module_summary_from_web(topic=trans_topic_name,level=level)
    else:    
        print("web search false:-")
        module_summary_content = generate_module_summary(topic=trans_topic_name,level=level)    
    
    module_ids = {}
    for modulename, modulesummary in module_summary_content.items():
        new_module = Module(
            module_name=modulename,
            topic_id=topic.topic_id,
            websearch=websearch,
            level=level,
            summary=modulesummary
        )
        db.session.add(new_module)
        db.session.commit()
        module_ids[modulename] = new_module.module_id

    # add user query to database
    new_user_query = Query(user_id=user.user_id, topic_id=topic.topic_id, level=level, websearch=websearch, lang=source_language)
    db.session.add(new_user_query)
    db.session.commit()

    trans_moduleids = {}
    if source_language !='en':
        for key, value in module_ids.items():
            trans_key = GoogleTranslator(source='en', target=source_language).translate(str(key))
            trans_moduleids[trans_key]=value
        module_ids=trans_moduleids
    # translate module summary content to source language
    trans_module_summary_content = translate_module_summary(module_summary_content, source_language)
    print(f"Translated module summary content: {trans_module_summary_content}")

    return jsonify({"message": "Query successful", "topic_id":topic.topic_id, "topic":trans_topic_name, "source_language":source_language, "module_ids":module_ids, "content": trans_module_summary_content, "response":True}), 200

#course overview route
@users.route('/query2/course-overview/<int:module_id>/<string:source_language>/<string:websearch>', methods=['GET'])
@cross_origin(supports_credentials=True)
def course_overview(module_id, source_language, websearch):
    # check if user is logged in
    user_id = session.get("user_id", None)
    if user_id is None:
        return jsonify({"message": "User not logged in", "response": False}), 401
    
    # check if user exists
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"message": "User not found", "response": False}), 404
    session["module_id"] = module_id
    
    # check if submodules are saved in the database for the given module_id
    module = Module.query.get(module_id)
    other_modules = Module.query.filter(Module.topic_id == module.topic_id,Module.level==module.level,Module.websearch==module.websearch, Module.module_id != module_id).all()
    modules_dict_list = [module.to_dict() for module in other_modules]
    module_info = {}
    module_info['module_name']=module.module_name
    module_info['summary']=module.summary
    module_info['level']=module.level

    if module.submodule_content is not None:
        print("language",source_language)
        trans_submodule_content = translate_submodule_content(module.submodule_content, source_language)
        print(f"Translated submodule content: {trans_submodule_content}")
        return jsonify({"message": "Query successful","other_modules":modules_dict_list,"module": module_info ,"images": module.image_urls,"videos": module.video_urls, "content": trans_submodule_content, "response": True}), 200
    
    # images = module_image_from_web(module.module_name)
    # if submodules are not generated, generate and save them in the database
    with ThreadPoolExecutor() as executor:
        if websearch == "true":
            submodules = generate_submodules_from_web(module.module_name,module.summary)
            print(submodules)
            keys_list = list(submodules.keys())
            future_images_list = executor.submit(module_image_from_web, submodules)
            future_video_list = executor.submit(module_videos_from_web, submodules)
            submodules_split_one = {key: submodules[key] for key in keys_list[:3]}
            submodules_split_two = {key: submodules[key] for key in keys_list[3:]}
            future_content_one = executor.submit(generate_content_from_web, submodules_split_one, module.module_name, 'first')
            future_content_two = executor.submit(generate_content_from_web, submodules_split_two, module.module_name, 'second')

        else:
            submodules = generate_submodules(module.module_name)
            print(submodules)
            keys_list = list(submodules.keys())
            future_images_list = executor.submit(module_image_from_web, submodules)
            future_video_list = executor.submit(module_videos_from_web, submodules)
            submodules_split_one = {key: submodules[key] for key in keys_list[:3]}
            submodules_split_two = {key: submodules[key] for key in keys_list[3:]}
            future_content_one = executor.submit(generate_content, submodules_split_one, module.module_name,'first')
            future_content_two = executor.submit(generate_content, submodules_split_two, module.module_name,'second')

    # Retrieve the results when both functions are done
    content_one = future_content_one.result()
    content_two = future_content_two.result()

    content = content_one + content_two
    images_list = future_images_list.result()
    video_list = future_video_list.result()

    module.submodule_content = content
    module.image_urls = images_list
    module.video_urls = video_list
    db.session.commit()

    # add module to ongoing modules for user
    ongoing_module = OngoingModule(user_id=user.user_id, module_id=module_id, level=module.level)
    db.session.add(ongoing_module)
    db.session.commit()

    # translate submodule content to the source language
    trans_submodule_content = translate_submodule_content(content, source_language)
    print(f"Translated submodule content: {trans_submodule_content}")
    
    return jsonify({"message": "Query successful","other_modules": modules_dict_list,"module": module_info ,"images": module.image_urls,"videos": module.video_urls ,"content": trans_submodule_content,"sub_modules": submodules, "response": True}), 200


# module query --> generate mutlimodal content (with images) for submodules in a module

@users.route('/query2/<int:module_id>/<string:source_language>/<string:websearch>', methods=['GET'])
@cross_origin(supports_credentials=True)
def query_module(module_id, source_language, websearch):
    # check if user is logged in
    user_id = session.get("user_id", None)
    if user_id is None:
        return jsonify({"message": "User not logged in", "response": False}), 401
    
    # check if user exists
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"message": "User not found", "response": False}), 404
    session["module_id"] = module_id
    
    # check if submodules are saved in the database for the given module_id
    module = Module.query.get(module_id)
    ongoing_module = OngoingModule.query.filter(OngoingModule.user_id==user.user_id, OngoingModule.module_id==module_id)
    if not ongoing_module:
        ongoing_modules = OngoingModule(user_id=user.user_id, module_id=module_id, level=module.level)
        db.session.add(ongoing_modules)
        db.session.commit()
    if module.submodule_content is not None:
        trans_submodule_content = translate_submodule_content(module.submodule_content, source_language)
        print(f"Translated submodule content: {trans_submodule_content}")
    return jsonify({"message": "Query successful", "images": module.image_urls,"videos": module.video_urls, "content": trans_submodule_content, "response": True}), 200
    

# download route --> generate pdf for module summary and module content
# currently generate pdf for latin and devanagari scripts 
@users.route('/query2/test', methods=['GET'])
def test():
    ongoing_module = OngoingModule(user_id=2, module_id=78, level='beginner')
    db.session.add(ongoing_module)
    db.session.commit()
    return jsonify({"message": "Query successful"})

@users.route('/query2/<int:module_id>/<string:source_language>/download', methods=['GET'])
def download_pdf(module_id, source_language):
    # get module from database
    module = Module.query.get(module_id)
    modulename = module.module_name
    clean_modulename = modulename.replace(':',"_") 
    module_summary = module.summary
    submodule_content = module.submodule_content

    # translate module summary and submodule content to source language
    trans_modulename = GoogleTranslator(source='en', target=source_language).translate(modulename)
    trans_module_summary = GoogleTranslator(source='en', target=source_language).translate(module_summary)
    trans_submodule_content = translate_submodule_content(submodule_content, source_language)

    # Create a PDF file
    download_dir = os.path.join(os.getcwd(), "downloads")
    os.makedirs(download_dir, exist_ok=True)
    pdf_file_path = os.path.join(download_dir, f"{clean_modulename}_summary.pdf")

    # Call the generate_pdf function with the custom_styles argument
    generate_pdf(pdf_file_path, trans_modulename, trans_module_summary, trans_submodule_content, source_language, module.video_urls)

    # Send the PDF file as an attachment
    return send_file(pdf_file_path, as_attachment=True)

#function of text to speech
def text_to_speech(text, language='en', directory='audio_files'):
    if not os.path.exists(directory):
        os.makedirs(directory)
    # Create a gTTS object
    speech = gTTS(text=text, lang=language, slow=False)
    # Specify the file path including the directory to save the MP3 file
    file_path = os.path.join(directory, 'text.mp3')
    # Save the speech to the specified file path
    speech.save(file_path)
    return file_path


@users.route('/generate-audio', methods=['POST'])
@cross_origin(supports_credentials=True)
def generate_audio():
    data = request.json
    content = data.get('content')
    language = data.get('language') 
    subject_title = data.get('subject_title') 
    subject_content = data.get('subject_content') 

    # check if user is logged in
    user_id = session.get("user_id", None)
    if user_id is None:
        return jsonify({"message": "User not logged in", "response":False}), 401
    
    # check if user exists
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"message": "User not found", "response":False}), 404
    
    full_text = ""
    full_text += f"{subject_title}. {subject_content}. "
    # Combine titles and contents to form full text
    for item in content:
        full_text += f"{item['title']}. {item['content']}. "
    # Create a gTTS object with the combined text
    tts = gTTS(text=full_text, lang=language, slow=False)
    # Create an in-memory file-like object to store the audio data
    audio_file = BytesIO()
    # Save the audio into the in-memory file-like object
    tts.write_to_fp(audio_file)
    audio_file.seek(0)
    # file_path=text_to_speech(trans_output, language=source_lang, directory='audio_files')
    return send_file(audio_file, mimetype='audio/mp3', as_attachment=True, download_name='generated_audio.mp3')



@users.route('/quiz/<int:module_id>/<string:source_language>/<string:websearch>', methods=['GET'])
@cross_origin(supports_credentials=True)
def gen_quiz(module_id, source_language, websearch):
    user_id = session.get("user_id", None)
    if user_id is None:
        return jsonify({"message": "User not logged in", "response":False}), 401
    
    # check if user exists
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"message": "User not found", "response":False}), 404
    
    module = Module.query.get(module_id)
    sub_module_names = [submodule['title_for_the_content'] for submodule in module.submodule_content]
    print("Submodules:-----------------------",sub_module_names)

    if websearch=="true":
        print("WEB SEARCH OP quiz1--------------------------")
        quiz = generate_quiz_from_web(sub_module_names)
    else:
        quiz = generate_quiz(sub_module_names)
    translated_quiz = translate_quiz(quiz["quizData"], source_language)
    return jsonify({"message": "Query successful", "quiz": translated_quiz, "response": True}), 200

@users.route('/quiz2/<int:module_id>/<string:source_language>/<string:websearch>', methods=['GET'])
@cross_origin(supports_credentials=True)
def gen_quiz2(module_id, source_language, websearch):
    user_id = session.get("user_id", None)
    if user_id is None:
        return jsonify({"message": "User not logged in", "response":False}), 401
    
    # check if user exists
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"message": "User not found", "response":False}), 404
    
    module = Module.query.get(module_id)

    # check if user has completed quiz1 or not
    # completed_module = CompletedModule.query.filter_by(user_id=user_id, module_id=module_id, level=module.level).first()
    # if completed_module.theory_quiz_score is None:
    #     return jsonify({"message": "User has not completed quiz1", "response":False}), 404
    
    sub_module_names = [submodule['title_for_the_content'] for submodule in module.submodule_content]
    print("Submodules:-----------------------",sub_module_names)
    if websearch=="true":
        print("WEB SEARCH OP quiz2--------------------------")
        quiz = generate_applied_quiz_from_web(sub_module_names)
    else:
        quiz = generate_applied_quiz(sub_module_names)

    translated_quiz = translate_quiz(quiz["quizData"], source_language)
    print("quiz---------------",quiz)
    return jsonify({"message": "Query successful", "quiz": translated_quiz, "response": True}), 200

@users.route('/quiz3/<int:module_id>/<string:source_language>/<string:websearch>', methods=['GET'])
@cross_origin(supports_credentials=True)
def gen_quiz3(module_id, source_language, websearch):
    user_id = session.get("user_id", None)
    if user_id is None:
        return jsonify({"message": "User not logged in", "response":False}), 401
    
    # check if user exists
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"message": "User not found", "response":False}), 404
    
    module = Module.query.get(module_id)

    # check if user has completed quiz1 or not
    # completed_module = CompletedModule.query.filter_by(user_id=user_id, module_id=module_id, level=module.level).first()
    # if completed_module.theory_quiz_score is None:
    #     return jsonify({"message": "User has not completed quiz1", "response":False}), 404
    
    sub_module_names = [submodule['subject_name'] for submodule in module.submodule_content]
    print("Submodules:-----------------------",sub_module_names)
    if websearch=="true":
        print("WEB SEARCH OP quiz2=3--------------------------")
        quiz = generate_conversation_quiz_from_web(sub_module_names)
    else:
        quiz = generate_conversation_quiz(sub_module_names)

    translated_questions = translate_assignment(quiz, source_language)
    print("quiz---------------",quiz)
    return jsonify({"message": "Query successful", "quiz": translated_questions, "response": True}), 200


@users.route('/add_theory_score/<int:score>')
@cross_origin(supports_credentials=True)
def add_theory_score(score):
    user_id = session.get("user_id", None)
    if user_id is None:
        return jsonify({"message": "User not logged in", "response":False}), 401
    
    # check if user exists
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"message": "User not found", "response":False}), 404
    module_id = session.get("module_id", None)
    module = Module.query.get(module_id)
    completed_module = CompletedModule(user_id=user_id, module_id=module_id, level=module.level, theory_quiz_score=score)
    db.session.add(completed_module)
    db.session.commit()
    return jsonify({"message": "Score added successfully", "response": True}), 200

@users.route('/add_application_score/<int:score>')
@cross_origin(supports_credentials=True)
def add_application_score(score):
    user_id = session.get("user_id", None)
    if user_id is None:
        return jsonify({"message": "User not logged in", "response":False}), 401
    
    # check if user exists
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"message": "User not found", "response":False}), 404
    module_id = session.get("module_id", None)
    module = Module.query.get(module_id)
    completed_module = CompletedModule.query.filter_by(user_id=user_id, module_id=module_id, level=module.level).first()
    completed_module.application_quiz_score = score
    db.session.commit()
    return jsonify({"message": "Score added successfully", "response": True}), 200

@users.route('/add_assignment_score',methods=['POST'])
@cross_origin(supports_credentials=True)
def add_assignment_score():
    user_id = session.get("user_id", None)
    if user_id is None:
        return jsonify({"message": "User not logged in", "response":False}), 401
    
    # check if user exists
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"message": "User not found", "response":False}), 404

    request_data = request.get_json()
    module_id = session.get("module_id", None)
    score = request_data.get('evaluationResponse')
    module = Module.query.get(module_id)
    completed_module = CompletedModule.query.filter_by(user_id=user_id, module_id=module_id, level=module.level).first()
    completed_module.assignment_score = score
    db.session.commit()

    ongoing_module = OngoingModule.query.filter_by(user_id=user_id, module_id=module_id).first()
    if ongoing_module:
        db.session.delete(ongoing_module)
        db.session.commit()

    return jsonify({"message": "Score added successfully", "response": True}), 200

###ASSISTANT API SECTION#######################
def wait_on_run(run_id, thread_id):
    client = OpenAI(api_key=openai_api_key1)
    while True:
        run = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run_id,
        )
        print('RUN STATUS', run.status)
        time.sleep(0.5)
        if run.status in ['failed', 'completed', 'requires_action']:
            return run


client = OpenAI(api_key = openai_api_key1)

def submit_tool_outputs(thread_id, run_id, tools_to_call):
    tools_outputs = []
    for tool in tools_to_call:
        output = None
        tool_call_id = tool.id
        tool_name = tool.function.name
        tool_args = tool.function.arguments
        print('TOOL CALLED:', tool_name)
        print('ARGUMENTS:', tool_args)
        tool_to_use = available_tools.get(tool_name)
        if tool_name =='retrieval_augmented_generation':
            tool_args_dict = ast.literal_eval(tool_args)
            query = tool_args_dict['query']
            output = tool_to_use(query)
        elif tool_name == 'get_context_from_page':
            index = session.get('index_chatbot')
            output = tool_to_use(index)
        if output:
            tools_outputs.append(
                {'tool_call_id': tool_call_id, 'output': output})

    return client.beta.threads.runs.submit_tool_outputs(thread_id=thread_id, run_id=run_id, tool_outputs=tools_outputs)


def retrieval_augmented_generation(query, vectordb=VECTORDB):
    relevant_docs = vectordb.similarity_search(query)
    rel_docs = [doc.page_content for doc in relevant_docs]
    output = '\n'.join(rel_docs)
    print(output)
    return output

def get_page_context(index=1):
    module_id = session.get("module_id", None)
    module = Module.query.get(module_id)
    data = module.submodule_content[index]
    all_text = (
    f"{data['subject_name']}\n"
    f"{data['title_for_the_content']}\n"
    f"{data['content']}\n"
    )

    for subsection in data['subsections']:
        all_text += f"{subsection['title']}\n{subsection['content']}\n"
    print("submodule_content------------------------",all_text)
    return all_text

available_tools = {
    'retrieval_augmented_generation': retrieval_augmented_generation,
    'get_context_from_page': get_page_context
}

@users.route('/chatbot-route', methods=['POST'])
@cross_origin(supports_credentials=True)
def chatbot_route():
    data = request.get_json()
    print(data)
    tool_check = []
    query = data.get('userdata', '')
    if data.get('index_no', ''):
        index = int(data.get('index_no', ''))
        session['index_chatbot'] = index

    if query:
        source_language = Lang(str(detector.detect_language_of(query)).split('.')[1].title()).pt1
        if source_language != 'en':
            trans_query = GoogleTranslator(source=source_language, target='en').translate(query)
        else:
            trans_query = query
        assistant_id = session['assistant_id']
        print('ASSISTANT ID', assistant_id)
        thread_id = session['thread_id']
        print('THREAD ID', thread_id)
        print(trans_query)
        message = client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content= trans_query,
        )
        run = client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=session['assistant_id'],
        )
        run = wait_on_run(run.id, thread_id)

        if run.status == 'failed':
            print(run.error)
        elif run.status == 'requires_action':
            run = submit_tool_outputs(thread_id, run.id, run.required_action.submit_tool_outputs.tool_calls)
            run = wait_on_run(run.id,thread_id)
        messages = client.beta.threads.messages.list(thread_id=thread_id,order="asc")
        print('message',messages)
        content = None
        for thread_message in messages.data:
            content = thread_message.content
        print("Content List", content)
        if len(tool_check) == 0:
            chatbot_reply = content[0].text.value
            print("Chatbot reply",chatbot_reply)
            if source_language != 'en':
                trans_output = GoogleTranslator(source='auto', target=source_language).translate(chatbot_reply)
            else:
                trans_output = chatbot_reply
            response = {'chatbotResponse': trans_output,'function_name': 'normal_search'}
        return jsonify(response)
    else:
        return jsonify({'error': 'User message not provided'}), 400
##############################################################################
    
##################whisper######################################
@users.route('/query2/voice-save', methods=['POST'])
@cross_origin(supports_credentials=True)
def save_voices():
    try:
        user_id = session.get("user_id", None)
        module_id = session.get("module_id", None)
        if user_id is None:
            return jsonify({"message": "User not logged in", "response": False}), 401

        # check if user exists
        user = User.query.get(user_id)
        if user is None:
            return jsonify({"message": "User not found", "response": False}), 404
        print("Module id:-----------", module_id)

        # Create a folder to store the voice recordings if it doesn't exist
        base_folder = os.path.join('voice_recordings', str(user_id), str(module_id))
        os.makedirs(base_folder, exist_ok=True)

        # Check if the post request has the file part
        if 'voice' not in request.files:
            return jsonify({"message": "No file part in the request", "response": False}), 400

        # Get the voice file
        voice = request.files['voice']

        # Save the voice recording as a WAV file
        filename = f'voice_{datetime.now().strftime("%Y%m%d%H%M%S")}.wav'
        file_path = os.path.join(base_folder, secure_filename(filename))
        voice.save(file_path)

        return jsonify({'message': 'Voice saved successfully', 'response': True}), 200
    except Exception as e:
        return jsonify({'error': str(e), 'response': False}), 500

###############################################################
    
####################quiz 3 evaluation##############################
@users.route('/evaluate_quiz/<string:source_language>', methods=['POST'])
@cross_origin(supports_credentials=True)
def evaluate_quiz(source_language):
    try:
        user_id = session.get("user_id", None)
        module_id = session.get("module_id", None)
        if user_id is None:
            return jsonify({"message": "User not logged in", "response": False}), 401
        # check if user exists
        user = User.query.get(user_id)
        if user is None:
            return jsonify({"message": "User not found", "response": False}), 404
        # Get the responses from the request data
        responses = request.json.get('responses')
        print("responses",responses)
        translated_responses_output =  translate_responses(responses,source_language)
        # Perform evaluation logic (replace this with your actual evaluation logic)
        evaluation_result = evaluate_conversation_quiz(translated_responses_output)
        translate_evaluation_result = translate_evaluations(evaluation_result,source_language)
        # evaluation_result = {
        #     "accuracy": 7,
        #     "completeness": 6,
        #     "clarity": 8,
        #     "relevance": 9,
        #     "understanding": 8,
        #     "feedback": "Overall, your answers demonstrate a good understanding of machine learning concepts and their applications. However, there are some areas for improvement. In the first question, the answer lacks specific examples of real-world scenarios where machine learning is applied. For the second question, while the explanation of supervised and unsupervised learning is accurate, examples of each are missing. The answer to the third question is accurate, but could benefit from more detailed explanation and specific examples. The answer to the fourth question is comprehensive and relevant. In the fifth question, the answer could be improved by providing more examples and elaborating further on the impact of feature selection and engineering on model performance. Overall, your responses are clear and well-organized, but adding specific examples and more detailed explanations would further enhance the completeness and understanding of your answers."
        # }
        # Return the evaluation result
        return jsonify(translate_evaluation_result), 200
    except Exception as e:
        print(f"Error during evaluation: {str(e)}")
        return jsonify({"error": "An error occurred during evaluation"}), 500
###################################################################
    
@users.route('/delete-info', methods=['GET'])
@cross_origin(supports_credentials=True)
def delete_info():
    module_id = session.get("module_id", None)
    user_id = session.get("user_id", None)
    ongoing_module = OngoingModule.query.filter_by(user_id=user_id, module_id=module_id).first()
    if ongoing_module:
        db.session.delete(ongoing_module)
        db.session.commit()
    module = Module.query.filter_by(module_id=module_id).first()
    if module:
        db.session.delete(module)
        db.session.commit()
    return jsonify({"message": "An error occurred during evaluation"}), 200
