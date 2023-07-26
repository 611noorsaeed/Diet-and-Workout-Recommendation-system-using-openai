from flask import Flask, render_template, request
import os
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains import LLMChain
import re

import os
import re
os.environ['OPENAI_API_KEY'] = 'your key is here' # your openai key





app = Flask(__name__)

llm_resto = OpenAI(temperature=0.6)
prompt_template_resto = PromptTemplate(
    input_variables=['age', 'gender', 'weight', 'height', 'veg_or_nonveg', 'disease', 'region', 'allergics', 'foodtype'],
    template="Diet Recommendation System:\n"
             "I want you to recommend 6 restaurants names, 6 breakfast names, 5 dinner names, and 6 workout names, "
             "based on the following criteria:\n"
             "Person age: {age}\n"
             "Person gender: {gender}\n"
             "Person weight: {weight}\n"
             "Person height: {height}\n"
             "Person veg_or_nonveg: {veg_or_nonveg}\n"
             "Person generic disease: {disease}\n"
             "Person region: {region}\n"
             "Person allergics: {allergics}\n"
             "Person foodtype: {foodtype}."
)



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/recommend', methods=['POST'])
def recommend():
    if request.method == "POST":
        age = request.form['age']
        gender = request.form['gender']
        weight = request.form['weight']
        height = request.form['height']
        veg_or_noveg = request.form['veg_or_nonveg']
        disease = request.form['disease']
        region = request.form['region']
        allergics = request.form['allergics']
        foodtype = request.form['foodtype']

        chain_resto = LLMChain(llm=llm_resto, prompt=prompt_template_resto)
        input_data = {'age': age,
                              'gender': gender,
                              'weight': weight,
                              'height': height,
                              'veg_or_nonveg': veg_or_noveg,
                              'disease': disease,
                              'region': region,
                              'allergics': allergics,
                              'foodtype': foodtype}
        results = chain_resto.run(input_data)

        # Extracting the different recommendations using regular expressions
        restaurant_names = re.findall(r'Restaurants:(.*?)Breakfast:', results, re.DOTALL)
        breakfast_names = re.findall(r'Breakfast:(.*?)Dinner:', results, re.DOTALL)
        dinner_names = re.findall(r'Dinner:(.*?)Workouts:', results, re.DOTALL)
        workout_names = re.findall(r'Workouts:(.*?)$', results, re.DOTALL)

        # Cleaning up the extracted lists
        restaurant_names = [name.strip() for name in restaurant_names[0].strip().split('\n') if name.strip()]
        breakfast_names = [name.strip() for name in breakfast_names[0].strip().split('\n') if name.strip()]
        dinner_names = [name.strip() for name in dinner_names[0].strip().split('\n') if name.strip()]
        workout_names = [name.strip() for name in workout_names[0].strip().split('\n') if name.strip()]

        return render_template('result.html', restaurant_names=restaurant_names,breakfast_names=breakfast_names,dinner_names=dinner_names,workout_names=workout_names)
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
