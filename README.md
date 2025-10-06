# Home Assistant CalDAV client

Work in progress: this is a simple setup to handle caldav from home assistant via a `service`.

I created the python package [CalDAV-Tasks-API](https://github.com/thiswillbeyourgithub/Caldav-Tasks-API) and wanted to use the `Voice Assistant` to create task. Something like `Okay Nabu. I have to do the dishes` and have it automatically added to my TODO lists. That lists being part of my Nextcloud [Tasks](https://apps.nextcloud.com/apps/tasks) app, which uses caldav so is synced on my phone to [Tasks.org](https://github.com/tasks/tasks/).


## How to

0. Have a Home Assistant instance.
1. Install [HACS](https://www.hacs.xyz/).
2. Use HACS to install [pyscript](https://hacs-pyscript.readthedocs.io/).
3. Have a way to access Home Assistant's files. I use [addon-ssh](https://github.com/hassio-addons/addon-ssh).
4. *Not sure this is needed:* add to `/root/homeassistant/configuration.yaml`:
```yaml
pyscript:
  allow_all_imports: true
  hass_is_global: true
```
5. Create the folder `/config/pyscript`
6. Inside that `pyscript` folder, add the `requirements.txt` file (this will install my package [CalDAV-Tasks-API](https://github.com/thiswillbeyourgithub/Caldav-Tasks-API)). Same for `caldav.py`. You can add a `caldav_password.secret` text file containing your password to avoid hardcoding it in the Web UI.
6. Restart Home Assistant (might not be needed but just to be safe)


### Testing everything works
1. Open Home Assistant > `Settings` > `Automations & scenes` > `Create automation` > `Create new automation` > `Add action` > search for `caldav_add`.
2. Fill in the values then click on the [kebab menu](https://kagi.com/proxy/images?c=_m3km2RjA3G0qleowsZXHZb9NEn0fSsEYIHbKzMDyAFb4nUPIanknmQV_g0rmdCI7DSE22WJPm02DVRa5zIwCPC41lLGjxK0i-EQl5d8ksDTc5kbYP4yXvylNyvKQ4EQWuBHN6v0-pHv23WJZriDSg%3D%3D) then `Run action`.
3. In the Home Assistant shell, `cat /root/homeassistant/homeassistant.log` to look for any issues.


## Notes
- Feedbacks welcome
- I didn't create `intents` or things like that because I use LLMs directly
