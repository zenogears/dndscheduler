import os

from crontab import CronTab

def main():
    cfg = {
    "main": {
        "HOUR": 22,
        "MINUTE": 45,
        "HERO": 7
    }}
    return cfg


if __name__=='__main__':
    main()
