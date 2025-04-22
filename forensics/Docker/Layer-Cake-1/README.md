#Description#
A GoodCorp developer wants to publish a new Docker image. He uses an environment variable storing a flag at build time, and assures you that this secret is not visible to the public. The image is [anssi/fcsc2024-forensics-layer-cake-1](https://hub.docker.com/r/anssi/fcsc2024-forensics-layer-cake-1).

#Solution#
The description says that the image owner uses an environment variable so it must be declared while building.
but when we run `docker pull anssi/fcsc2024-forensics-layer-cake-1:latest` we got no files downloaded but this does not mean the image is empty.
So i tried to run it with an interactive shell : `docker run -it anssi/fcsc2024-forensics-layer-cake-1:latest` tried something like finding such file named flag.txt but I found nothing.
And as the description mentionned an environment variable was declared, chatgpt suggested to try : `docker history anssi/fcsc2024-forensics-layer-cake-1`
After running it i got this output : 
```
IMAGE          CREATED         CREATED BY                                      SIZE      COMMENT
0faa62781dd1   15 months ago   CMD ["/bin/sh"]                                 0B        buildkit.dockerfile.v0
<missing>      15 months ago   USER guest                                      0B        buildkit.dockerfile.v0
<missing>      15 months ago   ARG FIRST_FLAG=FCSC{a1240d90ebeed7c6c422969e…   0B        buildkit.dockerfile.v0
<missing>      15 months ago   /bin/sh -c #(nop)  CMD ["/bin/sh"]              0B        
<missing>      15 months ago   /bin/sh -c #(nop) ADD file:37a76ec18f9887751…   7.38MB
```
we can see the start of the flag but not completed.
so we must add the argument `--no-trunc` and here we go:
```
<missing>                                                                 15 months ago   ARG FIRST_FLAG=FCSC{a1240d90ebeed7c6c422969ee529cc3e1046a3cf337efe51432e49b1a27c6ad2}
```


