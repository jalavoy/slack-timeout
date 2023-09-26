# Slack Time-out
Put a user in timeout when they're being annoying.

## Permissions
You'll need to setup a slack app with the following scopes:

### Bot Token Scopes
- app_mentions:read
- channels:history
- chat:write
- groups:history
- users:read

### User Token Scopes
- chat:write

### Dependencies
You'll need a redis running somewhere to store the time-outs. I'm too lazy to store/implement it in code and want it to persist beyond restarts.

### Environment
- REDIS_HOST: Host of redis, defaults to localhost
- REDIS_PORT: Port of redis, defaults to 6379
- SLACK_APP_TOKEN: Token for your slack app
- SLACK_BOT_TOKEN: Token for your apps BOT scope (see permissions & OAUTH)
- SLACK_OAUTH_TOKEN: Token for your apps USER scope (see permissions & OAUTH)