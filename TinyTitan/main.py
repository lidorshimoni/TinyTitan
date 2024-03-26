from TinyTitan import TinyTitan
import logging

logger = logging.Logger(__name__)

UART_SERVICE_UUID = "6e400001-b5a3-f393-e0a9-e50e24dcca9e"
UART_RX_CHAR_UUID = "6e400002-b5a3-f393-e0a9-e50e24dcca9e"
UART_TX_CHAR_UUID = "6e400003-b5a3-f393-e0a9-e50e24dcca9e"
mac_address = "88:22:B2:F4:5C:32"

def main():
    if not TinyTitan.is_connected():
        logger.warning("TinyTitan not connected!")
    titan = TinyTitan()
    titan.open(bluetooth=True, mac_address=mac_address, uart_uuid=UART_SERVICE_UUID, tx_uuid=UART_TX_CHAR_UUID, rx_uuid=UART_RX_CHAR_UUID)
    titan.heartbeat()
    titan.neutralize()
    titan.perform_animation("neutralize")
    titan.perform_animation("squat")
    titan.perform_animation("jitter")


if __name__ == "__main__":
    main()