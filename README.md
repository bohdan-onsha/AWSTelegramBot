This template will help you in developing and deploying webhook-based telegram bots.
Echo bot is included :)

Libraries & frameworks used:
- Telegram Bot Api library: [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI)
- Deployment framework: [aws-syndicate](https://github.com/epam/aws-syndicate)
- WSGI web application framework (for local development): [Flask](https://pypi.org/project/Flask/)


Project structure
```
├── README.md                                   <--- YOU ARE HERE
├── cd.sh                                       <--- Deployment script
├── requirements.txt                            <--- Project requirements
├── sdct.log                                    <--- Syndicate logs
    ├── src                                      <--- Sources root
│   ├── __init__.py
│   ├── deployment_resources.json               <--- Syndicate deployment resources
│   ├── helpers                                 <--- module for helping tools
│   │   ├── __init__.py
│   │   ├── exception.py                  <--- custom project exception
│   │   └── log_helper.py                 <--- logger configurator
│   ├── lambdas                           <--- module for lambda functions
│   │   ├── __init__.py
│   │   └── telegram-bot-handler          <--- lambda root
│   │       ├── __init__.py
│   │       ├── debug.py                  <--- flask server script
│   │       ├── deployment_resources.json <--- deployment resources for lambda
│   │       ├── handler.py                <--- lambda entry point
│   │       ├── lambda_config.json        <--- lambda configuration
│   │       ├── local_requirements.txt    <--- local modules required by lambda
│   │       └── requirements.txt          <--- third-party libraries required by lambda
│   └── services                          <--- services module
│       ├── __init__.py
│       ├── abstract_lambda.py                  <--- abstract lambda handler
│       ├── environment_service.py              <--- environment service
│       └── service_provider.py                 <--- service provider
├── syndicate_conf                              <--- Syndicate config directory
│   ├── bundles                                 <--- deployment bundles
│   │   └── aws-telegram-bot_270621.185829_deploy  <--- bundle folder
│   │       ├── build_meta.json                    <--- bundle meta
│   │       └── telegram-bot-handler-1.0.zip       <--- bundle zip
│   ├── syndicate.yml                           <--- Syndicate configuration file
│   └── syndicate_aliases.yml                   <--- Syndicate aliases file
```


## Installation

1. Clone repository:
   `git clone https://github.com/bohdan-onsha/AWSTelegramBot`
2. Move into root directory:
   `ch AWSTelegramBot/`
3. Create virtual environment:
   `virtualenv -p python3 .venv`
4. Activate virtual environment:
   `source .venv/bin/activate`
5. Install dependencies with pip:
   `python3 -m pip install -r requirements.txt`

### Local development:

1. Install & configure https tunnel to localhost (using
   [ngrok](https://ngrok.com/) or any other took you like)  

2. In `src/lambdas/telegram-bot-handler/debug.py`:
- Replace `TARGET_PORT` (if needed, 80 by default)
- Replace `WEBHOOK_URL` with your url

   
3. `python debug.py`
   That's it. You're ready to make something fantastic!

### Deploy
1. Configure `syndicate_conf/syndicate.yml`

```yaml
account_id: $AWS_ACCOUNT_ID
aws_access_key_id: $AWS_ACCESS_KEY_ID
aws_secret_access_key: $AWS_SECRET_ACCESS_KEY
deploy_target_bucket: $DEPLOY_TARGET_BUCKET
project_path: $YOUR_PATH/AWSTelegramBot/src
region: eu-central-1
resources_prefix: tg-
build_projects_mapping:
  python:
    - /
```

2. Configure `syndicate_conf/syndicate_aliases.yml`
```yaml
account_id: $AWS_ACCOUNT_ID
lambdas_alias_name: dev
region: eu-central-1
bot_token: $BOT_TOKEN
```

3. Set `SDCT_CONF` environment variable:  
`export SDCT_CONF=YOUR_PATH/AWSTelegramBot/syndicate_conf`

4. Deploy your bot:   
`sh cd.sh deploy`

Upon this, syndicate will create:

1. Lambda function: `telegram-bot-handler`
2. API gateway `telegram-bot-api`, with 1 endpoint to trigger lambda

3. Configure webhook for your bot:
```python3
bot.set_webhook(url='https://{IG_HOST}.execute-api.eu-central-1.amazonaws.com/prod/handler')
```
4. Done, you can trigger the bot.

### Update lambda:
Complete redeploy is not required, just:
`sh cd.sh`

### Clean resources:
`syndicate clean --deploy_name aws-telegram-bot --bundle_name YOUR_DEPLOY_BUNDLE_NAME`