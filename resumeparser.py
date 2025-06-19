# import libraries
import openai  
import yaml
import os
from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def ats_extractor(resume_data):
    prompt = '''
    You are an AI bot designed to act as a professional for parsing resumes. You are given with resume and your job is to extract the following information from the resume:
    
    1. employment details    
    2. projects [name,description]
    3. Education [degree,major]
    5. Certifications
    6. Name, Email, Mobile, Address, linkedin 
    7. Resume Summary
    
    Give the extracted information in json format only
    '''

    messages = [ 
        {"role": "system", "content": prompt},
        {"role": "user", "content": resume_data}
    ]
    
    #user_content = resume_data
    
    #messages.append({"role": "user", "content": user_content})

    response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.0,
                max_tokens=1500)
        
    data = response.choices[0].message.content

    #print(data)
    return data