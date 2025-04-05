from models.get_response import *


def llm_verify(ans, real_ans, judge_model='gpt-4-1106-preview'):
    prompt = 'I will input two texts. The first text is a solution or answer to a science question (which may not be correct), and the second text is the standard answer to this question. Please determine if the answer from the first solution is mathematically equivalent to the standard answer, and output only "0" or "1" based on your judgment, without any additional information. Output "1" if the answers are consistent; otherwise, output "0" if the answers do not match, or if the first text does not clearly indicate an answer or does not include a LaTeX expression. If the relationship between the first solution and the standard answer is ambiguous, output "0".\n'
    qry = prompt + 'Text 1:' + ans + '\n' + 'Text 2:' + real_ans + '\nOutput:'
    lbl = ''
    cnt = 5
    while lbl == '' and cnt:
        out = ''
        try:
            chat_comp = openai.ChatCompletion.create(model=judge_model, messages=[{"role": "user", "content": qry}])
            out = chat_comp.choices[0].message.content[0]
        except Exception as e:
            print(f'Error:{e}\n')
        if out == '0' or out == '1':
            lbl = out
        else:
            cnt -= 1
    if not cnt:
        return 0
    return int(lbl)
