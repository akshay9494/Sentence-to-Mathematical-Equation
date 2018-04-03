from word2number import w2n
import re
import logging

stop_words = ['how', 'much', 'is', 'what', '?', 'of', 'calculate', 'hey', 'tejas', 'dude',
              'find', 'please', 'the', 'answer', 'tell', 'to', 'when']

multiplication = ['times', 'into', 'x']
division = ['by']
addition = ['plus']
subtraction = ['minus']
power = []

multiplication_multiword = ['multiplied by']
division_multiword = ['divided by']
addition_multiword = []
subtraction_multiword = ['subtracted by']
power_multiword = ['raised to', 'to the power']

punctuations = ['.', ',', '!']

math_symbols = ['/', '*', '+', '-']

def sent_to_result(sentence):
    try:
        # print(sentence)
        sentence = sentence.lower()
        try:
            new_sentence = sentence.replace('x', '*').replace('^', '**')
            res = eval(new_sentence)
            logging.info('Straight answer: {}'.format(res))
            return new_sentence, res
        except Exception as e:
            logging.error(e)
            logging.error('Could not directly evaluate, doing further processing')

        for m in multiplication_multiword:
            if m in sentence:
                sentence = sentence.replace(m, '*')
        for m in division_multiword:
            if m in sentence:
                sentence = sentence.replace(m, '/')
        for m in addition_multiword:
            if m in sentence:
                sentence = sentence.replace(m, '+')
        for m in subtraction_multiword:
            if m in sentence:
                sentence = sentence.replace(m, '-')
        for m in power_multiword:
            if m in sentence:
                sentence = sentence.replace(m, '**')

        res = re.split("[ ?]+", sentence)
        s_list = [r for r in res if r not in stop_words]
        s_list = [s for s in s_list if s != '']
        sent = []
        for s in s_list:
            if s[-1] in punctuations:
                sent.append(s[:-1])
            else:
                sent.append(s)
        sentence = ' '.join(sent)
        sentence = sentence.lstrip().rstrip()
        logging.debug('Sentence preprocessed as: {}'.format(sentence))

        split_sentence = sentence.split()
        for idx, s in enumerate(split_sentence):
            if s in multiplication:
                split_sentence[idx] = '*'
            elif s in division:
                split_sentence[idx] = '/'
            elif s in addition:
                split_sentence[idx] = '+'
            elif s in subtraction:
                split_sentence[idx] = '-'
            elif s in power:
                split_sentence[idx] = '**'

        sentence = ' '.join(split_sentence)
        logging.debug('Equations formatted as: {}'.format(sentence))
        res = re.split("[/*+-]+", sentence)
        res = [r.lstrip().rstrip() for r in res]
        # print(res)
        for r in res:
            sentence = sentence.replace(r, str(w2n.word_to_num(r)))
        logging.debug('Mathematical Equation formed as: {}'.format(sentence))
        return sentence, eval(sentence)
    except Exception as e:
        logging.error('Error happened!!')
        logging.error(e, exc_info=True)
        return None, None




if __name__ == '__main__':
    sent1 = 'how much is two plus two minus three?'
    sent2 = 'what is four hundred and fifty divided by 3 times eight?'
    sent3 = 'how much is twenty two thousand four hundred and fifty one minus 33 multiplied by forty four?'
    sent4 = 'what is eighty seven point nine into six point three three'
    sent5 = 'two to the power of four'
    sent6 = 'what is two raised to four by six'
    sent7 = 'calculate ninety nine minus twenty three.'
    sent8 = '2-3+5-6'

    sent = sent7

    print('Query: {}'.format(sent))
    res = sent_to_result(sent)

    if res is None:
        print('This calculation is way beyond my comprehension! Please ask me something simpler :P')
    else:
        print('Answer: {}'.format(res))