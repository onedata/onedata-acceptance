# Setup venv
virtualenv -p /usr/bin/python3 venv
. venv/bin/activate

# Install OnedataRESTFS
pip install fs.onedatarestfs

# If you encounter problems with setuptools, you may need to downgrade the library 
pip install setuptools==81.0.0

# Export necessary OnedataRESTFS arguments as environment variables
OZ_NAME=oz_test;\
until OZ_IP=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $OZ_NAME 2>/dev/null) && [ -n "$OZ_IP" ]; do\
	echo -en "Awaiting the ${OZ_NAME} container...\r"; sleep 1;\
done; echo; \
export OZ_IP
export ACCESS_TOKEN=$(docker exec op_test1 demo-access-token)

# # Finally start Python3 shell
# python3

# We don't run the last command, because the rest will be run as Python script