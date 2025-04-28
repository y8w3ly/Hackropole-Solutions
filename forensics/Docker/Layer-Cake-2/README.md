# **Layer Cake 2/3**

## **Description**
Un développeur de GoodCorp souhaite publier une nouvelle image Docker. Il copie au moment du build un fichier contenant un flag, puis le supprime. Il vous assure que ce secret n’est pas visible du public. L’image est [anssi/fcsc2024-forensics-layer-cake-2](https://hub.docker.com/r/anssi/fcsc2024-forensics-layer-cake-2).


## **Solution**

+ First we pull `docker pull anssi/fcsc2024-forensics-layer-cake-2:latest`, we get : 

```
latest: Pulling from anssi/fcsc2024-forensics-layer-cake-2
4abcf2066143: Already exists 
a0eaf34c8bac: Pull complete 
1ba3c4c6a2e3: Pull complete 
Digest: sha256:86a863f674adbbae9168d1a5d233478cd9747a587a322b8950fcb39f3992be7a
Status: Downloaded newer image for anssi/fcsc2024-forensics-layer-cake-2:latest
docker.io/anssi/fcsc2024-forensics-layer-cake-2:latest
```

+ I was suck at docker so I made some research and found out that :
 - Each instruction in a Dockerfile (e.g. COPY, RUN) generates a new image layer. These layers are immutable and stacked to form the final filesystem.
 - File deletion in a later layer doesn’t purge the data; Docker marks files as removed via “whiteout” entries (character devices with 0/0 device numbers under overlayfs) but the original file content persists in the lower layer’s tar

+ But After I runned `docker history --no-trunc anssi/fcsc2024-forensics-layer-cake-2:latest` that was the result :

```
IMAGE                                                                     CREATED         CREATED BY                                                                                          SIZE      COMMENT
sha256:03014d9fc4801b1810b112fd53e05e35ea127e55c82d1304b5622cfe257c0ad8   13 months ago   CMD ["/bin/sh"]                                                                                     0B        buildkit.dockerfile.v0
<missing>                                                                 13 months ago   USER guest                                                                                          0B        buildkit.dockerfile.v0
<missing>                                                                 13 months ago   RUN /bin/sh -c rm /tmp/secret # buildkit                                                            0B        buildkit.dockerfile.v0
<missing>                                                                 13 months ago   COPY secret /tmp # buildkit                                                                         71B       buildkit.dockerfile.v0
<missing>                                                                 15 months ago   /bin/sh -c #(nop)  CMD ["/bin/sh"]                                                                  0B        
<missing>                                                                 15 months ago   /bin/sh -c #(nop) ADD file:37a76ec18f9887751cd8473744917d08b7431fc4085097bb6a09d81b41775473 in /    7.38MB
```

+ So our guy didn't use RUN rm to remove the secret, instead he did it after getting the shell.
+ After more research I found a tool named [Dive](https://github.com/wagoodman/dive) for interactive layer inspection.

+ Let's try `dive anssi/fcsc2024-forensics-layer-cake-2` 
STILL STUCK HERE
