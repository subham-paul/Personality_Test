from flask import Flask, render_template, request, session, redirect, url_for
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change this to a random secret key

# Personality test questions
QUESTIONS = [
    {
        'id': 1,
        'question': 'In social situations, you tend to:',
        'options': [
            {'text': 'Be the center of attention', 'type': 'extrovert'},
            {'text': 'Listen more than you speak', 'type': 'introvert'},
            {'text': 'Adapt to the situation', 'type': 'ambivert'},
            {'text': 'Observe and analyze people', 'type': 'analytical'}
        ]
    },
    {
        'id': 2,
        'question': 'When making decisions, you usually:',
        'options': [
            {'text': 'Go with your gut feeling', 'type': 'intuitive'},
            {'text': 'Analyze all the facts carefully', 'type': 'analytical'},
            {'text': 'Consider how it affects others', 'type': 'feeling'},
            {'text': 'Follow logical steps', 'type': 'thinking'}
        ]
    },
    {
        'id': 3,
        'question': 'Your ideal weekend involves:',
        'options': [
            {'text': 'Going out with friends', 'type': 'extrovert'},
            {'text': 'Staying home with a good book', 'type': 'introvert'},
            {'text': 'Trying something new and adventurous', 'type': 'adventurous'},
            {'text': 'Organizing and planning', 'type': 'organized'}
        ]
    },
    {
        'id': 4,
        'question': 'When faced with a problem, you:',
        'options': [
            {'text': 'Brainstorm creative solutions', 'type': 'creative'},
            {'text': 'Follow a proven method', 'type': 'practical'},
            {'text': 'Ask others for advice', 'type': 'collaborative'},
            {'text': 'Research thoroughly', 'type': 'analytical'}
        ]
    },
    {
        'id': 5,
        'question': 'You describe yourself as:',
        'options': [
            {'text': 'Spontaneous and flexible', 'type': 'spontaneous'},
            {'text': 'Organized and planned', 'type': 'organized'},
            {'text': 'Thoughtful and reflective', 'type': 'introvert'},
            {'text': 'Energetic and outgoing', 'type': 'extrovert'}
        ]
    }
]

# Personality type descriptions
PERSONALITY_TYPES = {
    'extrovert': {
        'name': 'The Social Butterfly',
        'description': 'You thrive in social situations and gain energy from being around people. You\'re outgoing, expressive, and love meeting new people.',
        'traits': ['Energetic', 'Sociable', 'Talkative', 'Enthusiastic']
    },
    'introvert': {
        'name': 'The Thoughtful Observer',
        'description': 'You prefer quiet environments and meaningful one-on-one conversations. You recharge by spending time alone and are very self-aware.',
        'traits': ['Reflective', 'Reserved', 'Focused', 'Independent']
    },
    'analytical': {
        'name': 'The Logical Analyst',
        'description': 'You approach life with logic and reason. You enjoy solving complex problems and making decisions based on careful analysis.',
        'traits': ['Logical', 'Detailed', 'Systematic', 'Objective']
    },
    'creative': {
        'name': 'The Creative Innovator',
        'description': 'You see the world differently and love expressing yourself through creative outlets. You\'re imaginative and always full of new ideas.',
        'traits': ['Imaginative', 'Original', 'Expressive', 'Visionary']
    },
    'ambivert': {
        'name': 'The Balanced Adaptor',
        'description': 'You have the best of both worlds! You can be social when needed but also enjoy your alone time. You adapt well to different situations.',
        'traits': ['Adaptable', 'Balanced', 'Versatile', 'Socially Flexible']
    }
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/test')
def test():
    session['current_question'] = 0
    session['answers'] = {}
    return render_template('test.html', question=QUESTIONS[0], progress=0)

@app.route('/test/question/<int:question_id>', methods=['GET', 'POST'])
def question(question_id):
    if question_id < 1 or question_id > len(QUESTIONS):
        return redirect(url_for('test'))
    
    if request.method == 'POST':
        # Store the answer
        answer = request.form.get('answer')
        if answer:
            session['answers'][str(question_id)] = answer
            session.modified = True
    
    # Move to next question or show results
    if question_id < len(QUESTIONS):
        progress = (question_id / len(QUESTIONS)) * 100
        return render_template('test.html', 
                             question=QUESTIONS[question_id], 
                             progress=progress,
                             next_question=question_id + 1)
    else:
        return redirect(url_for('results'))

@app.route('/results')
def results():
    # Calculate personality type based on answers
    type_scores = {}
    for question_id, answer_type in session.get('answers', {}).items():
        type_scores[answer_type] = type_scores.get(answer_type, 0) + 1
    
    if not type_scores:
        return redirect(url_for('test'))
    
    # Get the dominant personality type
    dominant_type = max(type_scores, key=type_scores.get)
    personality_info = PERSONALITY_TYPES.get(dominant_type, PERSONALITY_TYPES['ambivert'])
    
    return render_template('results.html', 
                         personality=personality_info,
                         score=type_scores[dominant_type],
                         total_questions=len(QUESTIONS))

if __name__ == '__main__':
    app.run(debug=True)