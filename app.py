from flask import Flask, render_template, request, redirect, url_for, session
import json
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a real secret key for production

# Load questions from JSON file
def load_questions():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(base_dir, 'data/questions.json')
    with open(json_path) as f:
        return json.load(f)

questions = load_questions()

# Function to calculate the music genre
def calculate_genre(answers):
    genre_scores = {'Pop': 0, 'Rock': 0, 'Jazz': 0, 'EDM': 0, 'Hip-Hop': 0, 'Classical': 0}
    
    for answer_list in answers.values():
        for answer in answer_list:
            # Expanded answers with different preferences and habits
            if answer in ['Dancing', 'Synthesizer', 'Night', 'Partying']:
                genre_scores['EDM'] += 1
            elif answer in ['Reading', 'Piano', 'Morning', 'Relaxing']:
                genre_scores['Jazz'] += 1
            elif answer in ['Traveling', 'Guitar', 'Evening', 'Exploring']:
                genre_scores['Rock'] += 1
            elif answer in ['Gaming', 'Drums', 'Afternoon', 'Socializing']:
                genre_scores['Pop'] += 1
            elif answer in ['Street Culture', 'Rap', 'Beats', 'Urban']:
                genre_scores['Hip-Hop'] += 1
            elif answer in ['Orchestra', 'Violin', 'Symphony', 'Calm']:
                genre_scores['Classical'] += 1
    
    genre = max(genre_scores, key=genre_scores.get)
    return genre

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if request.method == 'POST':
        answers = {}
        for q in questions:
            answer_list = request.form.getlist(f'question_{q["id"]}')
            answers[q["id"]] = answer_list
        genre = calculate_genre(answers)
        session['genre'] = genre  # Store genre in session
        return redirect(url_for('result'))
    return render_template('quiz.html', questions=questions)

@app.route('/result')
def result():
    genre = session.get('genre', 'Unknown')
    return render_template('result.html', genre=genre)

if __name__ == '__main__':
    app.run(debug=True)
