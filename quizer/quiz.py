import json
import random


def load_data(data_file):
    
    with open('data/'+data_file) as json_file:
        data = json.load(json_file)

    return data



def standard(data, numberOfQuestions):
    #Show questions in random order
    mode = 'standard'

    questions = list(data.keys())

    random.shuffle(questions)

    for i in range(numberOfQuestions):
        print('\n',questions[i])

        correctAnswer = data[questions[i]]

        wrongAnswers = list(data.values())
        del wrongAnswers[wrongAnswers.index(correctAnswer)]
        wrongAnswers = random.sample(wrongAnswers, 3)
        answerOptions = wrongAnswers + [correctAnswer]
        random.shuffle(answerOptions)

        check_answer(data, questions[i], correctAnswer, answerOptions, mode)

def advanced(data, numberOfQuestions, data_file):
    #Show the less known questions first, admits different kinds of questions
    mode = 'advanced'

    questions = []
    for q in list(data.keys()):
        if data[q][3]==0:
            f = 0
        else:
            f = data[q][2]**2/data[q][3]
        questions.append((q,f))

    questions.sort(key=lambda tup: tup[1])

    for i in range(numberOfQuestions):
        print('\n',questions[i][0])

        correctAnswer = data[questions[i][0]][0]

        wrongAnswers = []
        for q in questions:
            if data[questions[i][0]][1] == data[q[0]][1] and data[q[0]][0] != correctAnswer:
                wrongAnswers += [data[q[0]][0]]
        wrongAnswers = random.sample(wrongAnswers, 3)
        answerOptions = wrongAnswers + [correctAnswer]
        random.shuffle(answerOptions)

        data = check_answer(data, questions[i][0], correctAnswer, answerOptions, mode)

        save_data(data,data_file)


def check_answer(data, q, correctAnswer, answerOptions, mode):
    for n,a in enumerate(answerOptions):
        print(n+1,'. ',a)

    answer = input('Introduce the number of the answer: ')

    if mode == 'advanced':
        data[q][3] += 1
    
    if answerOptions[int(answer)-1] == correctAnswer:
        print('\n Correct!')
        if mode == 'advanced':
            data[q][2] += 1

    else:
        print('\n Wrong! The answer was: ', correctAnswer)

    return data

def save_data(data, data_file):
     with open('data/'+data_file, 'w') as json_file:
        json.dump(data,json_file)

def main():

    #Initial parameters

    numberOfQuestions = int(input('Number of questions: '))
    data_file = input('Quiz name (i.e. "test2"): ')+'.json'

    data = load_data(data_file)

    if type(list(data.values())[0]) == list:
        advanced(data, numberOfQuestions, data_file)
    else:
        standard(data, numberOfQuestions)

if __name__ == '__main__':
    main()
    