This is a [Docker Hub container](https://hub.docker.com/r/masterandrey/docker-amazon-dash-button-hack/) 
for the Amazon Dash Button hack.

To run it:
```
docker rm -f amazon_dash
docker run --net host -it --name amazon_dash -v $PWD/amazon-dash-private:/amazon-dash-private:ro masterandrey/docker-amazon-dash-button-hack
```

This is configured to make http requests on button presses.

Forked from [docker-amazon-dash-button-hack](https://github.com/masterandrey/docker-amazon-dash-button-hack)
See details from the creator's blog in [Smart wifi button and Docker on Synology (Amazon Dash Button hack)](http://masterandrey.com/posts/en/amazon_dash_button_hack/).
