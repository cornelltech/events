cat .env | sed 's/^/--env_var /' | sed -e 's/$/ /g' | tr -d '\n' | tr -d '"' |
xargs dev_appserver.py bookmarklet.yaml
