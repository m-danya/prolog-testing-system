curl \
    -H "Content-Type: application/json" \
    -d '{"type": "gprolog", "task": "'$1'", "submission_id": "'$2'"}' \
  http://localhost:3001/execute

