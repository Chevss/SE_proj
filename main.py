from win32 import win32print
import os

# From user made modules
import shared_state
from user_logs import log_actions

def create_receipt():
    receipt_text = """
    ---------------------------------
           Receipt Example
    ---------------------------------
    Date: 2024-06-24
    Time: 10:00 AM
    Amount: $50.00
    Payment Method: Cash
    Thank you for your purchase!
    ---------------------------------
    """

    return receipt_text

def print_receipt(printer_name):
    receipt = create_receipt()

    # Get the default printer handle
    printer_handle = win32print.OpenPrinter(printer_name)

    # Start a print job
    job = win32print.StartDocPrinter(printer_handle, 1, (os.path.basename("receipt.txt"), None, "RAW"))

    # Write the receipt text to the printer
    win32print.StartPagePrinter(printer_handle)
    win32print.WritePrinter(printer_handle, receipt.encode())

    # End the print job
    win32print.EndPagePrinter(printer_handle)
    win32print.EndDocPrinter(printer_handle)

    print(f"Receipt printed to {printer_name}.")
    action = "Printed a receipt."
    log_actions(shared_state.current_user, action)

if __name__ == "__main__":
    # Specify the printer name here (you may retrieve it from the user or a configuration)
    printer_name = "XP-58C"

    # Print the receipt
    print_receipt(printer_name)
