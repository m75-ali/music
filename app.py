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
# Function to calculate the music genre
def calculate_genre(answers):
    # Detailed mapping of answers to genres
    genre_mapping = {
        'Dancing': 'EDM', 'Synthesizer': 'EDM', 'Night': 'EDM', 'Partying': 'EDM',
        'Reading': 'Jazz', 'Piano': 'Jazz', 'Morning': 'Jazz', 'Relaxing': 'Jazz',
        'Traveling': 'Rock', 'Guitar': 'Rock', 'Evening': 'Rock', 'Exploring': 'Rock',
        'Gaming': 'Pop', 'Drums': 'Pop', 'Afternoon': 'Pop', 'Socializing': 'Pop',
        'Street Culture': 'Hip-Hop', 'Rap': 'Hip-Hop', 'Beats': 'Hip-Hop', 'Urban': 'Hip-Hop',
        'Orchestra': 'Classical', 'Violin': 'Classical', 'Symphony': 'Classical', 'Calm': 'Classical',
        'Cooking': 'Jazz', 'Photography': 'Jazz', 'Hiking': 'Rock', 'Watching Movies': 'Pop',
        'Visiting Friends': 'Pop', 'Playing Sports': 'Rock', 'Relaxing at Home': 'Jazz',
        'Shopping': 'EDM', 'Lo-fi': 'Jazz', 'Electronic': 'EDM', 'Rock': 'Rock',
        'Jazz': 'Jazz', 'Ambient': 'Classical', 'Classical': 'Classical',
        'Love it': 'Rock', 'Its okay': 'Jazz', 'Not a fan': 'Classical', 
        'Never been': 'Classical', 'Prefer small gigs': 'Jazz', 'Enjoy virtual concerts': 'EDM'
    }

    genre_scores = {genre: 0 for genre in set(genre_mapping.values())}
    
    # Calculate scores based on answers
    for answer_list in answers.values():
        for answer in answer_list:
            if answer in genre_mapping:
                genre_scores[genre_mapping[answer]] += 1

    # Debugging output to monitor the scores
    print("Genre Scores:", genre_scores)

    # Determine the genre with the maximum score
    highest_score_genre = max(genre_scores, key=genre_scores.get)
    return highest_score_genre

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
