import time
from pygame import mixer

class Alarm:
    def __init__(self, alarm_file_path: str) -> None:
        self.alarm_file_path = alarm_file_path
    
    def turn_on(self, duration: int = 2) -> None:
        mixer.init() 
        mixer.music.load(self.alarm_file_path)
        mixer.music.play()
        time.sleep(duration)
        mixer.music.stop()


if __name__ == "__main__":
    alarm = Alarm("src\\alarms\\Alarm-ringtone.mp3")
    alarm.turn_on(duration=1)