python evaluate.py \
  --task_name "math" \
  --file "math_500" \
  --propose_method "llama" \
  --value_method "local" \
  --mode "mcts" \
  --evaluate "math" \
  --iteration_limit 50 \
  --use_reflection "simple" \
  --branch 3 | tee test_evaluate_math500.log
