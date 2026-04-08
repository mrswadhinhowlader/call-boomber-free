#!/usr/bin/env python3
import os
import time
import subprocess
import threading
import logging
import re

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class NetHunterBulkCaller:
    def __init__(self):
        self.package_name = "com.android.dialer"
    
    def validate_number(self, number):
        """Flexible validation"""
        # Remove spaces/dashes
        clean = re.sub(r'[^\d+]', '', number)
        if clean.startswith('880') and len(clean) == 13:
            return '+88' + clean[3:]
        elif clean.startswith('+880') and len(clean) == 13:
            return clean
        elif clean.startswith('01') and len(clean) == 11:
            return '+8801' + clean[2:]
        elif len(clean) == 13 and clean.startswith('8801'):
            return '+' + clean
        return None
    
    def test_dialer(self):
        try:
            subprocess.run(["am", "start", "-a", "android.intent.action.DIAL"], 
                         timeout=5, check=True, capture_output=True)
            logger.info("✅ Dialer OK")
            return True
        except:
            logger.error("❌ Dialer access denied")
            return False
    
    def clear_dialpad(self):
        subprocess.run(["input", "keyevent", "123"], timeout=1)
        time.sleep(0.3)
    
    def dial_number(self, number):
        self.clear_dialpad()
        subprocess.run(["input", "text", number], timeout=3)
        time.sleep(0.5)
        subprocess.run(["input", "keyevent", "66"], timeout=2)  # CALL
        logger.info(f"📞 Dialing: {number}")
    
    def open_dialer(self):
        subprocess.run([
            "am", "start", "-a", "android.intent.action.DIAL",
            "--ez", "launch_single_user", "false"
        ], timeout=3)
        time.sleep(2)
    
    def hangup(self):
        time.sleep(20)
        subprocess.run(["input", "keyevent", "6"], timeout=2)  # End call
        logger.info("📞 Hangup")
    
    def single_call(self, number):
        self.open_dialer()
        self.dial_number(number)
        hangup_thread = threading.Thread(target=self.hangup)
        hangup_thread.daemon = True
        hangup_thread.start()
        time.sleep(25)
    
    def bulk_attack(self, number, total_calls=50, delay=5):
        logger.info(f"🚀 Bulk Attack: {number} ({total_calls} calls)")
        
        if not self.test_dialer():
            return
        
        for i in range(total_calls):
            self.single_call(number)
            logger.info(f"📊 {i+1}/{total_calls}")
            if i < total_calls - 1:
                time.sleep(delay)

def main():
    print("🔥 NetHunter Bulk Caller v3.0 - FIXED 🔥")
    number = input("📱 Number (+8801xxxxxxxxx / 01xxxxxxxxx): ").strip()
    
    validated = NetHunterBulkCaller().validate_number(number)
    if not validated:
        print("❌ Invalid! Examples:")
        print("   +8801712345678")
        print("   01712345678") 
        print("   8801712345678")
        return
    
    print(f"✅ Validated: {validated}")
    
    total = int(input("🔢 Calls [50]: ") or 50)
    delay = float(input("⏱️ Delay [5s]: ") or 5)
    
    caller = NetHunterBulkCaller()
    caller.bulk_attack(validated, total, delay)
    print("✅ COMPLETE!")

if __name__ == "__main__":
    main()
