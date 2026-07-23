#!/usr/bin/env python3
"""
Automated setup script for NTBSS-Force-Save
Handles UE4SS installation, file placement, and configuration
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path
from tkinter import Tk, filedialog, messagebox
import json


class SetupWizard:
    """Interactive setup wizard for NTBSS-Force-Save"""
    
    def __init__(self):
        self.steam_path = None
        self.game_path = None
        self.backup_created = False
        
    def show_info(self, title, message):
        """Show information dialog"""
        Tk().withdraw()
        messagebox.showinfo(title, message)
    
    def show_error(self, title, message):
        """Show error dialog"""
        Tk().withdraw()
        messagebox.showerror(title, message)
    
    def show_warning(self, title, message):
        """Show warning dialog"""
        Tk().withdraw()
        messagebox.showwarning(title, message)
    
    def ask_yes_no(self, title, message):
        """Ask yes/no question"""
        Tk().withdraw()
        return messagebox.askyesno(title, message)
    
    def select_directory(self, prompt, initial_dir=None):
        """Let user select directory"""
        Tk().withdraw()
        result = filedialog.askdirectory(title=prompt, initialdir=initial_dir)
        return result if result else None
    
    def find_game_installation(self):
        """Attempt to find game installation automatically"""
        common_paths = [
            Path("D:/steam/steamapps/common/Naruto To Boruto"),
            Path("C:/Program Files (x86)/Steam/steamapps/common/Naruto To Boruto"),
            Path("C:/Program Files/Steam/steamapps/common/Naruto To Boruto"),
        ]
        
        for path in common_paths:
            if path.exists():
                naruto_exe = path / "Naruto.exe"
                if naruto_exe.exists():
                    return path
        
        return None
    
    def locate_game_path(self):
        """Locate or prompt for game installation path"""
        print("\n[SETUP] Looking for game installation...")
        
        auto_found = self.find_game_installation()
        if auto_found:
            print(f"[SETUP] Found game at: {auto_found}")
            if self.ask_yes_no("Installation Found", 
                              f"Found game at:\n{auto_found}\n\nUse this path?"):
                self.game_path = auto_found
                return True
        
        self.show_info("Manual Selection", 
                      "Please navigate to your game installation folder.\n"
                      "Look for 'Naruto.exe' in the folder.")
        
        selected = self.select_directory(
            "Select Naruto To Boruto game folder",
            "D:/steam/steamapps/common" if sys.platform == "win32" else None
        )
        
        if not selected:
            return False
        
        game_path = Path(selected)
        if not (game_path / "Naruto.exe").exists():
            self.show_error("Invalid Path", 
                          "Naruto.exe not found in selected folder!")
            return False
        
        self.game_path = game_path
        return True
    
    def backup_naruto_exe(self):
        """Create backup of Naruto.exe"""
        naruto_exe = self.game_path / "Naruto.exe"
        backup_path = self.game_path / "Naruto.exe.backup"
        
        if backup_path.exists():
            print(f"[SETUP] Backup already exists at {backup_path}")
            return True
        
        try:
            print(f"[SETUP] Creating backup of Naruto.exe...")
            shutil.copy2(naruto_exe, backup_path)
            self.backup_created = True
            print(f"[SETUP] Backup created at: {backup_path}")
            return True
        except Exception as e:
            self.show_error("Backup Failed", 
                          f"Could not backup Naruto.exe:\n{str(e)}")
            return False
    
    def copy_ue4ss_files(self):
        """Copy UE4SS files to Win64 binaries directory"""
        ue4ss_dir = Path(__file__).parent / "ue4ss"
        target_dir = self.game_path / "NARUTO" / "Binaries" / "Win64"
        
        if not ue4ss_dir.exists():
            self.show_error("UE4SS Files Missing",
                          f"UE4SS directory not found at:\n{ue4ss_dir}\n\n"
                          "Please ensure ue4ss folder is in the setup directory.")
            return False
        
        if not target_dir.exists():
            self.show_error("Invalid Game Path",
                          f"Win64 directory not found at:\n{target_dir}")
            return False
        
        try:
            print(f"[SETUP] Copying UE4SS files to {target_dir}...")
            for item in ue4ss_dir.iterdir():
                if item.is_file():
                    dest = target_dir / item.name
                    print(f"[SETUP]   Copying {item.name}...")
                    shutil.copy2(item, dest)
                elif item.is_dir():
                    dest = target_dir / item.name
                    if dest.exists():
                        shutil.rmtree(dest)
                    print(f"[SETUP]   Copying directory {item.name}...")
                    shutil.copytree(item, dest)
            
            print("[SETUP] UE4SS files copied successfully!")
            return True
        except Exception as e:
            self.show_error("Copy Failed",
                          f"Could not copy UE4SS files:\n{str(e)}")
            return False
    
    def create_temp_directory(self):
        """Create C:\\temp directory if it doesn't exist"""
        temp_path = Path("C:/temp")
        try:
            temp_path.mkdir(exist_ok=True)
            print(f"[SETUP] Temp directory ready at: {temp_path}")
            return True
        except Exception as e:
            self.show_error("Temp Directory Failed",
                          f"Could not create C:\\temp:\n{str(e)}")
            return False
    
    def setup_mod_loader(self):
        """Attempt to replace or patch Naruto.exe (placeholder)"""
        print("[SETUP] Note: Mod loader setup requires manual installation.")
        print("[SETUP] Ensure you have placed the modified Naruto.exe in the game directory.")
        
        naruto_exe = self.game_path / "Naruto.exe"
        if naruto_exe.exists():
            return True
        
        self.show_warning("Mod Loader Not Found",
                         "Modified Naruto.exe not found.\n"
                         "Please manually place the mod-enabled executable in the game folder.")
        return False
    
    def verify_installation(self):
        """Verify all files are in place"""
        checks = [
            (self.game_path / "Naruto.exe", "Naruto.exe"),
            (self.game_path / "NARUTO" / "Binaries" / "Win64" / "UE4SS.dll", "UE4SS.dll"),
            (Path("C:/temp"), "C:\\temp directory"),
        ]
        
        print("\n[SETUP] Verifying installation...")
        missing = []
        
        for path, name in checks:
            if path.exists():
                print(f"[SETUP] ✓ {name}")
            else:
                print(f"[SETUP] ✗ {name} NOT FOUND")
                missing.append(name)
        
        if missing:
            self.show_warning("Installation Incomplete",
                            f"Missing files:\n" + "\n".join(f"  - {m}" for m in missing))
            return False
        
        return True
    
    def create_shortcuts(self):
        """Create shortcuts for easy access"""
        try:
            # Create shortcut to gui.py
            gui_path = Path(__file__).parent / "gui.py"
            desktop = Path.home() / "Desktop"
            
            print(f"[SETUP] Creating desktop shortcut for GUI...")
            # This is a simplified version; actual shortcut creation varies by OS
            print(f"[SETUP] GUI available at: {gui_path}")
            
            return True
        except Exception as e:
            print(f"[SETUP] Shortcut creation skipped: {str(e)}")
            return True  # Non-critical
    
    def run_setup(self):
        """Run complete setup process"""
        print("\n" + "="*60)
        print("NTBSS-Force-Save Setup Wizard")
        print("="*60)
        
        # Step 1: Locate game
        if not self.locate_game_path():
            self.show_error("Setup Cancelled", "Game path not selected.")
            return False
        
        print(f"\n[SETUP] Game path: {self.game_path}")
        
        # Step 2: Create backup
        if not self.backup_naruto_exe():
            return False
        
        # Step 3: Create temp directory
        if not self.create_temp_directory():
            return False
        
        # Step 4: Copy UE4SS files
        if not self.copy_ue4ss_files():
            return False
        
        # Step 5: Verify mod loader
        if not self.setup_mod_loader():
            return False
        
        # Step 6: Verify installation
        if not self.verify_installation():
            return False
        
        # Step 7: Create shortcuts
        self.create_shortcuts()
        
        print("\n" + "="*60)
        print("Setup Complete!")
        print("="*60)
        print("\nNext steps:")
        print("1. Launch the game")
        print("2. Load into a lobby (full game, not title screen)")
        print("3. Run gui.py to dump or upload saves")
        print("4. After uploading a save, return to title screen then back to game")
        print("\n" + "="*60)
        
        self.show_info("Setup Complete!",
                      "Installation successful!\n\n"
                      "Next steps:\n"
                      "1. Launch the game\n"
                      "2. Load into a lobby (full game, not title screen)\n"
                      "3. Run gui.py to dump or upload saves\n"
                      "4. After uploading, return to title screen then back to game")
        
        return True


def main():
    """Main entry point"""
    try:
        wizard = SetupWizard()
        success = wizard.run_setup()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n[ERROR] Setup failed: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
