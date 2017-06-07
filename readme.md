### run à la
- `docker build -t crashtest .`
- `docker run -it -e version=5.1 crashtest` or `docker run -it -e version=6 crashtest`

It should crash on 5.1, and not on 6.
