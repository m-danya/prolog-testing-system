./submit.sh $2 2>/dev/null | jq .submission_id | xargs ./execute.sh $1
