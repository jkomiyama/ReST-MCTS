import torch
from transformers import AutoModelForCausalLM

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
base_model = AutoModelForCausalLM.from_pretrained(
            "/workspace/ckpt/MetaMath-Mistral-7B",
                trust_remote_code=True,
                    torch_dtype=torch.bfloat16
                    ).to(device)
