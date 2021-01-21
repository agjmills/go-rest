FROM public.ecr.aws/lambda/python:3.8

RUN yum -y install nmap pip 
RUN pip install python-nmap

COPY app.py ./

CMD ["app.handler"]
