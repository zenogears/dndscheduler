import os

from gettext import gettext as _
from configparser import ConfigParser
import crontab
crontab.CRON_COMMAND = "/var/run/host/usr/bin/crontab"

CONFIG_DIR=f"{os.path.expanduser('~')}/.config/dndscheduler"
CONFIG_FILE=f'sleep.ini'

ALLDAYS = {"MON": _("Monday"),
        "TUE": _("Tuesday"),
        "WED": _("Thirsday"),
        "THU": _("Wednsday"),
        "FRI": _("Friday"),
        "SAT": _("Satuday"),
        "SUN": _("Sunday")
        }

default_cfg = {
    "main": {
        "SHOUR": 23,
        "SMIN": 0,
        "EHOUR": 7,
        "EMIN": 0,
        "MON": False,
        "TUE": False,
        "WED": False,
        "THU": False,
        "FRI": False,
        "SAT": False,
        "SUN": False,
        "SILENT": True,
        "ENABLED": False
    }}

def job_status(data):
    cfg = main_func()
    if eval(cfg["main"][data]):
         return({"status": True, "text": _("On")})
    else:
         return({"status": False, "text": _("Off")})

def ret_days():
    dayson = []
    cfg = main_func()
    workdays = ["MON", "TUE", "WED", "THU", "FRI"]
    weekends = ["SAT","SUN"]
    alldays = workdays.copy()
    alldays.extend(weekends)
    for i in alldays:
        if eval(cfg["main"][i]):
            dayson.append(i)
    if len(dayson) == 7:
        return(_('Everyday'))
    if dayson == workdays:
        return(_('On workdays'))
    if dayson == weekends:
        return(_('On weekends'))
    return(', '.join(dayson) if dayson else _('Never'))
            

def set_status(param, value):
    cfg = load_data()
    cfg["main"][param] = str(value)
    save_data(cfg)
    if eval(cfg["main"]["ENABLED"]) or param.lower() == "enabled":
        create_cron()
    return True

def save_data(cfg):
    with open(f'{CONFIG_DIR}/{CONFIG_FILE}', 'w') as f:
        cfg.write(f)
    
def load_data():
    cfg_default = ConfigParser()
    cfg_default["main"] = default_cfg["main"]
    cfg = ConfigParser()
    cfg.read(f'{CONFIG_DIR}/{CONFIG_FILE}')
    for i in cfg['main']:
        cfg_default["main"][i] = cfg["main"][i]
    return cfg_default

def create_cron():
    cfg = load_data()
    dayofweeks = [x for x in ALLDAYS if cfg["main"][x] == 'True']
    statusDict = {"true": "quiet", "false": "full", "silent": "silent"}
    bannersDict = {"true": "false", "false": "true"}
    status = statusDict[str(cfg["main"]["ENABLED"]).lower()] 
    status_banners = bannersDict[str(cfg["main"]["ENABLED"]).lower()]
    cron = crontab.CronTab(user=True)
    
    job_banners_on = next(cron.find_comment('BannersOn'), False)
    if not job_banners_on:
        command_banners_on = f'gsettings set org.gnome.desktop.notifications show-banners true'
        job_banners_on = cron.new(command=command_banners_on, comment='BannersOn')
    
    job_banners_off = next(cron.find_comment('BannersOff'), False)
    if not job_banners_off:
        command_banners_off = f'gsettings set org.gnome.desktop.notifications show-banners false'
        job_banners_off = cron.new(command=command_banners_off, comment='BannersOff')
        
    job_profile_on = next(cron.find_comment('ProfileOn'), False)
    if not job_profile_on:
        command_profile_on = f'gsettings set org.sigxcpu.feedbackd profile full'
        job_profile_on = cron.new(command=command_profile_on, comment='ProfileOn')
        
    job_profile_off = next(cron.find_comment('ProfileOff'), False)
    if not job_profile_off:
        command_profile_off = f'gsettings set org.sigxcpu.feedbackd profile quiet'
        job_profile_off = cron.new(command=command_profile_off, comment='ProfileOff')
   
    job_banners_on.enable(eval(cfg["main"]["ENABLED"]))
    job_banners_off.enable(eval(cfg["main"]["ENABLED"]))
    
    job_banners_on.hour.on(cfg["main"]["EHOUR"])
    job_banners_on.minute.on(cfg["main"]["EMIN"])
    job_banners_off.hour.on(cfg["main"]["SHOUR"])
    job_banners_off.minute.on(cfg["main"]["SMIN"])
    
    job_profile_on.enable(eval(cfg["main"]["ENABLED"]))
    job_profile_off.enable(eval(cfg["main"]["ENABLED"]))
    
    job_profile_on.hour.on(cfg["main"]["EHOUR"])
    job_profile_on.minute.on(cfg["main"]["EMIN"])
    job_profile_off.hour.on(cfg["main"]["SHOUR"])
    job_profile_off.minute.on(cfg["main"]["SMIN"])

    if dayofweeks:
        job_banners_on.dow.on(*dayofweeks)
        job_banners_off.dow.on(*dayofweeks)
        job_profile_on.dow.on(*dayofweeks)
        job_profile_off.dow.on(*dayofweeks)

    cron.write()

    

def main_func():
    cfg = ConfigParser()
    if not os.path.isdir(CONFIG_DIR):
        os.mkdir(CONFIG_DIR)
    if not os.path.exists(f'{CONFIG_DIR}/{CONFIG_FILE}'):
        cfg["main"] = default_cfg["main"]
        save_data(cfg)
    else:
        cfg = load_data()
    return cfg


if __name__=='__main__':
    main_func()
