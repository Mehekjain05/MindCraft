from server import create_app
from server.models import User, Topic, Module, Query, CompletedModule, CompletedTopics, OngoingModule
# from server.users.utils import generate_module_summary, generate_submodules
# from faker import Faker
# from random import randint, sample
# import openai
# from openai import OpenAI
# import time
# from pprint import pprint
import csv
# from sqlalchemy import desc

# fake = Faker()
app = create_app()

# List of interests
# interests = ["Machine Learning", "Deep Learning", "Natural Language Processing", "Computer Vision", "Reinforcement Learning",
#              "Data Science", "Neural Networks", "AI Ethics", "TensorFlow", "PyTorch", "Supervised Learning",
#              "Unsupervised Learning", "Recommender Systems", "Data Preprocessing", "Time Series Analysis",
#              "Ensemble Learning", "Regression Analysis", "Classification", "Clustering", "Autoencoders", "Automobiles", "Computer Vision", "Artificial Intelligence"]

# # Convert the list of interests to HTML options
# html_options = ""
# for interest in interests:
#     html_options += f'<option value="{interest}">{interest}</option>\n'

# # Print or use the generated HTML options
# print(html_options)


with app.app_context():
#     from server import db, bcrypt
#     db.create_all()

#     # Add users to database
#     for _ in range(20):
#         fname = fake.first_name()
#         lname = fake.last_name()
#         user_name = fname + "_" + lname
#         hashed_password = bcrypt.generate_password_hash(fname+"pass").decode('utf-8')


#         new_user = User(
#             fname=fname,
#             lname=lname,
#             user_name=user_name,
#             email=user_name + "@gmail.com",
#             password=hashed_password,
#             country=fake.country(),
#             state=fake.state(),
#             city=fake.city(),
#             gender=fake.random_element(elements=('Male', 'Female', 'Other')),
#             age=fake.random_int(min=18, max=60),
#             interests=", ".join(sample(interests, randint(1, 3))),
#             date_joined=fake.date_time_this_decade()
#         )

#         db.session.add(new_user)
# #     # # Commit the changes to the database
#     db.session.commit()

    # Add topic and its modules to datbase
    # topic = 'machine learning'
    # new_topic = Topic(topic_name=topic)
    # db.session.add(new_topic)
    # db.session.commit()


    # start = time.time()

    # # generate modules and their summaries for beginner level
    # beg_module_content = generate_module_summary(topic, 'beginner')
    # print(f"Time take to generate modules and their summaries for beginner level: {time.time() - start}")

    # # generate submodules and their content
    # for modulename, modulesummary in beg_module_content.items():
    #     sub_module_names = generate_submodules(modulename)
    #     print(f"Time take to generate submodules for {modulename} for beginner level: {time.time() - start}")

    #     sub_module_content = generate_content(sub_module_names)
    #     print(f"Time take to generate content for {modulename} for beginner level: {time.time() - start}")
    #     print(type(sub_module_content))

    #     new_module = Module(
    #         module_name=modulename,
    #         topic_id=new_topic.topic_id,
    #         level='beginner',
    #         summary=beg_module_content[modulename],
    #         submodule_content=sub_module_content
    #     )
    #     db.session.add(new_module)
    #     db.session.commit()

#     # start = time.time()

#     # # generate modules and their summaries for advanced level
#     # adv_module_content = generate_module_summary(topic, 'advanced')
#     # print(f"Time take to generate modules and their summaries for advanced level: {time.time() - start}")

#     # # generate submodules and their content
#     # for modulename, modulesummary in adv_module_content.items():
#     #     sub_module_content = generate_submodules(modulename)
#     #     print(f"Time take to generate submodules for {modulename} for advanced level: {time.time() - start}")

#     #     sub_module_content = generate_content(sub_module_content)
#     #     print(f"Time take to generate content for {modulename} for advanced level: {time.time() - start}")

#     #     new_module = Module(
#     #         module_name=modulename,
#     #         topic_id=new_topic.topic_id,
#     #         level='advanced',
#     #         summary=modulesummary,
#     #         submodule_content=sub_module_content
#     #     )
#     #     db.session.add(new_module)
#     #     db.session.commit()

#     # Task 1: Add data to the Query table for all users querying 1-3 topics
#     # all_users = User.query.all()
#     # all_topics = Topic.query.all()

#     # for user in all_users:
#     #     # Choose 1 to 3 random topics for each user
#     #     queried_topics = sample(all_topics, k=sample(range(1, 4), 1)[0])

#     #     for topic in queried_topics:
#     #         new_query = Query(user_id=user.user_id, topic_id=topic.topic_id, date_search=fake.date_time_this_decade(), lang='en')  # Assuming "en" as the language
#     #         db.session.add(new_query)

#     # db.session.commit()

#     # Task 2: Add data to CompletedModule for 10 random users completing 1-5 modules
#     # random_users = sample(all_users, k=15)
#     # all_modules = Module.query.all()

#     # for user in random_users:
#     #     # Choose 1 to 5 random modules for each user
#     #     completed_modules = sample(all_modules, k=sample(range(1, 6), 1)[0])

