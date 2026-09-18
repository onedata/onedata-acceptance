OZ_NAME=oz_test;\
until OZ_IP=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $OZ_NAME 2>/dev/null) && [ -n "$OZ_IP" ]; do\
	echo -en "Awaiting the ${OZ_NAME} container...\r"; sleep 1;\
done; echo; \
docker run --rm --detach -i --name xCONTAINERxNAMEx onedata/oneprovider:xRELEASExVERSIONx demo $OZ_IP
