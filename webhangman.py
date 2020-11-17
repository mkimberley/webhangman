# eHangman.com v

import random
import os
from flask import Flask,render_template,request,redirect,url_for
from copy import deepcopy

lettersguessed=''

HANGMAN =  [
                ['|', '-', '-', '-', '-', ' ', ' ', ' '],
                ['|', ' ', ' ', ' ', '|', ' ', ' ', ' '],
                ['|', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                ['|', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                ['|', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                ['|', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                ['|', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
           ]

HANGMAN_STAGES = [
                    [4, 2, 'O'],
                    [4, 3, '+'],
                    [3, 3, '/'],
                    [5, 3, '\\'],
                    [4, 4, '|'],
                    [3, 5, '/'],
                    [5, 5, '\\']
                 ]
SPACE = '_'

def get_random_word():
    word_list = ['apple', 'pepper', 'sausage']
    return random.choice(word_list)

def get_hangman_string(guessed,word):

    draw_list=deepcopy(HANGMAN)

    guessed_word = [SPACE] * len(word)
    guessed_letters = set()
    tries = 0

    for letter in guessed:
        guessed_letters.add(letter)

        if letter in word:
            for idx, char in enumerate(word):
                if char == letter:
                    guessed_word[idx] = letter
        else:
            x, y, value = HANGMAN_STAGES[tries]
            draw_list[y][x] = value
            tries += 1

        if all(char != SPACE for char in guessed_word):
            return(draw_list,word+'\n\nYou got it!','won')

        elif tries == len(HANGMAN_STAGES):
            gamestate='lost'
            return(draw_list,'Bad luck, it was {}'.format(word),'lost')

    return (draw_list,guessed_word,'playing')

app = Flask(__name__)


@app.route('/')
def redir_to_game():
   return redirect(url_for('run_hangman_web'))

@app.route('/hangman/newgame')
def new_game():
   return redirect(url_for('run_hangman_web'))

@app.route('/hangman/',methods = ['POST', 'GET'])
def run_hangman_web():
   #global lettersguessed
   thisguess=''
   lettersguessed=''
   word=get_random_word()
   if request.method == 'POST':
      thisguess = request.form['guess']
      lettersguessed = request.form['lettersguessed']
      word = request.form['word']
   ### thisguess = request.args.get('guess')  <- if using get 
   
   lettersguessed=lettersguessed+thisguess

   (hangman,guessed,gamestate)=get_hangman_string(lettersguessed,word)

   hman='\n'.join(''.join(row) for row in hangman)
   guess=''.join(guessed)

   if gamestate == "playing": 
      guess="Letters guessed: "+guess

   return render_template('hangman.html',hangman=hman,guessed=guess,state=gamestate,lettersguessed=lettersguessed,word=word)

if __name__ == '__main__':
   port = os.getenv('PORT', '5000')
   app.run(host='0.0.0.0', port=int(port))


