OZ_NAME=oz_test;\
until OZ_IP=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $OZ_NAME 2>/dev/null) && [ -n "$OZ_IP" ]; do\
	echo -en "Awaiting the ${OZ_NAME} container...\r"; sleep 1;\
done; echo; \
docker run --rm -i --name op_test1 -h op_test1 -v /tmp/op-pers:/volumes/persistence -v /tmp/op-storage:/volumes/storage onedata/oneprovider:xRELEASExVERSIONx demo $OZ_IP