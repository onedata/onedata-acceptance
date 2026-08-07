# Setup venv
virtualenv -p /usr/bin/python3 venv
. venv/bin/activate

# Install OnedataRESTFS
pip install fs.onedatarestfs

# If you encounter problems with setuptools, you may need to downgrade the library 
pip install setuptools==81.0.0

# Export necessary OnedataRESTFS arguments as environment variables
export OZ_IP=$(docker inspect --format '{{ .NetworkSettings.IPAddress }}' oz_test)
export ACCESS_TOKEN=$(docker exec op_test1 demo-access-token)

# # Finally start Python3 shell
# python3

# We don't run the last command, because the rest will be run as Python script