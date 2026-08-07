docker run --rm -i -d --name oz_test onedata/onezone:xRELEASExVERSIONx demo
OZ_IP=$(docker inspect --format '{{ .NetworkSettings.IPAddress }}' oz_test)
docker run --rm -i -d --name op_test1 onedata/oneprovider:xRELEASExVERSIONx demo $OZ_IP
OP_IP=$(docker inspect --format '{{ .NetworkSettings.IPAddress }}' op_test1)
docker exec op_test1 await-demo
ACCESS_TOKEN=$(docker exec op_test1 demo-access-token)
DEMO_SPACE_ID="cb274b2b8bb1750d9be37dd4a3eb7014chb175"
FILE_NAME="test$RANDOM.txt"
RESULT=$(curl -ks -H "x-auth-token: $ACCESS_TOKEN" \
    -X POST "https://$OP_IP/api/v3/oneprovider/data/$DEMO_SPACE_ID/children?name=$FILE_NAME" \
    -H "Content-Type: application/octet-stream" -d "hello world\n")
# below JSON parsing method is definitely not elegant, 
# but bear with us since we want a portable example not depending on 'jq'
FILE_ID=$(echo $RESULT | cut -d':' -f2 | tr -d '"}')
echo "All done! Created a file called \"$FILE_NAME\" in the demo space; view it here:"
echo ""
echo "https://$OZ_IP/#/action/file/show/$FILE_ID"