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

    rain = None       # *** 
    speed = None      # ***
    while True:
        print("*" * 40)

        # *** Read stuff from the queues. Here, I'm just using the latest
        # item in the queue - but one can do other things as well. 
        while not rain_q.empty(): 
            rain = await rain_q.get()
        
        while not speed_q.empty(): 
            speed = await speed_q.get()

        print(f"*** Last rain was {rain}")            
        print(f"*** Last speed was {speed}")
        print("Sending Data.....")    #Here I'd like to get access to rain and speed variable by using a queue
        print("*" * 40)
        await asyncio.sleep(5)

     

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())