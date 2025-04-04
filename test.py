import torch
if torch.cuda.is_available():
    print("GPU is available")
    print(f"GPU count: {torch.cuda.device_count()}")
    print(f"GPU now: {torch.cuda.get_device_name(0)}")
else:
    print("GPU is not available")

from MCTS.task import *
question = "Calculate the sum of the first 10 prime numbers."
task = MCTS_Task(question, 'llama', 'local', lang='en', iteration_limit=100)
output = task.run()
print(output['solution'])
