import os
import time
import threading
import multiprocessing
import asyncio
import argparse
import requests
import aiohttp

IMAGE_FOLDER = './parsing_images/images'


def download_image_sync(url):
    response = requests.get(url)
    if not os.path.exists(IMAGE_FOLDER):
        os.mkdir(IMAGE_FOLDER)
    if response.status_code == 200:
        save_path = os.path.join(IMAGE_FOLDER, os.path.basename(url))
        with open(save_path, "wb") as f:
            f.write(response.content)


async def download_image_async(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if not os.path.exists(IMAGE_FOLDER):
                os.mkdir(IMAGE_FOLDER)
            if response.status == 200:
                save_path = os.path.join(IMAGE_FOLDER, os.path.basename(url))
                with open(save_path, "wb") as f:
                    f.write(await response.read())


async def download_images_asynchronous(urls):
    await asyncio.gather(*(download_image_async(url) for url in urls))


def main():
    parser = argparse.ArgumentParser(description='Скачивание с заданных URL-адресов')
    parser.add_argument('urls', nargs='+', help='')
    args = parser.parse_args()

    start_time = time.time()
    for url in args.urls:
        download_image_sync(url)
    sync_time = time.time() - start_time
    print(f"Синхронный подход, сохранение за: {sync_time:.4f} секунд")

    threads = []
    start_time = time.time()
    for url in args.urls:
        thread = threading.Thread(target=download_image_sync, args=(url,))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
    multithread_time = time.time() - start_time
    print(f"Мультипоточный подход, сохранение за: {multithread_time:.4f} секунд")

    processes = []
    start_time = time.time()
    for url in args.urls:
        process = multiprocessing.Process(target=download_image_sync, args=(url,))
        processes.append(process)
        process.start()
    for process in processes:
        process.join()
    multiprocess_time = time.time() - start_time
    print(f"Мультипроцессорный подход, сохранение за: {multiprocess_time:.4f} секунд")

    tasks = []
    start_time = time.time()

    asyncio.run(download_images_asynchronous(args.urls))
    asynchronous_time = time.time() - start_time
    print(f"Асинхронный подход, сохранение за: {asynchronous_time:.4f} секунд")


if __name__ == '__main__':
    main()
