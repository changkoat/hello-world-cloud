from book_tracker import app as application

# This file exists to provide an entry point for deployment and to fix the web URL.
# It imports the Flask app defined in book_tracker.py and runs it.

if __name__ == '__main__':
    # Run the application on all network interfaces so it can be accessed remotely
    application.run(host="0.0.0.0", port=8080)
