OZ_NAME=oz_test;\
until OZ_IP=$(docker inspect -f '{{.NetworkSettings.IPAddress}}' $OZ_NAME 2>/dev/null) && [ -n "$OZ_IP" ]; do\
	echo -en "Awaiting the ${OZ_NAME} container...\r"; sleep 1;\
done; echo; \
docker run --rm -it --name op_test2 onedata/oneprovider:xRELEASExVERSIONx demo $OZ_IP