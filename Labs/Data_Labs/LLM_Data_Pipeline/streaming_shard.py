# save as streaming_shard.py
import os
import torch
from torch.utils.data import IterableDataset, DataLoader
from datasets import load_dataset
from transformers import AutoTokenizer
import multiprocessing as mp

def manual_shard(dataset_iter, num_shards, process_index):
    for idx, example in enumerate(dataset_iter):
        if idx % num_shards == process_index:
            yield example

class TokenizedStreamingIterableDataset(IterableDataset):
    def __init__(self, dataset_iter, tokenizer, max_length):
        self.dataset_iter = dataset_iter
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __iter__(self):
        for ex in self.dataset_iter:
            toks = self.tokenizer(
                ex["text"],
                truncation=True,
                padding="max_length",
                max_length=self.max_length,
                return_tensors="pt",
            )
            yield {
                "input_ids": toks["input_ids"].squeeze(0),
                "attention_mask": toks["attention_mask"].squeeze(0),
                "labels": torch.tensor(ex["label"], dtype=torch.long),
            }

def collate_fn(batch):
    return {
        "input_ids": torch.stack([ex["input_ids"] for ex in batch]),
        "attention_mask": torch.stack([ex["attention_mask"] for ex in batch]),
        "labels": torch.stack([ex["labels"] for ex in batch]),
    }

def worker_entry(rank, world_size, model_name, batch_size, max_length, batches_to_show):
    stream_ds = load_dataset("ag_news", split="train", streaming=True)
    sharded_iter = manual_shard(stream_ds, world_size, rank)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    tokenized_iterable = TokenizedStreamingIterableDataset(sharded_iter, tokenizer, max_length)
    loader = DataLoader(tokenized_iterable, batch_size=batch_size, collate_fn=collate_fn, num_workers=0)
    print(f"[PID {os.getpid()} | rank {rank}] starting…")
    for i, batch in enumerate(loader):
        print(f"[rank {rank}] batch {i} {tuple(batch['input_ids'].shape)}")
        if i + 1 >= batches_to_show:
            break
    print(f"[rank {rank}] done.")

def launch_multi_proc(num_procs, model_name, batch_size, max_length, batches_to_show):
    ctx = mp.get_context("spawn")
    procs = []
    for rank in range(num_procs):
        p = ctx.Process(target=worker_entry, args=(rank, num_procs, model_name, batch_size, max_length, batches_to_show))
        p.start()
        procs.append(p)
    for p in procs:
        p.join()

if __name__ == "__main__":
    launch_multi_proc(num_procs=4,
                      model_name="distilbert-base-uncased",
                      batch_size=8,
                      max_length=128,
                      batches_to_show=2)
