docker run -it --rm \
    -v $(pwd)/bin:/app \
    --env-file $(pwd)/.env \
    --network steem-watcher_steem_watcher_net \
    ety001/steem-python:mysql \
    /bin/ash
    
