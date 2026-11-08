# import asyncio
# from collections import defaultdict
# import pandas as pd
# from config.settings import QUEUE_MAX_SIZE, BATCH_SIZE, WORKER_SLEEP_INTERVAL
# from repository.inventory_repository import InventoryRepository
# from repository.movement_repository import MovementRepository

# class InventoryService:
#     def __init__(self):
#         self.inv_repo = InventoryRepository()
#         self.mov_repo = MovementRepository()
#         self.queue = asyncio.Queue(maxsize=QUEUE_MAX_SIZE)
#         self.product_locks = defaultdict(asyncio.Lock)
#         self._worker_task = None

#     async def start_worker(self):
#         if self._worker_task is None or self._worker_task.done():
#             self._worker_task = asyncio.create_task(self._process_queue())

#     async def add_movement(self, product_id: str, warehouse_id: str, delta: int):
#         async with self.product_locks[product_id]:
#             await self.queue.put((product_id, warehouse_id, delta))

#     async def _process_queue(self):
#         while True:
#             batch = []
#             try:
#                 item = await self.queue.get()
#                 batch.append(item)
#                 while len(batch) < BATCH_SIZE:
#                     batch.append(self.queue.get_nowait())
#             except asyncio.QueueEmpty:
#                 pass

#             if batch:
#                 try:
#                     applied = await self.inv_repo.update_batch(batch)
#                     if applied < len(batch):
#                         for prod, wh, delta in batch:
#                             current = await self.inv_repo.get_stock(prod, wh)
#                             if current is None or (current + delta) < 0:
#                                 await self.mov_repo.log_rejection(
#                                     prod, wh, delta, "Stock insuficiente o SKU inexistente"
#                                 )
#                 except Exception as e:
#                     print(f"Error procesando lote: {e}")
#                 finally:
#                     for _ in batch:
#                         self.queue.task_done()

#             await asyncio.sleep(WORKER_SLEEP_INTERVAL)

#     async def get_inventory_df(self) -> pd.DataFrame:
#         return await self.inv_repo.fetch_all()


import pandas as pd
from repository.inventory_repository import InventoryRepository
from repository.movement_repository import MovementRepository

class InventoryService:
    def __init__(self):
        self.inv_repo = InventoryRepository()
        self.mov_repo = MovementRepository()

    def process_movement(self, product_id: str, warehouse_id: str, delta: int) -> bool:
        success = self.inv_repo.update_stock(product_id, warehouse_id, delta)
        if not success:
            self.mov_repo.log_rejection(
                product_id, warehouse_id, delta, "Stock insuficiente o SKU inexistente"
            )
        return success

    def get_inventory_df(self) -> pd.DataFrame:
        return self.inv_repo.fetch_all()