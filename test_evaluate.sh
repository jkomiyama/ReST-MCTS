python evaluate.py \
  --task_name "scibench" \
  --file "thermo_standardized" \
  --propose_method "llama" \
  --value_method "local" \
  --mode "mcts" \
  --evaluate "scibench" \
  --iteration_limit 50 \
  --use_reflection "simple" \
  --branch 3
