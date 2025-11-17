# streaming_lm_shard.py
import os
import torch
from torch.utils.data import IterableDataset, DataLoader
from datasets import load_dataset
from transformers import AutoTokenizer
import multiprocessing as mp
import sys, time
from datetime import datetime

# ============================================================
# Rolling buffer generator for causal LM fixed-length blocks
# ============================================================
def rolling_token_blocks(token_iter, block_size, pad_token_id):
    """
    Takes an iterator of tokenized sequences and yields fixed-length token blocks.
    Uses a rolling buffer to concatenate sequences until a full block is formed.
    """
    buffer = []
    for tokens in token_iter:
        buffer.extend(tokens)
        while len(buffer) >= block_size:
            chunk = buffer[:block_size]
            buffer = buffer[block_size:]
            yield {
                "input_ids": torch.tensor(chunk, dtype=torch.long),
                "attention_mask": torch.ones(block_size, dtype=torch.long)
            }
    # Pad leftover tokens if any remain
    if buffer:
        padded = buffer + [pad_token_id] * (block_size - len(buffer))
        yield {
            "input_ids": torch.tensor(padded, dtype=torch.long),
            "attention_mask": torch.tensor([1] * len(buffer) + [0] * (block_size - len(buffer)), dtype=torch.long)
        }

# ============================================================
# Manual sharding function
# ============================================================
def manual_shard(dataset_iter, num_shards, process_index):
    for idx, example in enumerate(dataset_iter):
        if idx % num_shards == process_index:
            yield example

# ============================================================
# IterableDataset wrapper for LM
# ============================================================
class LMStreamingDataset(IterableDataset):
    def __init__(self, dataset_iter, tokenizer, block_size):
        self.dataset_iter = dataset_iter
        self.tokenizer = tokenizer
        self.block_size = block_size

    def __iter__(self):
        token_stream = (
            self.tokenizer(ex["text"], add_special_tokens=False)["input_ids"]
            for ex in self.dataset_iter
        )
        yield from rolling_token_blocks(token_stream, self.block_size, self.tokenizer.pad_token_id)

# ============================================================
# Collate function
# ============================================================
def collate_fn(batch):
    return {
        "input_ids": torch.stack([ex["input_ids"] for ex in batch]),
        "attention_mask": torch.stack([ex["attention_mask"] for ex in batch])
    }

# ============================================================
# Worker entry function
# ============================================================

def worker_entry(rank, world_size, model_name, block_size, batch_size, batches_to_show):
    stream_ds = load_dataset("wikitext", "wikitext-2-raw-v1", split="train", streaming=True)
    sharded_iter = manual_shard(stream_ds, world_size, rank)

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    tokenizer.pad_token = tokenizer.eos_token

    lm_dataset = LMStreamingDataset(sharded_iter, tokenizer, block_size)
    loader = DataLoader(lm_dataset, batch_size=batch_size, collate_fn=collate_fn, num_workers=0)

    print(f"{datetime.now()} [PID {os.getpid()} | rank {rank}] starting…", flush=True)
    for i, batch in enumerate(loader):
        print(f"{datetime.now()} [rank {rank}] batch {i} → {batch['input_ids'].shape}", flush=True)
        time.sleep(0.5)  # Slow down so overlap is visible
        if i + 1 >= batches_to_show:
            break
    print(f"{datetime.now()} [rank {rank}] done.", flush=True)


# ============================================================
# Launcher
# ============================================================
def launch_multi_proc(num_procs, model_name, block_size, batch_size, batches_to_show):
    ctx = mp.get_context("spawn")  # Safe for all platforms
    procs = []
    for rank in range(num_procs):
        p = ctx.Process(target=worker_entry, args=(rank, num_procs, model_name, block_size, batch_size, batches_to_show))
        p.start()
        procs.append(p)
    for p in procs:
        p.join()

if __name__ == "__main__":
    launch_multi_proc(
        num_procs=4,  # Number of CPU cores to use
        model_name="gpt2",
        block_size=128,  # Sequence length per sample
        batch_size=4,
        batches_to_show=2
    )
