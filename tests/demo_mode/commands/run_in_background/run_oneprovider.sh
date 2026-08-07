OZ_NAME=oz_test;\
until OZ_IP=$(docker inspect -f '{{.NetworkSettings.IPAddress}}' $OZ_NAME 2>/dev/null) && [ -n "$OZ_IP" ]; do\
	echo -en "Awaiting the ${OZ_NAME} container...\r"; sleep 1;\
done; echo; \
docker run --rm --detach -i --name op_test1 onedata/oneprovider:xRELEASExVERSIONx demo $OZ_IP