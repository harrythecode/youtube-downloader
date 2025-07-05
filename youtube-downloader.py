import yt_dlp
import os
import gettext
import locale

# --- i18n Setup ---
APP_NAME = "messages"
LOCALE_DIR = os.path.join(os.path.dirname(__file__), 'locales')

# Global variable to store current language
current_language = None

def setup_language(lang_code=None):
    """
    Set up gettext translation based on language code or system default.
    """
    global current_language
    
    try:
        if lang_code:
            # Use specified language
            current_language = lang_code
            t = gettext.translation(APP_NAME, localedir=LOCALE_DIR, languages=[lang_code], fallback=True)
            _ = t.gettext
        else:
            # Use system's default language
            lang, encoding = locale.getdefaultlocale()
            if lang:
                lang_code = lang.split('_')[0]
                current_language = lang_code
                t = gettext.translation(APP_NAME, localedir=LOCALE_DIR, languages=[lang_code], fallback=True)
                _ = t.gettext
            else:
                # Fallback to English if language cannot be detected
                current_language = 'en'
                _ = gettext.gettext
    except FileNotFoundError:
        # Fallback to English if no translation files are found
        current_language = 'en'
        _ = gettext.gettext
    
    return _

# Initialize with system default language
_ = setup_language()
# --------------------

def show_help():
    """
    Display help information.
    """
    print(_("=== Help ==="))
    print(_("This tool allows you to download YouTube videos and audio files."))
    print()
    print(_("Features:"))
    print(_("- Download videos in MP4 format"))
    print(_("- Download audio only"))
    print(_("- Choose quality and format"))
    print(_("- Multi-language support"))
    print()
    print(_("Usage:"))
    print(_("1. Select 'Download Video/Audio' from the main menu"))
    print(_("2. Enter the YouTube URL"))
    print(_("3. Choose video or audio format"))
    print(_("4. Select quality and start download"))
    print()
    print(_("Files are saved in the 'downloads' folder."))
    print()
    input(_("Press Enter to return to main menu..."))

def change_language():
    """
    Allow user to change the application language.
    """
    global _, current_language
    
    print(_("=== Language Settings ==="))
    print(_("1. English"))
    print(_("2. Japanese"))
    print(_("3. Auto-detect (system default)"))
    
    choice = input(_("Please select language (1-3): "))
    
    if choice == '1':
        _ = setup_language('en')
        print(_("Language changed to English."))
    elif choice == '2':
        _ = setup_language('ja')
        print(_("Language changed to Japanese."))
    elif choice == '3':
        _ = setup_language()
        print(_("Language set to auto-detect."))
    else:
        print(_("Invalid language selection."))
    
    input(_("Press Enter to continue..."))

def download_with_yt_dlp():
    """
    Downloads a YouTube video or audio using yt-dlp, with i18n support.
    """
    url = input(_("Please enter the YouTube video URL to download: "))

    try:
        print(_("\nFetching video information..."))
        ydl_opts_info = {'quiet': True, 'no_warnings': True}
        with yt_dlp.YoutubeDL(ydl_opts_info) as ydl:
            info = ydl.extract_info(url, download=False)
            title = info.get('title', 'N/A')
            uploader = info.get('uploader', 'N/A')
            duration = info.get('duration', 0)
            formats = info.get('formats', [])

        print("\n--------------------------------------------------")
        # Note: Use .format() for translatable strings with variables
        print(_("Title: {}").format(title))
        print(_("Channel: {}").format(uploader))
        print(_("Duration: {} min {} sec").format(duration // 60, duration % 60))
        print("--------------------------------------------------\n")

    except Exception as e:
        print(_("\nError: Failed to fetch video information. Please check if the URL is correct."))
        print(_("Details: {}").format(e))
        return

    mode = input(_("Select download type (1: Video, 2: Audio only): "))

    if mode == '1':
        available_formats = sorted(
            [f for f in formats if f.get('vcodec') != 'none' and f.get('acodec') != 'none' and f.get('ext') == 'mp4'],
            key=lambda f: f.get('height') or 0, reverse=True)
        print(_("\nAvailable video streams (MP4):"))
        if not available_formats:
            print(_("No suitable video streams found."))
            return
            
    elif mode == '2':
        available_formats = sorted(
            [f for f in formats if f.get('acodec') != 'none' and f.get('vcodec') == 'none'],
            key=lambda f: f.get('abr') or 0, reverse=True)
        print(_("\nAvailable audio streams:"))
        if not available_formats:
            print(_("No suitable audio streams found."))
            return
    else:
        print(_("Invalid selection."))
        return

    for i, f in enumerate(available_formats):
        filesize_mb = f.get('filesize') or f.get('filesize_approx')
        filesize_str = f"{filesize_mb / (1024*1024):.2f}MB" if filesize_mb else "N/A"
        
        if mode == '1':
            print(_("{}: Resolution={}, Ext={}, Size={}").format(i+1, f.get('format_note', 'N/A'), f.get('ext'), filesize_str))
        else:
            abr_str = f"{f.get('abr')}kbps" if f.get('abr') is not None else "N/A"
            print(_("{}: Bitrate={}, Format={}, Size={}").format(i+1, abr_str, f.get('ext'), filesize_str))

    try:
        choice = int(input(_("\nEnter the number of the format you want to download: ")))
        selected_format = available_formats[choice - 1]
        format_id = selected_format['format_id']
    except (ValueError, IndexError):
        print(_("Invalid input."))
        return

    print(_("\nStarting download..."))
    save_path = "downloads"
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    
    ydl_opts_download = {
        'format': format_id,
        'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),
        'progress_hooks': [lambda d: print_progress(d)],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts_download) as ydl:
            ydl.download([url])
        print(_("\nDownload completed successfully!"))
    except Exception as e:
        print(_("\nAn error occurred during download: {}").format(e))

def print_progress(d):
    """Callback function to display download progress."""
    if d['status'] == 'downloading':
        percent_str = d.get('_percent_str', '0.0%').strip()
        speed_str = d.get('_speed_str', '0.0KiB/s').strip()
        eta_str = d.get('_eta_str', '00:00').strip()
        # This string is for developers, so it doesn't need translation.
        print(f"\rDownloading... {percent_str} at {speed_str}, ETA {eta_str}", end="")
    elif d['status'] == 'finished':
        filename = d.get('info_dict', {}).get('filename') or d.get('filename')
        if filename:
            print(_("\nFinished processing: '{}'").format(os.path.basename(filename)))

def main_menu():
    """
    Display the main menu and handle user selections.
    """
    while True:
        print("\n" + "="*50)
        print(_("=== YouTube Downloader ==="))
        print(_("1. Download Video/Audio"))
        print(_("2. Help"))
        print(_("3. Language Settings"))
        print(_("4. Exit"))
        print("="*50)
        
        choice = input(_("Please select an option (1-4): "))
        
        if choice == '1':
            download_with_yt_dlp()
        elif choice == '2':
            show_help()
        elif choice == '3':
            change_language()
        elif choice == '4':
            print(_("Thank you for using YouTube Downloader!"))
            break
        else:
            print(_("Invalid option. Please try again."))

if __name__ == "__main__":
    main_menu()