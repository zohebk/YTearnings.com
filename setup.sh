export GRADIO_SERVER_NAME=0.0.0.0 
export GRADIO_SERVER_PORT="$PORT"
cp cdnindex.html /app/.heroku/python/lib/python3.11/site-packages/gradio/templates/cdn/index.html
cp frontendindex.html /app/.heroku/python/lib/python3.11/site-packages/gradio/templates/frontend/index.html
