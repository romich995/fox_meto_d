seq 1 10 | xargs -n1 -P10   curl -X POST \
      -H "Content-Type: application/json" \
      -d '{"from_wallet": 2, "to_wallet": 3, "transfer_amount": 100000}' \
      http://localhost:8000/api/transfer

