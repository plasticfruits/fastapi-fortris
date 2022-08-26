# Technical Python Challenge

## API
* The API can be accessed here: [http://167.71.42.226](http://167.71.42.226)

## Documentation & Testing
Please refer to [http://138.68.75.94/docs](http://167.71.42.226/docs)

## Run Locally
### A. Using Docker (recommended)
If you are new to Docker, click [here](https://docs.docker.com/get-started/) to install and get started
1. Pull docker image from hub `docker pull plasticfruits/fortris-app`
2. Run container `docker run --name mycontainer -p 80:80 plasticfruits/fortris-app`
3. Open the URL where the app is being served [http://0.0.0.0:80]
4. Exit with `ctrl + c`

### B. Using Virtual Environment (e.g. Conda)
1. cd into folder `cd fastapi-fortris`
2. Create new conda environment `conda create --name fruity-env --file requirements.txt`
3. Activate environment `conda activate fruity-env`
4. cd to app folder `cd app`
5. Start the live server `uvicorn main:app --reload`
6. Open URL where app is being served (e.g. [http://127.0.0.1:8000])

## Notes
- Google Trends API seem not returning results for last three days, therefore Task 5 returns only 4 data objects.
- No need to use **docker-compose** as only 1 container being used

## Todos
- Add exception handling to endpoints
- Investigate why Google Trends API not passing last 3 days
- Better documentation on functions
- Remove unused libraries
- Read more about async calls & FastAPI :D
