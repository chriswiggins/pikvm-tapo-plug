import asyncio
import argparse

from tapo import ApiClient

parser = argparse.ArgumentParser(description='Tapo PiKVM Script')
parser.add_argument('--username', dest='username', help='Tapi API Username', required=True)
parser.add_argument('--password', dest='password', help='Tapi API Password', required=True)
parser.add_argument('--ip', dest='ip', help='Tapo IP Address of P100', required=True)
parser.add_argument('action', choices=['on', 'off', 'toggle', 'status'], help='Action to perform')

async def main():
    args = parser.parse_args()

    def tapo_print(msg):
        print(f"Tapo[{args.ip}]: " + msg)

    client = ApiClient(args.username, args.password)
    device = await client.generic_device(args.ip)

    if args.action == 'off' or args.action == 'toggle':
        tapo_print("Turning device off...")
        await device.off()

    if args.action == 'toggle':
        tapo_print("Waiting 2 seconds...")
        await asyncio.sleep(2)

    if args.action == 'on' or args.action == 'toggle':
        tapo_print("Turning device on...")
        await device.on()


    if args.action == 'status':
        status = await device.get_device_info_json()
        if status['device_on']:
            tapo_print("Device is ON")
            return 0
        else:
            tapo_print("Device is OFF")
            return 1

    return 0

if __name__ == "__main__":
    ret = asyncio.run(main())
    exit(ret)