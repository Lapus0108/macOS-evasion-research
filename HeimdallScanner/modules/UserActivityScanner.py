import os
import objc
import json
import sqlite3
import plistlib
from utils import *
from CoreServices import MDQueryCreate, MDQueryExecute, MDQueryGetResultCount


class UserActivityScanner:
    BOOKMARKS_THRESHOLD = 5
    HISTORY_THRESHOLD = 40
    COMMON_APPS_THRESHOLD = 4

    RECENT_DOCS_THRESHOLD = 3
    RECENT_DOCS_PERIOD_DAYS = 5

    DESKTOP_ITEMS_THRESHOLD = 4
    DOWNLOADS_ITEMS_THRESHOLD = 5

    def __init__(self):
        self.user_home_path = os.path.expanduser("~")

    def scan(self):
        common_directories_files = self.scan_common_directories()
        desktop_entries = common_directories_files['desktop']['files'] + common_directories_files['desktop']['directories']
        downloads_entries = common_directories_files['downloads']['files'] + common_directories_files['downloads']['directories']
        recently_opened_files = self.check_recent_documents()
        
        total_bookmarks = self.check_browsers_bookmarks()
        total_history_entries = self.checks_browsers_history()

        common_apps_installed = self.check_common_applications()

        return [
            {
                'label': 'Browser Bookmarks',
                'result': f'{total_bookmarks} bookmarks for all browsers',
                'vm_detected': total_bookmarks < self.BOOKMARKS_THRESHOLD,
                'status': 'success'
            },
            {
                'label': 'Browser History',
                'result': f'{total_history_entries} entries for all browsers',
                'vm_detected': total_history_entries < self.HISTORY_THRESHOLD,
                'status': 'success'
            },
            {
                'label': 'Recently opened files & documents',
                'result': f'{recently_opened_files} files/documents opened in the last {self.RECENT_DOCS_PERIOD_DAYS} days.',
                'vm_detected': recently_opened_files < self.RECENT_DOCS_THRESHOLD,
                'status': 'success'
            },
            {
                'label': 'Number of items on Desktop',
                'result': f'The user has only {desktop_entries} {'item' if desktop_entries == 1 else 'items'} on Desktop.',
                'vm_detected': desktop_entries < self.DESKTOP_ITEMS_THRESHOLD,
                'status': 'success' 
            },
            {
                'label': 'Downloads',
                'result': f"The user has only {downloads_entries} {'item' if downloads_entries == 1 else 'items'} in the Downloads folder.",
                'vm_detected': downloads_entries < self.DOWNLOADS_ITEMS_THRESHOLD,
                'status': 'success' 
            },
            {
                'label': 'Common Applications',
                'result': f"The user has {common_apps_installed} {'application' if common_apps_installed == 1 else 'applications'} installed from a list of commonly found apps.",
                'vm_detected': common_apps_installed < self.COMMON_APPS_THRESHOLD,
                'status': 'success' 
            }
        ]

        
    def scan_common_directories(self):
        directories = [
            os.path.join(self.user_home_path, "Desktop"),
            os.path.join(self.user_home_path, "Documents"),
            os.path.join(self.user_home_path, "Downloads")
        ]

        results = {}
        for dir in directories:
            dir_key = os.path.basename(dir).lower()
            results[dir_key] = self.scan_directory(dir)

        return results

    def scan_directory(self, dir_path: str):
        if not os.path.exists(dir_path):
            return 0
        
        total_files = 0
        total_dirs = 0
        for item in os.listdir(dir_path):
            full_path = os.path.join(dir_path, item)
            if os.path.isfile(full_path):
                total_files +=1 
            elif os.path.isdir(full_path):
                total_dirs += 1
        
        return {
            'files': total_files,
            'directories': total_dirs
        }

    def check_browsers_bookmarks(self):
        chrome_bkms = self.check_chrome_bookmarks()
        brave_bkms = self.check_brave_bookmarks()
        safari_bkms = self.check_safari_bookmarks()
        firefox_bkms = self.check_firefox_bookmarks()

        return chrome_bkms + brave_bkms + safari_bkms + firefox_bkms

    def checks_browsers_history(self):
        chrome_entries = self.check_chrome_history()
        brave_entries = self.check_brave_history()
        safari_entries = self.check_safari_history()
        firefox_entries = self.check_firefox_history()

        return chrome_entries + brave_entries + safari_entries + firefox_entries

    def check_recent_documents(self):
        interval_seconds = self.RECENT_DOCS_PERIOD_DAYS * 24 * 60 * 60

        query_string = f'(kMDItemLastUsedDate >= $time.now(-{interval_seconds})) && (kMDItemContentType != "public.folder") && (kMDItemContentType != "com.apple.application-bundle")'
        
        query = MDQueryCreate(None, query_string, None, None)
        if query and MDQueryExecute(query, objc.YES):
            count = MDQueryGetResultCount(query)
            # file_paths = [MDQueryGetResultAtIndex(query, i) for i in range(count)]
            # for path in file_paths:
            #     print(MDItemCopyAttribute(path, "kMDItemPath"))
            return count
        
        return 0
    
    def check_chrome_bookmarks(self):
        chrome_bookmarks_file = os.path.join(self.user_home_path, "Library/Application Support/Google/Chrome/Default/Bookmarks")
        if not os.path.isfile(chrome_bookmarks_file):
            print(f"[Chrome] Bookmarks file not found: {chrome_bookmarks_file}")
            return 0
        
        with open(chrome_bookmarks_file, "r", encoding="utf-8") as bookmarks_file:
            bookmarks = json.load(bookmarks_file)
        
        urls = []
        def extract_bookmarks(data):
            if isinstance(data, dict):
                if data.get("type") == "url":
                    urls.append(f"{data['name']} -> {data['url']}")
                for key in data:
                    extract_bookmarks(data[key])
            elif isinstance(data, list):
                for item in data:
                    extract_bookmarks(item)
        
        extract_bookmarks(bookmarks.get("roots", {}))
        return len(urls)

    def check_brave_bookmarks(self):
        brave_bookmarks_file = os.path.join(self.user_home_path, "Library/Application Support/BraveSoftware/Brave-Browser/Default/Bookmarks")
        if not os.path.isfile(brave_bookmarks_file):
            print("[Brave] Bookmarks file not found.")
            return 0
        
        with open(brave_bookmarks_file, "r", encoding="utf-8") as bookmarks_file:
            bookmarks = json.load(bookmarks_file)
        
        urls = []
        def extract_bookmarks(data):
            if isinstance(data, dict):
                if data.get("type") == "url":
                    urls.append(f"{data['name']} -> {data['url']}")
                for key in data:
                    extract_bookmarks(data[key])
            elif isinstance(data, list):
                for item in data:
                    extract_bookmarks(item)
        
        extract_bookmarks(bookmarks.get("roots", {}))        
        return len(urls)

    def check_safari_bookmarks(self):
        safari_bookmarks_file = os.path.join(self.user_home_path, "Library/Safari/Bookmarks.plist")
        if not os.path.isfile(safari_bookmarks_file):
            print(f"[Safari] Bookmarks file not found: {safari_bookmarks_file}")
            return 0
        
        try:
            with open(safari_bookmarks_file, "rb") as f:
                bookmarks = plistlib.load(f)
            
            urls = []
            def extract_bookmarks(data):
                if isinstance(data, dict):
                    if "URLString" in data:
                        title = data.get("URIDictionary", {}).get("title", "No Title")
                        urls.append(f"{title} -> {data['URLString']}")
                    for key in data:
                        extract_bookmarks(data[key])
                elif isinstance(data, list):
                    for item in data:
                        extract_bookmarks(item)
            
            extract_bookmarks(bookmarks)
            return len(urls)
        except PermissionError:
            print("[Safari] No permissions to open database file. Please run the file directly from the Terminal.")
            return 0
    
    def check_firefox_bookmarks(self):
        firefox_profiles_dir = os.path.join(self.user_home_path, "Library/Application Support/Firefox/Profiles")
        if not os.path.isdir(firefox_profiles_dir):
            print("[Firefox] Not found on the system.")
            return 0
        
        profiles = []
        for profile in os.listdir(firefox_profiles_dir):
            full_path = os.path.join(firefox_profiles_dir, profile)
            if full_path.endswith(".default-release"):
                profiles.append(full_path)

        if len(profiles) == 0:
            print("[Firefox] No profiles found.")
            return 0
        
        query = """
            SELECT moz_bookmarks.title || ' -> ' || moz_places.url 
            FROM moz_bookmarks 
            JOIN moz_places ON moz_bookmarks.fk = moz_places.id 
            WHERE moz_places.url IS NOT NULL 
            AND moz_bookmarks.title IS NOT NULL 
            AND moz_places.url NOT LIKE '%mozilla%' 
            ORDER BY moz_bookmarks.dateAdded DESC;
        """
        
        total_bookmarks_all_profiles = 0
        for profile in profiles:
            db_file = os.path.join(profile, "places.sqlite")
            if not os.path.isfile(db_file):
                print(f"[Firefox] No places.sqlite file found for profile {os.path.basename(profile)}, skipping...")
                continue
            
            conn = sqlite3.connect(db_file)
            cursor = conn.cursor()
            
            cursor.execute(query)
            bookmarks = cursor.fetchall()
            conn.close()
            
            total_bookmarks_all_profiles += len(bookmarks)
        
        return total_bookmarks_all_profiles

    def check_safari_history(self, period_days=7):
        safari_history_db = os.path.join(os.path.expanduser("~"), "Library/Safari/History.db")
        if not os.path.isfile(safari_history_db):
            print("[Safari] History file not found.")
            return 0

        try:
            apple_epoch_offset = 978307200
            query = f"""
                SELECT
                    datetime(visit_time + {apple_epoch_offset}, 'unixepoch') AS visit_date,
                    url,
                    title
                FROM history_visits
                JOIN history_items ON history_items.id = history_visits.history_item
                WHERE visit_time >= strftime('%s', 'now', '-{period_days} days') - {apple_epoch_offset}
                ORDER BY visit_date DESC;
            """
            
            conn = sqlite3.connect(safari_history_db)
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            conn.close()

            return len(rows)
        except sqlite3.OperationalError:
            print("[Safari] No permissions to open History file. Please run the file directly from the Terminal.")
            return 0
    
    def check_brave_history(self, period_days=7):
        brave_history_db = os.path.join(self.user_home_path, "Library/Application Support/BraveSoftware/Brave-Browser/Default/History")
        if not os.path.isfile(brave_history_db):
            print("[Brave] History file not found.")
            return 0

        query = f"""
            SELECT
                datetime(visit_time / 1000000, 'unixepoch') AS visit_date,
                urls.url,
                urls.title
            FROM visits
            JOIN urls ON urls.id = visits.url
            WHERE visit_time >= (strftime('%s', 'now', '-{period_days} days') * 1000000)
            ORDER BY visit_date DESC;
        """

        try:
            conn = sqlite3.connect(brave_history_db)
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            conn.close()
        except sqlite3.OperationalError as e:
            print(f"[Brave History] sqlite query error: " + str(e))
            return 0

        return len(rows)

    def check_chrome_history(self, period_days=7):
        kill_process("Google Chrome")
        chrome_history_db = os.path.join(self.user_home_path, "Library/Application Support/Google/Chrome/Default/History")
        if not os.path.isfile(chrome_history_db):
            print("[Chrome] History file not found.")
            return 0

        chrome_epoch_offset = 11644473600
        query = f"""
            SELECT 
                datetime((visit_time / 1000000) - {chrome_epoch_offset}, 'unixepoch') AS visit_date, 
                urls.url, 
                urls.title 
            FROM visits 
            JOIN urls ON urls.id = visits.url 
            WHERE visit_time >= ((strftime('%s', 'now', '-{period_days} days') + {chrome_epoch_offset}) * 1000000) 
            ORDER BY visit_date ASC;
        """

        try:
            conn = sqlite3.connect(chrome_history_db)
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            conn.close()
        except sqlite3.OperationalError as e:
            print(f"[Chrome History] sqlite query error: " + str(e))
            return 0

        return len(rows)

    def check_firefox_history(self, period_days=7):
        kill_process("firefox")
        firefox_profiles_dir = os.path.join(self.user_home_path, "Library/Application Support/Firefox/Profiles")
        if not os.path.isdir(firefox_profiles_dir):
            print("[Firefox] Firefox profiles directory not found.")
            return 0

        profiles = []
        for profile in os.listdir(firefox_profiles_dir):
            full_path = os.path.join(firefox_profiles_dir, profile)
            if full_path.endswith(".default-release"):
                profiles.append(full_path)

        query = f"""
            SELECT
                datetime(visit_date/1000000, 'unixepoch') AS visit_date,
                url,
                title
            FROM moz_historyvisits
            JOIN moz_places ON moz_places.id = moz_historyvisits.place_id
            WHERE visit_date >= (strftime('%s', 'now', '-{period_days} days') * 1000000)
            ORDER BY visit_date DESC;
        """

        total_history_entries = 0
        for profile in profiles:
            firefox_history_db = os.path.join(firefox_profiles_dir, profile, "places.sqlite")

            if not os.path.isfile(firefox_history_db):
                print(f"[Firefox] No places.sqlite file found for profile {os.path.basename(profile)}, skipping...")
                continue

            conn = sqlite3.connect(firefox_history_db)
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            conn.close()

            total_history_entries += len(rows)

        return total_history_entries
    
    def check_common_applications(self):
        installed_apps = []
        for app in os.listdir("/Applications"):
            if app.endswith(".app"):
                installed_apps.append(app[:-4])
        
        installed_apps = set(installed_apps)

        COMMON_APPS = {
            "Firefox", 
            "Google Chrome", 
            "Brave Browser",
            "Microsoft Word", 
            "Microsoft Excel", 
            "Microsoft PowerPoint", 
            "Microsoft Outlook", 
            "Notion", 
            "Evernote", 
            "OneNote", 
            "Obsidian",
            "LibreOffice",
            "Slack", 
            "zoom.us", 
            "Microsoft Teams", 
            "Skype", 
            "Webex",
            "Discord",
            "OneDrive",
            "Thunderbird",
            "Spotify",
            "PyCharm",
            "Visual Studio Code", 
            "Sublime Text", 
            "Eclipse", 
            "IntelliJ IDEA",
            "Final Cut Pro"
        }

        common_apps = installed_apps.intersection(COMMON_APPS)
        return len(list(common_apps))
        