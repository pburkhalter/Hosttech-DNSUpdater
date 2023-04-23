# Hosttech DNS-Updater
A very simple updater using the Hosttech-API. Could be useful if you need to update your dynamic IP at home. There's also a Dockerfile included. 

## Usage

### Docker CLI
1. Create a volume to hold the config/token:<br />
`docker volume create [NAME OF THE VOLUME]`
2. Switch into the directory and build the docker-image:<br /> 
`docker build -t [NAME OF THE IMAGE] -f Dockerfile .`
3. Run the container: <br />
`docker run -v [NAME OF THE VOLUME]:/config` <br /> 
`--network host ` <br /> 
`-e TZ=Europe/Zurich` <br /> 
`-e HTUPD_DOMAIN='[NAME OF THE DOMAIN]'` <br /> 
`-e HTUPD_SUBDOMAIN='[NAME OF THE SUBDOMAIN]'` <br /> 
`-e HTUPD_RECORD=[YOUR HOSTTECH RECORD ID]` <br /> 
`-e HTUPD_TOKEN='[YOUR HOSTTECH TOKEN]'` <br /> 
`-e HTUPD_URL='https://api.ns1.hosttech.eu/api/user/v1/zones/'`  
`-e HTUPD_TTL=10800` <br /> 
`-it [NAME OF THE CONTAINER]`


### Portainer
1. Get the code, switch into the directory and create a tar-archive: <br />
`tar -cf hosttech-updater.tar *`
2.  Build a new Image under "Images". Upload the tar-archive to portainer and prefix the container with "localhost" for local usage, for example: <br />
`localhost/hosttech_updater`
3. Create a new Volume under "Volumes" to hold the config/token, for example: <br /> 
`hosttech_config`
4. Create a new Container
   - Choose the created image from local repository
   - Set the networking to `host`
   - Map the previously created Volume to `/config`
   - Set the restart policy to `Unless stopped`
   - Set the required ENV-Variables...:<br />

       `HTUPD_TTL=10800`<br />
       `HTUPD_URL=https://api.ns1.hosttech.eu/api/user/v1/zones/` <br />
       `HTUPD_TOKEN= [YOUR HOSTTECH TOKEN HERE]` <br />
       `HTUPD_RECORD=[YOUR HOSTTECH RECORD HERE]` <br />
       `HTUPD_DOMAIN=[YOUR DOMAIN HERE]` <br />
       `HTUPD_SUBDOMAIN=[YOUR SUBDOMAIN HERE]` <br />
       `TZ=Europe/Zurich`<br />
5. Deploy your container! By default, it will refresh the IP every 30min (defined in the crontab-file)

### Swagger
To get the Record-ID and/or verify the service is running correctly, you can use Swagger. 
Just get the Token via the Hosttech-WebUI and use it to authorize your requests to play around with the API :<br />
https://api.ns1.hosttech.eu/api/documentation/

## Licensing
This project is licensed under the terms of the MIT license.
