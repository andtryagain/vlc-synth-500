import objc
from Cocoa import (
    NSApplication, NSWindow, NSView, NSRect, NSPoint, NSSize,
    NSBackingStoreBuffered, NSColor, NSBezierPath
)
from PyObjCTools.AppHelper import runEventLoop


class GeometryApp:
    def __init__(self):
        self.setup_window()

    def setup_window(self):
        # Initialize macOS application
        NSApplication.sharedApplication()

        # Create the main application window
        window_frame = NSRect(NSPoint(100, 100), NSSize(400, 300))
        self.window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
            window_frame,
            15,  # Titled, closable, resizable
            NSBackingStoreBuffered,
            False
        )
        self.window.setTitle_("Geometry Example")
        self.window.makeKeyAndOrderFront_(None)

        # Set up the main content view
        self.content_view = self.window.contentView()

        # Draw geometric shapes
        self.draw_rectangle(NSRect(NSPoint(50, 50), NSSize(100, 100)))
        self.draw_circle(NSRect(NSPoint(200, 50), NSSize(100, 100)))

    def draw_rectangle(self, rect):
        shape_view = NSView.alloc().initWithFrame_(rect)
        shape_view.setWantsLayer_(True)
        shape_view.layer().setBackgroundColor_(NSColor.redColor().CGColor())
        self.content_view.addSubview_(shape_view)

    def draw_circle(self, rect):
        shape_view = NSView.alloc().initWithFrame_(rect)
        shape_view.setWantsLayer_(True)
        path = NSBezierPath.bezierPathWithOvalInRect_(rect)

        layer = shape_view.layer()
        layer.setBackgroundColor_(NSColor.clearColor().CGColor())
        layer.setMasksToBounds_(True)

        # Create a custom drawing
        shape_view.setWantsLayer_(True)
        shape_layer = shape_view.layer()
        shape_layer.setBackgroundColor_(NSColor.blueColor().CGColor())
        self.content_view.addSubview_(shape_view)


if __name__ == "__main__":
    app = GeometryApp()
    runEventLoop()