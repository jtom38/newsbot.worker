    `# NewsBot Error Codes

## Selenium Errors

### S01

Message: Failed to decode response from marionette
Fixes:
* Make sure that you have more then 2 GB of ram on the system running the container
* Make sure you have enough disk space on the host.  In some cases you might need to run `docker system purge` to free up any lingering layers to get disk space back.
* In the docker-compose.yml, add `shm_size: 3gb` to the container so Selenium can work correctly.