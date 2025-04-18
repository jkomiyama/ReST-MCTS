import re
import os
from tasks.prompts import *


# data: question: str
# mode: 'cot', 'tot', 'mcts'
# method: 'glm', 'gpt', 'local'
class SearchTask(object):
    def __init__(self, data, propose_method='glm', value_method='glm'):
        super().__init__()
        self.question = data
        self.propose_method = propose_method
        self.value_method = value_method
        self.value_cache = {}

    def clear_cache(self):
        self.value_cache = {}

    @staticmethod
    def summary_prompt_wrap(x: str, y: str = '') -> str:
        print('\n', '==============================', 'summary', '==============================', '\n')
        print('summary_prompt: \n', x + '\nExisting Steps:\n' + y + 'Summary based on the steps above:\n')
        prompt = summary_prompt + x + '\nExisting Steps:\n' + y + '\nOutput:'
        return prompt

    @staticmethod
    def MATH_summary_prompt_wrap(x: str, y: str = '') -> str:
        print('\n', '==============================', 'summary', '==============================', '\n')
        print('summary_prompt: \n', x + '\nExisting Steps:\n' + y + 'Summary based on the steps above:\n')
        prompt = MATH_summary_prompt + x + '\nSolution: ' + y + '\nExtracted answer:'
        return prompt

    @staticmethod
    def evaluate_summary_prompt_wrap(x: str, y: str = '') -> str:
        print('\n', '==============================', 'summary', '==============================', '\n')
        print('summary_prompt: \n', x + '\nExisting Steps:\n' + y + 'Summary based on the steps above:\n')
        prompt = evaluate_summary_prompt + x + '\nExisting Steps:\n' + y + '\nOutput:'
        return prompt

    @staticmethod
    def general_evaluate_summary_prompt_wrap(x: str, y: str = '') -> str:
        print('\n', '==============================', 'summary', '==============================', '\n')
        print('summary_prompt: \n', x + '\nExisting Steps:\n' + y + 'Summary based on the steps above:\n')
        prompt = general_evaluate_summary_prompt + x + '\nExisting Steps:\n' + y + '\nOutput:'
        return prompt

    @staticmethod
    def single_propose_prompt_wrap(x: str, y: str = '', step: int = 0) -> str:
        print('\n', '==============================', 'proposal', '==============================', '\nstep: ', step)
        print('propose_prompt: \n', x + '\nExisting Steps:\n' + y + 'Possible solution step based on the steps above:\n')
        prompt = single_proposal_prompt + x + '\nExisting Steps:\n' + y + '\nOutput:'
        return prompt

    @staticmethod
    def zero_single_propose_wrap(x: str, y: str = '', step: int = 0, lang: str = 'en') -> str:
        print('\n', '==============================', 'proposal', '==============================', '\nstep: ', step)
        print('propose_prompt: \n', x + '\nExisting Steps:\n' + y + 'Possible solution step based on the steps above:\n')
        if lang == 'zh':
            if not y:
                y = 'None\n'
            prompt = zero_single_proposal_prompt + x + '\nExisting Steps:\n' + y + '\nOutput:'
        else:
            if not y:
                y = 'None\n'
            prompt = zero_single_proposal_prompt_en + x + '\nExisting Steps:\n' + y + '\nOutput:'
        return prompt

    @staticmethod
    def zero_single_propose_wrap_mistral(x: str, y: str = '', step: int = 0) -> str:
        print('\n', '==============================', 'proposal', '==============================', '\nstep: ', step)
        print('propose_prompt: \n', x + '\nExisting Steps:\n' + y + 'Possible solution step based on the steps above:\n')
        if not y:
            y = 'None\n'
        prompt = zero_single_proposal_prompt_mistral + x + '\nExisting Steps:\n' + y + '\nOutput:'
        return prompt

    @staticmethod
    def zero_single_propose_wrap_gpt(x: str, y: str = '', step: int = 0, lang: str = 'en') -> str:
        print('\n', '==============================', 'proposal', '==============================', '\nstep: ', step)
        print('propose_prompt: \n', x + '\nExisting Steps:\n' + y + 'Possible solution step based on the steps above:\n')
        if lang == 'zh':
            if not y:
                y = 'None\n'
            prompt = zero_single_proposal_prompt_gpt + x + '\nExisting Steps:\n' + y + '\nOutput:'
        else:
            if not y:
                y = 'None\n'
            prompt = zero_single_proposal_prompt_gpt_en + x + '\nExisting Steps:\n' + y + '\nOutput:'
        return prompt

    @staticmethod
    def zero_single_propose_wrap_use_reflection(x: str, y: str = '', step: int = 0, ref: str = '', lang: str = 'en') -> str:
        print('\n', '==============================', 'proposal', '==============================', '\nstep: ', step)
        print('propose_prompt: \n', x + '\nExisting Steps:\n' + y + 'Possible solution step based on the steps above:\n')
        if lang == 'zh':
            if not y:
                y = 'None\n'
            if not ref:
                ref = 'None\n'
            prompt = zero_single_proposal_prompt_use_reflection + x + '\nExisting Steps:\n' + y + '\nAnalysis: ' + ref + '\nOutput:'
        else:
            if not y:
                y = 'None\n'
            if not ref:
                ref = 'None\n'
            prompt = zero_single_proposal_prompt_use_reflection_en + x + '\nExisting Steps:\n' + y + '\nAnalysis: ' + ref + '\nOutput:'
        return prompt

    @staticmethod
    def zero_single_propose_wrap_use_reflection_gpt(x: str, y: str = '', step: int = 0, ref: str = '', lang: str = 'en') -> str:
        print('\n', '==============================', 'proposal', '==============================', '\nstep: ', step)
        print('propose_prompt: \n', x + '\nExisting Steps:\n' + y + 'Possible solution step based on the steps above:\n')
        if lang == 'zh':
            if not y:
                y = 'None\n'
            if not ref:
                ref = 'None\n'
            prompt = zero_single_proposal_prompt_use_reflection_gpt + x + '\nExisting Steps:\n' + y + '\nAnalysis: ' + ref + '\nOutput:'
        else:
            if not y:
                y = 'None\n'
            if not ref:
                ref = 'None\n'
            prompt = zero_single_proposal_prompt_use_reflection_gpt_en + x + '\nExisting Steps:\n' + y + '\nAnalysis: ' + ref + '\nOutput:'
        return prompt

    @staticmethod
    def single_reflection_wrap(x: str, y: str = '', step: int = 0, lang: str = 'en') -> str:
        print('\n', '==============================', 'reflection', '==============================', '\nstep: ', step)
        print('propose_prompt: \n', x + '\nExisting Steps:\n' + y + 'Possible solution step based on the steps above:\n')
        if lang == 'zh':
            if not y:
                y = 'None\n'
            prompt = single_reflection_prompt + x + '\nExisting Steps:\n' + y + '\nOutput:'  # glm style
        else:
            if not y:
                y = 'None\n'
            prompt = single_reflection_prompt_en + x + '\nExisting Steps:\n' + y + '\nOutput:'
        return prompt

    @staticmethod
    def single_reflection_wrap_gpt(x: str, y: str = '', step: int = 0) -> str:
        print('\n', '==============================', 'reflection', '==============================', '\nstep: ', step)
        print('propose_prompt: \n', x + '\nExisting Steps:\n' + y + 'Possible solution step based on the steps above:\n')
        if not y:
            y = 'None\n'
        prompt = single_reflection_prompt_gpt + x + '\nExisting Steps:\n' + y  # gpt style
        return prompt

    @staticmethod
    def single_reflection_wrap_llama(x: str, y: str = '', step: int = 0) -> str:
        print('\n', '==============================', 'reflection', '==============================', '\nstep: ', step)
        print('propose_prompt: \n', x + '\nExisting Steps:\n' + y + 'Possible solution step based on the steps above:\n')
        if not y:
            y = 'None\n'
        prompt = single_reflection_prompt_llama + x + '\nExisting Steps:\n' + y + '\nBlank\nPlease give your opinion, do not solve the problem, your opinion should be completely based on the given steps.'  # llama style
        return prompt

    @staticmethod
    def single_reflection_wrap_simple(x: str, y: str = '', step: int = 0, lang: str = 'en') -> str:
        print('\n', '==============================', 'reflection', '==============================', '\nstep: ', step)
        print('propose_prompt: \n', x + '\nExisting Steps:\n' + y + 'Possible solution step based on the steps above:\n')
        if lang == 'zh':
            if not y:
                y = 'None\n'
            prompt = single_reflection_prompt_simple + x + '\nExisting Steps:\n' + y + '\nOutput:'  # simple style
        else:
            if not y:
                y = 'None\n'
            prompt = single_reflection_prompt_simple_en + x + '\nExisting Steps:\n' + y + '\nOutput:'
        return prompt

    @staticmethod
    def single_reflection_wrap_simple_mistral(x: str, y: str = '', step: int = 0) -> str:
        print('\n', '==============================', 'reflection', '==============================', '\nstep: ', step)
        print('propose_prompt: \n', x + '\nExisting Steps:\n' + y + 'Possible solution step based on the steps above:\n')
        if not y:
            y = 'None\n'
        prompt = single_reflection_prompt_simple_mistral + x + '\nExisting Steps:\n' + y + '\nOutput:'
        return prompt

    @staticmethod
    def value_prompt_wrap(x: str, y: str) -> str:
        print('\n', '==============================', 'critic', '==============================', '\n')
        value_prompt = critic_simplified + x + '\nExisting Steps:\n' + y.strip() + '\nOutput:'
        return value_prompt

    @staticmethod
    def self_critic_prompt_wrap(x: str, y: str) -> str:
        print('\n', '==============================', 'self-critic', '==============================', '\n')
        if not y:
            y = 'None\n'
        critic_prompt = self_critic_prompt + x + '\nSolution:\n' + y + '\nScore:'
        return critic_prompt

    @staticmethod
    def cot_prompt_wrap(x: str, lang: str = 'en', use_math: bool = False) -> str:
        print('\n', '==============================', 'proposal', '==============================', '\n')
        if not use_math:
            if lang == 'zh':
                prompt = cot_prompt + x + "\n解答过程:"
            else:
                prompt = cot_prompt_en + x + "\nSolution:"
        else:
            prompt = MATH_cot_prompt.format(query=x)
        print('propose_prompt: \n', prompt, '\n')
        return prompt

    @staticmethod
    def value_outputs_unwrap(value_outputs: list, low=0.0, high=1.0) -> float:
        out_value = low
        all_out = ''
        for _ in value_outputs:
            all_out = all_out + _
        if 'Score' not in all_out:
            print('Score output is invalid!\n')
            return out_value
        stp = all_out.split('Score')[-1].strip()
        try:
            match = re.findall(r'-?[0-9]+\.?[0-9]*', stp)[-1]
            out_value = float(match)
            out_value = min(max(low, out_value), high)
        except Exception as e:
            print(f'分数输出有误！错误类型:{e}\n')
            return low
        return out_value
