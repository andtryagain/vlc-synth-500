import vlc
import objc
from Cocoa import (
    NSApplication,
    NSWindow,
    NSView,
    NSRect,
    NSPoint,
    NSSize,
    NSBackingStoreBuffered,
    NSObject,
    NSEvent,
)
from PyObjCTools.AppHelper import runEventLoop, stopEventLoop


class WindowDelegate(NSObject):
    def windowWillClose_(self, notification):
        # Stop the VLC player if running
        print("Window is closing...")
        stopEventLoop()  # Stop the event loop


class VideoPlayerApp:
    def __init__(self, video_file):
        self.video_file = video_file
        self.setup_window()
        self.setup_vlc()

    def setup_window(self):
        # Initialize the macOS application
        NSApplication.sharedApplication()

        # Create a macOS window
        origin = NSPoint(100, 100)  # Window's origin
        size = NSSize(800, 600)  # Window's size
        window_frame = NSRect(origin, size)

        self.window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
            window_frame,
            15,  # Titled, closable, resizable
            NSBackingStoreBuffered,
            False,
        )
        self.window.setTitle_("VLC Video Player")
        self.window.makeKeyAndOrderFront_(None)

        # Create an NSView for video output
        content_view = self.window.contentView()
        self.video_view = NSView.alloc().initWithFrame_(content_view.bounds())
        self.video_view.setAutoresizingMask_(18)  # Allow resizing with the window
        content_view.addSubview_(self.video_view)

        # Set up the window delegate to handle the close event
        self.delegate = WindowDelegate.alloc().init()
        self.window.setDelegate_(self.delegate)

        # Monitor key presses
        NSEvent.addLocalMonitorForEventsMatchingMask_handler_(
            1 << 10,  # NSKeyDown
            self.handle_key_press,
        )

    def setup_vlc(self):
        # Initialize VLC
        self.vlc_instance = vlc.Instance(
            # mac m1 pro config where it was all developed
            "--codec=dav1d",
            "--avcodec-hw=none",
            "--avcodec-threads=1",
            "--vout=macosx"
        )
        self.player = self.vlc_instance.media_player_new()

        # Attach the VLC player to the NSView
        # Use objc to convert NSView to a pointer for VLC
        self.player.set_nsobject(objc.pyobjc_id(self.video_view))

    def play_video(self):
        # Set the media file and play
        media = self.vlc_instance.media_new(self.video_file)
        self.player.set_media(media)
        self.player.play()

    def handle_key_press(self, event):
        # Handle key presses to set video positionddddd
        key = event.charactersIgnoringModifiers()
        if key == "a":
            self.set_position(0)  # Set to 0 seconds
        elif key == "s":
            self.set_position(5)  # Set to 5 seconds
        elif key == "d":
            self.set_position(54.7)  # Set to 10 seconds
        return event

    def set_position(self, seconds):
        # Set the video playback position to the specified time
        total_duration = self.player.get_length()
        if total_duration == -1:
            print("No media loaded or player not ready.")
            return

        new_time = min(int(seconds * 1000), total_duration)  # Convert seconds to ms
        print(f"Setting position to: {seconds} seconds")
        self.player.set_time(new_time)


# Run the application
if __name__ == "__main__":
    video_file = "content/example_2.mp4" 
    
    app = VideoPlayerApp(video_file)
    app.play_video()

    runEventLoop()
