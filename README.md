# Интерактивное расписание занятий



## Setup

Docker:
```bash
git clone https://github.com/thek4n/ClassSchedule
cd ClassSchedule
# create .env file (env.example)
./run build
./run createsuperuser
./run rund "$(nroc)"  # create container with 8000 port with nproc workers
```