import speech_recognition as sr
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
import time
import os
from dotenv import load_dotenv
from time import sleep

class SpotifyVoiceController:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        
        load_dotenv()
        
        self.client_id = os.getenv('SPOTIFY_CLIENT_ID')
        self.client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
        self.redirect_uri = "http://localhost:8888/callback"
        self.scope = "user-modify-playback-state user-read-playback-state"
        
        self.auth_manager = SpotifyOAuth(
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=self.redirect_uri,
            scope=self.scope,
            cache_path=".spotify_cache",
            requests_timeout=10
        )
        
        try:
            self.spotify = spotipy.Spotify(
                auth_manager=self.auth_manager,
                requests_timeout=10,
                retries=3,
                status_forcelist=(429, 500, 502, 503, 504)
            )
            self.spotify.current_user()
            print("Successfully connected to Spotify!")
            
            self.active_device_id = None
            
        except Exception as e:
            print(f"Error connecting to Spotify: {e}")
            raise

        self.commands = {
            "play": self.play_music,
            "pause": self.pause_music,
            "next": self.next_track,
            "previous": self.previous_track,
            "volume up": self.volume_up,
            "volume down": self.volume_down
        }
    
    def get_available_devices(self):
        max_retries = 3
        retry_delay = 1
        
        for attempt in range(max_retries):
            try:
                devices = self.spotify.devices()
                if devices and 'devices' in devices:
                    return devices['devices']
                sleep(retry_delay)
            except Exception as e:
                print(f"Attempt {attempt + 1}/{max_retries} failed to get devices: {e}")
                if attempt < max_retries - 1:
                    sleep(retry_delay)
                    retry_delay *= 2
                continue
        return []

    def select_device(self, devices):
        if not devices:
            return None
            
        if self.active_device_id:
            for device in devices:
                if device['id'] == self.active_device_id:
                    return device['id']
        
        active_devices = [d for d in devices if d.get('is_active')]
        if active_devices:
            self.active_device_id = active_devices[0]['id']
            return self.active_device_id
            
        computer_devices = [d for d in devices if d['type'].lower() == 'computer']
        if computer_devices:
            self.active_device_id = computer_devices[0]['id']
            return self.active_device_id
            
        self.active_device_id = devices[0]['id']
        return self.active_device_id

    def activate_device(self, device_id):
        if not device_id:
            return False
            
        max_retries = 3
        retry_delay = 1
        
        for attempt in range(max_retries):
            try:
                self.spotify.transfer_playback(device_id, force_play=False)
                print(f"Successfully activated device!")
                return True
            except spotipy.exceptions.SpotifyException as e:
                if e.http_status == 429:
                    retry_after = int(e.headers.get('Retry-After', retry_delay))
                    print(f"Rate limited. Waiting {retry_after} seconds...")
                    sleep(retry_after)
                else:
                    print(f"Attempt {attempt + 1}/{max_retries} failed: {e}")
                    if attempt < max_retries - 1:
                        sleep(retry_delay)
                        retry_delay *= 2
        return False

    def ensure_active_device(self):
        devices = self.get_available_devices()
        
        if not devices:
            print("No Spotify devices found. Please open Spotify on any device.")
            return False
            
        print("\nAvailable devices:")
        for device in devices:
            print(f"- {device['name']} ({device['type']})")
        
        device_id = self.select_device(devices)
        if device_id:
            return self.activate_device(device_id)
        return False

    def execute_with_retry(self, func, *args, **kwargs):
        max_retries = 3
        retry_delay = 1
        
        for attempt in range(max_retries):
            try:
                return func(*args, **kwargs)
            except spotipy.exceptions.SpotifyException as e:
                if e.http_status == 429:
                    retry_after = int(e.headers.get('Retry-After', retry_delay))
                    print(f"Rate limited. Waiting {retry_after} seconds...")
                    sleep(retry_after)
                else:
                    print(f"Attempt {attempt + 1}/{max_retries} failed: {e}")
                    if attempt < max_retries - 1:
                        sleep(retry_delay)
                        retry_delay *= 2
                    else:
                        raise
        return None

    def listen_for_command(self):
        with sr.Microphone() as source:
            print("\nListening for command...")
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            try:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=3)
                command = self.recognizer.recognize_google(audio).lower()
                print(f"Recognized command: {command}")
                return command
            except sr.UnknownValueError:
                print("Could not understand audio")
                return None
            except sr.RequestError as e:
                print(f"Could not request results; {e}")
                return None
            except Exception as e:
                print(f"Error: {e}")
                return None

    def play_music(self):
        try:
            if not self.active_device_id:
                self.ensure_active_device()
            return self.execute_with_retry(self.spotify.start_playback)
        except Exception as e:
            print(f"Error playing music: {e}")
            return False

    def pause_music(self):
        try:
            if not self.active_device_id:
                self.ensure_active_device()
            return self.execute_with_retry(self.spotify.pause_playback)
        except Exception as e:
            print(f"Error pausing music: {e}")
            return False

    def next_track(self):
        try:
            if not self.active_device_id:
                self.ensure_active_device()
            return self.execute_with_retry(self.spotify.next_track)
        except Exception as e:
            print(f"Error skipping track: {e}")
            return False

    def previous_track(self):
        try:
            if not self.active_device_id:
                self.ensure_active_device()
            return self.execute_with_retry(self.spotify.previous_track)
        except Exception as e:
            print(f"Error going to previous track: {e}")
            return False

    def volume_up(self):
        try:
            if not self.active_device_id:
                self.ensure_active_device()
            current = self.execute_with_retry(self.spotify.current_playback)
            if current and 'device' in current:
                current_volume = current['device']['volume_percent']
                new_volume = min(100, current_volume + 10)
                return self.execute_with_retry(self.spotify.volume, new_volume)
        except Exception as e:
            print(f"Error increasing volume: {e}")
            return False

    def volume_down(self):
        try:
            if not self.active_device_id:
                self.ensure_active_device()
            current = self.execute_with_retry(self.spotify.current_playback)
            if current and 'device' in current:
                current_volume = current['device']['volume_percent']
                new_volume = max(0, current_volume - 10)
                return self.execute_with_retry(self.spotify.volume, new_volume)
        except Exception as e:
            print(f"Error decreasing volume: {e}")
            return False

    def process_command(self, command):
        if not command:
            return
        
        for key, func in self.commands.items():
            if key in command:
                return func()
        
        print("Command not recognized")
        return False

    def run(self):
        print("\nStarting Spotify Voice Controller...")
        print("Available commands:", list(self.commands.keys()))
        
        sleep(1)
        self.ensure_active_device()
        
        while True:
            try:
                command = self.listen_for_command()
                if command:
                    self.process_command(command)
                sleep(0.1)
            except KeyboardInterrupt:
                print("\nStopping voice controller...")
                break
            except Exception as e:
                print(f"An error occurred: {e}")
                print("Restarting voice controller...")
                sleep(2)

if __name__ == "__main__":
    try:
        controller = SpotifyVoiceController()
        controller.run()
    except Exception as e:
        print(f"Failed to start voice controller: {e}")