# from user import activate
import aiohttp
import asyncio
import multiprocessing
import statistics

lock = asyncio.Lock()
counter = 0
open_login_rt = []
sign_up_rt = []
view_course_rt = []
async def sign_up(name , mobile , password , session):

    async with session.post('https://dones.ir/login' , data={'sg_fullname': name ,'sg_mobile' : mobile , 'sg_password' : password}) as response:
        async with lock:
            global counter
            counter+=1
            print(counter)
        return await response.text()

async def open_login_page(session):
    async with session.get('https://dones.ir/login') as response:
        async with lock:
            global counter
            counter+=1
            print(counter)
        return await response.text()

async def view_course(session):

    async with session.get('https://dones.ir/course-info/course_1') as response:
        async with lock:
            global counter
            counter+=1
            print(counter)
        return await response.text()

async def main(i):
   import time
   name = "user"+str(i)
   mobile = "0988791"+str(i).zfill(4)
   password = mobile
   async with aiohttp.ClientSession() as session:

    start = time.perf_counter()
    await open_login_page(session)
    elapsed = time.perf_counter() - start
    open_login_rt.append(elapsed)
    print(f"{i}open_login_page finished in {elapsed:0.2f} seconds")

    start = time.perf_counter()
    await sign_up(name , mobile , password,session)
    elapsed = time.perf_counter() - start
    sign_up_rt.append(elapsed)
    print(f"{i}sign_up finished in {elapsed:0.2f} seconds")

    start = time.perf_counter()
    await view_course(session)
    elapsed = time.perf_counter() - start
    view_course_rt.append(elapsed)
    print(f"{i}view_course finished in {elapsed:0.2f} seconds")

async def start():
 await asyncio.gather(*(main(i) for i in range(5000) ))    

if __name__ == "__main__":
    counter = 0
    asyncio.run(start())
    print(f"open login page avrage responce time is : {statistics.mean(open_login_rt)}")
    print(f"sign up avrage responce time is : {statistics.mean(sign_up_rt)}")
    print(f"view course avrage responce time is : {statistics.mean(view_course_rt)}")
    
