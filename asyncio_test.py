import asyncio
import random

rain_q = asyncio.Queue()      # ***
speed_q = asyncio.Queue()     # ***

async def speed_forever():
    while True:
        speed = random.randint(1,100)
        print("Speed mesuring ......", speed)
        await speed_q.put(speed)                 # ***
        await asyncio.sleep(1)

async def rain_forever():
    while True:
        rain = random.random()
        print("Rain mesuring .......", rain)
        await rain_q.put(rain)                   # ***
        await asyncio.sleep(0.1)


async def main():
    asyncio.ensure_future(speed_forever())  # fire and forget
    asyncio.ensure_future(rain_forever())  # fire and forget

    while True:
        print("*" * 40)

        # *** - get data from the queues 
        while not rain_q.empty(): 
            rain = await rain_q.get()
            print(f"Rain was {rain}")
        while not speed_q.empty(): 
            speed = await speed_q.get()
            print(f"Speed was {speed}")


        print("Sending Data.....")    #Here I'd like to get access to rain and speed variable by using a queue
        print("*" * 40)
        await asyncio.sleep(5)
     

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
