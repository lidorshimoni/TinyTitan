from TinyTitanApi.TinyTitan import TinyTitan
import logging

logger = logging.Logger(__name__)

def main():
    if not TinyTitan.is_connected():
        logger.warning("TinyTitan not connected!")
    titan = TinyTitan(should_open_device=False)
    print(titan.animations)
    print(titan.poses)
    print(titan.limbs)
    # titan.neutralize()
    # for i in range(100):
        # titan.jitter()



if __name__ == "__main__":
    # main()
    import asyncio
    from bleak import BleakClient, BleakScanner
    import time
    address = "88:22:B2:F4:5C:32"
    # MODEL_NBR_UUID = "2A24"

    async def main(address):
        # devices = await BleakScanner.discover()
        # for d in devices:
        #     if d.address = address:
                
    #         print(d)
    #     return
        async with BleakClient(address) as client:
            for service in client.services:
                print(service)
            # time.sleep(4)
        # model_number = await client.read_gatt_char(MODEL_NBR_UUID)
        # print("Model Number: {0}".format("".join(map(chr, model_number))))

    asyncio.run(main(address))