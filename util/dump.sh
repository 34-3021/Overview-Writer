timestamp=$(date +%Y-%m-%d-%H-%M-%S | tr -d '\n')
python3 dump.py ../backend > "llm/backend-$timestamp.txt"
python3 dump.py ../frontend > "llm/frontend-$timestamp.txt"
