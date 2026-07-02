import threading
import time
import queue

class TaskScheduler:
    """
    A simple threaded task scheduler that executes functions from a queue.
    """
    def __init__(self, num_workers=2):
        self.task_queue = queue.Queue()
        self.num_workers = num_workers
        self.workers = []
        self._stop_event = threading.Event()

    def worker_loop(self, worker_id):
        while not self._stop_event.is_set():
            try:
                task_data = self.task_queue.get(timeout=1)
                task, args, kwargs = task_data
                print(f"[Worker {worker_id}] Starting task: {task.__name__}")
                try:
                    task(*args, **kwargs)
                except Exception as e:
                    print(f"[Worker {worker_id}] Error in task {task.__name__}: {e}")
                finally:
                    self.task_queue.task_done()
                    print(f"[Worker {worker_id}] Finished task: {task.__name__}")
            except queue.Empty:
                continue

    def start(self):
        print(f"Starting scheduler with {self.num_workers} workers...")
        for i in range(self.num_workers):
            t = threading.Thread(target=self.worker_loop, args=(i,))
            t.daemon = True
            t.start()
            self.workers.append(t)

    def stop(self):
        self._stop_event.set()
        for t in self.workers:
            t.join()
        print("Scheduler stopped.")

    def add_task(self, func, *args, **kwargs):
        self.task_queue.put((func, args, kwargs))

def sample_task(name, duration):
    time.sleep(duration)
    print(f"Task '{name}' completed after {duration} seconds.")

if __name__ == "__main__":
    scheduler = TaskScheduler(num_workers=3)
    scheduler.start()

    scheduler.add_task(sample_task, "Task A", 2)
    scheduler.add_task(sample_task, "Task B", 1)
    scheduler.add_task(sample_task, "Task C", 3)
    scheduler.add_task(sample_task, "Task D", 1)

    print("All tasks added to queue. Waiting for completion...")
    scheduler.task_queue.join()
    scheduler.stop()
    print("All done.")
