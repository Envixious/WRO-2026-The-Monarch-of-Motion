import asyncio
import os
import pickle
import signal
import sys
import time
from typing import Optional

from rplidarc1 import RPLidar


DATA_PATH = os.environ.get("LIDAR_DATA_PATH", "/dev/shm/lidar.data")


def cleanup_lidar(lidar: Optional[object]) -> None:
    """Stop the LiDAR cleanly so it can be re-started without stale state."""
    if lidar is None:
        return

    for method_name in ("reset", "shutdown"):
        method = getattr(lidar, method_name, None)
        if callable(method):
            try:
                method()
            except Exception:
                pass


async def queue_process(q: asyncio.Queue, event: asyncio.Event, output_path: str = DATA_PATH):
    """Process LiDAR queue and write snapshot to disk with throttled writes.
    
    Writes are batched and throttled to every 100ms to reduce disk I/O pressure.
    """
    data = {}
    last_write_time = time.time()
    write_interval = 0.1  # Write only every 100ms (max 10 writes/sec)
    
    while not event.is_set():
        while q.qsize() > 10:
            out = await q.get()
            if out.get("q") != 0:
                data[int(out["a_deg"])] = out["d_mm"]
                
                # Throttle disk writes: only write if interval has elapsed
                now = time.time()
                if now - last_write_time >= write_interval:
                    try:
                        os.makedirs(os.path.dirname(output_path), exist_ok=True)
                    except OSError:
                        pass
                    try:
                        with open(output_path, "wb") as handle:
                            pickle.dump(data, handle)
                        last_write_time = now
                    except Exception:
                        pass  # Silently skip write errors
        
        await asyncio.sleep(0.05)  # Reduce CPU spinning


async def main(lidar: RPLidar):
    stop_event = getattr(lidar, "stop_event", None)
    if stop_event is None:
        stop_event = asyncio.Event()
        setattr(lidar, "stop_event", stop_event)

    async with asyncio.TaskGroup() as tg:
        tg.create_task(queue_process(lidar.output_queue, stop_event))
        tg.create_task(lidar.simple_scan())

    cleanup_lidar(lidar)


if __name__ == "__main__":
    lidar = None
    try:
        lidar = RPLidar("/dev/ttyUSB0", 460800)
        asyncio.run(main(lidar))
    except KeyboardInterrupt:
        cleanup_lidar(lidar)
    except Exception:
        cleanup_lidar(lidar)
    finally:
        cleanup_lidar(lidar)
        sys.exit(0)