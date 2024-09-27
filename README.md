How to run: 
1. Copy `docker/.envs.sample` to `docker/.envs` and fill it.
2. Run these commands:
```
docker-compose --env-file docker/.envs -f docker/docker-compose.yml --project-directory . build
docker-compose --env-file docker/.envs -f docker/docker-compose.yml --project-directory . up -d
```
