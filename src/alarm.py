import time
from pygame import mixer

class Alarm:
    def __init__(self, alarm_file_path: str) -> None:
        """
            Wrapper for playing sound within certain duration.
        """
        self.alarm_file_path = alarm_file_path
    
    def turn_on(self, duration: int = 0) -> None:
        """
            Turn on alarm specified specified when the was created.

            Params:
                duration (int): sleep duration in seconds.
        """
        mixer.init() 
        mixer.music.load(self.alarm_file_path)
        mixer.music.play()
        time.sleep(duration)
        mixer.music.stop()


if __name__ == "__main__":
    alarm = Alarm("src\\alarms\\Alarm-ringtone.mp3")
    alarm.turn_on(duration=1)