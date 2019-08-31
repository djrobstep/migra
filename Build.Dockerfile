FROM centos:6.10
ARG RELEASENAME=centos_6_10
ARG SOURCEPATH=migra
ARG ARTIFACTNAME=pydbmigra
ARG MAINFILE=pydbmigra.py
RUN yum -y update && \
    yum -y install yum-utils && \
    yum -y groupinstall development && \
    yum -y install https://centos6.iuscommunity.org/ius-release.rpm && \
    yum -y install python36u && \
    yum -y install python36u-devel && \ 
    yum -y install python36u-setuptools

RUN easy_install-3.6 pip && \
    pip3 install pyinstaller

RUN mkdir -p Build/
WORKDIR Build/

COPY $SOURCEPATH/ .

 
 
RUN ls . -la
ENV PYTHONPATH="/Build/"
RUN pip3 install -r $SOURCEPATH/requirements.txt
RUN head -n -1 /Build/version.py >/Build/version2.py
RUN mv /Build/version2.py /Build/version.py

#inject distro into version.py
RUN echo ",\"distro\":\"\"\"">>/version.py
RUN cat /etc/redhat-release >>/version.py
RUN echo "\"\"\"">>/version.py

#inject libs into version.py
RUN echo ",\"python_libs\":\"\"\"" >>/Build/version.py
RUN pip freeze >>/Build/version.py
RUN echo "\"\"\"}" >>/Build/version.py
#RUN pyinstaller $SOURCEPATH/$ARTIFACTNAME.py  --add-data /Build/version.txt:.  --onefile
#RUN pyinstaller $MAINFILE  --onefile --paths $PYTHONPATH
RUN pyinstaller $MAINFILE --onefile --paths $PYTHONPATH --add-data 'schemainspect/pg/sql/*.sql:schemainspect/pg/sql/' -n ${ARTIFACTNAME}
RUN mkdir tmp 
RUN tar -czvf ${ARTIFACTNAME}_${RELEASENAME}.tar -C /Build/dist/ . 
RUN tar -xvf ./${ARTIFACTNAME}_${RELEASENAME}.tar -C ./tmp/
# RUN pip3 install -r $SOURCEPATH/requirements.txt
# RUN pyinstaller $SOURCEPATH/$ARTIFACTNAME.py -w --onefile
# RUN tar -czvf $ARTIFACTNAME.tar -C dist/ .

#for testing
ENV PGHOST=db
ENV PGDATABASE=postgres
ENV PGUSER=postgres
ENV PGPASSWORD=docker
ENV PGPORT=5432 