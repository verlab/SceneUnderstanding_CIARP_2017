FROM hugozanini/verlabfinal:finalok

MAINTAINER Verlab (www.verlab.com.br)

# Expose Ports for TensorBoard (6006), Ipython (8888)
EXPOSE 6006 8888

COPY source /root/source

WORKDIR "/root"
CMD ["/bin/bash"]
