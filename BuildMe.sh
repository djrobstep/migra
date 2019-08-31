export ARTIFACTNAME=pydbmigra
export MAINFILE=pydbmigra.py
export SOURCEPATH=migra
echo "version_dict = {\"git_hash\":\"\"\"">version.py
git rev-parse HEAD >>version.py
echo "\"\"\",">>version.py
echo "\"build_time\":\"\"\"">>version.py
date >>version.py
echo "\"\"\"">>version.py




echo "}">>version.py
docker build -t builder -f Build.Dockerfile .
docker rm buildmecentos
#ßdocker run -it -v /tmp/deploy-ready/:/Build/output builder  
docker run -it --name buildmecentos -v /tmp/deploy-ready/:/Build/output builder /Build/tmp/$ARTIFACTNAME --version
#docker run -it --name buildmecentos -v /tmp/deploy-ready/:/Build/output builder cp $ARTIFACTNAME_centos_6_10.tar /Build/output/
#####docker cp buildmecentos:/Build/$ARTIFACTNAME_centos_6_10.tar $ARTIFACTNAME_centos_6_10.tar 
# debug docker --rm -it <hash> sh

#pyinstaller pydbmigra.py --onefile --add-data 'schemainspect/pg/sql/*.sql:schemainspect/pg/sql/'