#     #     for module in completed_modules:
#     #         level = module.level  # You can adjust the level as needed
#     #         date_completed = fake.date_time_this_decade()
#     #         quiz_score = 80  # You can set an appropriate quiz score

#     #         new_completed_module = CompletedModule(
#     #             user=user,
#     #             module=module,
#     #             level=level,
#     #             date_completed=date_completed,
#     #             quiz_score=quiz_score,
#     #         )
#     #         db.session.add(new_completed_module)

#     # db.session.commit()

    # convert data in database to csv files

    # Assuming you have an instance of Flask app and SQLAlchemy db initialized

    # Extract data from the database
    # all_users = User.query.all()
    all_queries = Query.query.all()
    all_modules = Module.query.all()
    # all_topics = Topic.query.all()
    # # all_completed_modules = CompletedModule.query.all()

    # # Define file paths for CSV files
    # users_csv_path = "csv_data_files/users.csv"
    queries_csv_path = "server/recommender_system/queries.csv"
    modules_csv_path = "server/recommender_system/modules.csv"
    # topics_csv_path = "csv_data_files/topics.csv"
    # # completed_modules_csv_path = "csv_data_files/completed_modules.csv"

    # # Write data to CSV files
    # with open(users_csv_path, "w", newline="", encoding="utf-8") as users_csv:
    #     user_writer = csv.writer(users_csv)
    #     user_writer.writerow(["user_id", "fname", "lname", "user_name", "email", "country", "state", "city", "gender", "age", "interests", "date_joined"])
    #     for user in all_users:
    #         user_writer.writerow([user.user_id, user.fname, user.lname, user.user_name, user.email, user.country, user.state, user.city, user.gender, user.age, user.interests, user.date_joined.strftime("%d/%m/%Y %H:%M")])

    with open(queries_csv_path, "w", newline="", encoding="utf-8") as queries_csv:
        query_writer = csv.writer(queries_csv)
        query_writer.writerow(["query_id", "user_id", "topic_id", "date_search", "lang", "websearch", "level"])
        for query in all_queries:
            query_writer.writerow([query.query_id, query.user_id, query.topic_id, query.date_search.strftime("%d/%m/%Y %H:%M"), query.lang, query.websearch, query.level])

    with open(modules_csv_path, "w", newline="", encoding="utf-8") as modules_csv:
        module_writer = csv.writer(modules_csv)
        module_writer.writerow(["module_id", "module_name", "topic_id", "level", "summary"])
        for module in all_modules:
            module_writer.writerow([module.module_id, module.module_name, module.topic_id, module.level, module.summary])

    # with open(topics_csv_path, "w", newline="", encoding="utf-8") as topics_csv:
    #     topic_writer = csv.writer(topics_csv)
    #     topic_writer.writerow(["topic_id", "topic_name"])
    #     for topic in all_topics:
    #         topic_writer.writerow([topic.topic_id, topic.topic_name])

    # with open(completed_modules_csv_path, "w", newline="", encoding="utf-8") as completed_modules_csv:
    #     completed_module_writer = csv.writer(completed_modules_csv)
    #     completed_module_writer.writerow(["cmid", "user_id", "module_id", "level", "date_completed", "quiz_score"])
    #     for completed_module in all_completed_modules:
    #         completed_module_writer.writerow([completed_module.cmid, completed_module.user_id, completed_module.module_id, completed_module.level, completed_module.date_completed.strftime("%d/%m/%Y %H:%M"), completed_module.quiz_score])

#     # user1 = User.query.filter_by(user_id=1).first()
#     # print(user1)


#     # # map topic ids to date searched in user queries
#     # query_topic_date = {}
#     # for query in user1.user_query_association:
#     #     query_topic_date[query.topic_id] = query.date_search.strftime("%d/%m/%Y %H:%M")

#     # print(query_topic_date)

#     # latest_query = Query.query.filter_by(user_id=1).order_by(desc(Query.date_search)).first()
#     # print(latest_query)

# from gtts import gTTS
# tts_en = gTTS('hello this is in english', lang='en')
# tts_fr = gTTS('bonjour c\'est en français', lang='fr')
# tts_mr = gTTS('नमस्कार हे मराठीत आहे', lang='mr')
# tts_hi = gTTS('नमस्कार ये हिंदी में है', lang='hi')

# with open('hello_bonjour.mp3', 'wb') as f:
#     tts_en.write_to_fp(f)
#     tts_fr.write_to_fp(f)
#     tts_mr.write_to_fp(f)
#     tts_hi.write_to_fp(f)

# from lingua import LanguageDetectorBuilder
# from iso639 import Lang

# # detect kannada text
# # Detector for language detection
# detector = LanguageDetectorBuilder.from_all_languages().with_preloaded_language_models().build()
# print(detector.detect_language_of("ಇದು ವಿಭಿನ್ನವಾಗಿದೆ"), type(detector.detect_language_of("ಇದು ವಿಭಿನ್ನವಾಗಿದೆ")), sep='\n')
# source_language = Lang(str(detector.detect_language_of("ಇದು ವಿಭಿನ್ನವಾಗಿದೆ")).split('.')[1].title()).pt1

