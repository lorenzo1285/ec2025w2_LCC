FROM pklehre/ec2025-lab2

ADD lxc1039.py /bin/
ADD IBGA.py /bin/
ADD maxsat.py /bin/
ADD sbox_4.wcnf /bin/
ADD requirements.txt /bin/

RUN pip install --no-cache-dir -r /bin/requirements.txt

CMD ["-username", "lxc1039", "-submission", "python3 /bin/lxc1039.py"]
