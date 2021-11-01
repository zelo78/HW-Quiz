import json
import random


class GenericQuestion:

    def __init__(self, *,
                 text,
                 author,
                 complexity,
                 correct_answers,
                 topic,
                 is_asked=False,
                 user_answer='',
                 points_awarded=0,
                 ):

        self.text = text
        self.author = author
        self.complexity = complexity
        self.correct_answers = [answer.strip() for answer in correct_answers]
        self.topic = topic
        self.is_asked = is_asked
        self.user_answer = user_answer
        self.points_awarded = points_awarded


class Question(GenericQuestion):

    def get_points(self):
        ''' Возвращает int, количество баллов.
Баллы зависят от сложности: за 1 дается 10 баллов, за 5 дается 50 баллов.'''
        points = 10 * self.complexity
        return points

    def is_correct(self):
        ''' Возвращает True, если ответ пользователя совпадает с одним из верных ответов.'''
        answer = self.user_answer.strip().lower()
        if answer in [answer.lower() for answer in self.correct_answers]:
            return True
        else:
            return False

    def build_question(self, current_number):
        '''Возвращает вопрос в понятном пользователю виде, учитывая его текущий номер'''
        complexity_to_text = {
            1: 'просто', 2: 'просто',
            3: 'средняя', 4: 'средняя',
            5: 'сложно',
        }

        s = f'Вопрос {current_number}, тема {self.topic}, сложность {complexity_to_text[self.complexity]}\n{self.text}'
        return s


def read_questions(file_name):
    with open(file_name, mode='rt') as f:
        base = json.load(f)

    questions = []

    for record in base:
        question = Question(**record)
        questions.append(question)

    return questions


def run_quiz(questions):
    for i, question in enumerate(questions):
        print(question.build_question(i+1))
        answer = input('Введите Ваш ответ: ')

        question.is_asked = True
        question.user_answer = answer

        if question.is_correct():
            points = question.get_points()
            question.points_awarded = points
            print(f'Ответ верный, получено {points} баллов.')
        else:
            right_answer = question.correct_answers[0]
            print(f'Ответ неверный. Правильный ответ - {right_answer}.')

    asked_questions, right_answers, points_awarded = 0, 0, 0
    for question in questions:
        if question.is_asked:
            asked_questions += 1
        if question.is_correct():
            right_answers += 1
        points_awarded += question.points_awarded

    print('Вот и всё!')
    print(f'Правильно отвечено на {right_answers} вопросов из {asked_questions}, набрано {points_awarded} баллов.')


def main():
    BASE_FILE_NAME = 'base1.json'
    questions = read_questions(BASE_FILE_NAME)

    random.shuffle(questions)

    run_quiz(questions)

if __name__ == '__main__':
    main()
