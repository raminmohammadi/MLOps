# Toturial Video
you can watch the toturial vidoe on my channel [Video](https://youtu.be/stdbAFjHAQY?si=vgOsFnBz_lMUF1X-)




# Docker Cheatsheet

## Basic Commands

### Images
- **List images**
  ```sh
  docker images
  ```

- **Pull an image from a repository**

```sh
docker pull <repository>:<tag>
```

- **Remove an image**
```sh
docker rmi <image_id>
```

## Containers
**
- **List running containers**
```sh
docker ps
```

- **List all containers (including stopped ones)**
```sh
docker ps -a
```

- **Run a container**
```sh
docker run -d -p <host_port>:<container_port> <repository>:<tag>
```

- **Stop a running container**
```sh
docker stop <container_id>
```

- **Remove a container**
```sh
docker rm <container_id>
```

### Volumes
- **List volumes**
```sh
  docker volume ls
```

- **Create a volume**
```sh
  docker volume create <volume_name>
```

- **Remove a volume**
```sh
  docker volume rm <volume_name>
```

### Networks
- **List networks**
```sh
  docker network ls
```

- **Create a network**
```sh
  docker network create <network_name>
```

- **Remove a network**
```sh
  docker network rm <network_name>
```

## Advanced Commands

### Building Images
- **Build an image from a Dockerfile**
```sh
  docker build -t <repository>:<tag> <path_to_dockerfile>
```

### Managing Containers
- **Start a stopped container**
```sh
  docker start <container_id>
```

- **Restart a container**
```sh
  docker restart <container_id>
```

- **Attach to a running container**
```sh
  docker attach <container_id>
```

- **View container logs**
```sh
  docker logs <container_id>
```

### Pruning
- **Remove unused data (images, containers, volumes, and networks)**
```sh
  docker system prune
```

## Deleting All Docker Images Locally

1. Stop all running containers:
```sh
   docker stop $(docker ps -q)
```

2. Remove all containers:
```sh
   docker rm $(docker ps -a -q)
```

3. Remove all images:
```sh
   docker rmi $(docker images -q)
```

### One-liner Command

To delete all Docker images, containers, and volumes with a single command:
```sh
docker stop $(docker ps -q) && docker rm $(docker ps -a -q) && docker rmi $(docker images -q)
```
### Additional Cleanup

To also remove all unused volumes and networks:
```sh
docker volume prune -f
docker network prune -f
```