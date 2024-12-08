import objc
from Cocoa import (
    NSApplication,
    NSWindow,
    NSColor,
    NSBezierPath,
    NSView,
    NSRect,
    NSPoint,
    NSSize,
    NSBackingStoreBuffered,
)
from PyObjCTools.AppHelper import runEventLoop


# class MinimalView(NSView):
#     def init(self):
#         self = objc.super(MinimalView, self).init()
#         if self is None:
#             return None
#         return self

#     def drawRect_(self, rect):
#         """Draw a simple rectangle."""
#         NSColor.blueColor().set()
#         NSBezierPath.fillRect(self.bounds())

class KeyboardView(NSView):
    def init(self):
        """Initialize the KeyboardView."""
        self = objc.super(KeyboardView, self).init()
        if self is None:
            return None
        self.pressed_keys = set()  # Track pressed keys
        self.key_to_index = {
            "a": 0,  # C
            "s": 1,  # D
            "d": 2,  # E
            "f": 3,  # F
            "g": 4,  # G
            "h": 5,  # A
            "j": 6,  # B
        }
        self.black_keys = {0: 0, 1: 1, 3: 2, 4: 3, 5: 4}  # Black key positions
        return self

    def drawRect_(self, rect):
        """Draw the keyboard."""
        self.draw_white_keys()
        self.draw_black_keys()

    def draw_white_keys(self):
        """Draw 7 white keys (C to B)."""
        key_width = self.bounds().size.width / 7
        key_height = self.bounds().size.height

        for i in range(7):
            rect = NSRect(
                NSPoint(i * key_width, 0),
                NSSize(key_width, key_height),
            )
            color = (
                NSColor.redColor() if i in self.pressed_keys else NSColor.whiteColor()
            )
            color.set()
            NSBezierPath.fillRect(rect)

            # Draw key borders
            NSColor.blackColor().set()
            NSBezierPath.strokeRect(rect)

class MinimalApp:
    def __init__(self):
        self.setup_window()

    def setup_window(self):
        # Initialize macOS application
        NSApplication.sharedApplication()

        # Create the main application window
        window_frame = NSRect(NSPoint(800, 100), NSSize(700, 300))
        self.window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
            window_frame, 
            15,
            NSBackingStoreBuffered,
            False
        )

        self.window.setTitle_("keyboard")
        self.window.makeKeyAndOrderFront_(None)

        # Create a minimal view
        self.view = KeyboardView.alloc().initWithFrame_(self.window.contentView().bounds())
        # self.view.setAutoresizingMask_(18)  # Allow resizing
        self.window.contentView().addSubview_(self.view)


if __name__ == "__main__":
    app = MinimalApp()
    runEventLoop()
