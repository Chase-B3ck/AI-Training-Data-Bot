import asyncio
from ai_training_data_bot.bot import TrainingDataBot
from ai_training_data_bot.storage.dataset_exporter import DatasetExporter
from ai_training_data_bot.models import ExportFormat
from pathlib import Path
import logging

async def run_example():
    logging.basicConfig(level=logging.INFO)
    bot = TrainingDataBot()

    sample_dir = Path('samples')
    sample_dir.mkdir(exist_ok=True)

    # Load documents
    documents = await bot.load_documents([str(sample_dir)])
    if not documents:
        print("No documents found in 'samples' directory.")
        return

    # Process documents into dataset
    dataset = await bot.process_documents(documents)
    if not dataset.examples:
        print("No training examples generated.")
        return

    # Export dataset
    out = Path('output')
    out.mkdir(exist_ok=True)
    exporter = DatasetExporter()
    await exporter.export(dataset, out / 'training_data.jsonl', format=ExportFormat.JSONL)

    print(f" Export complete: {out / 'training_data.jsonl'}")

if __name__ == "__main__":
    asyncio.run(run_example())
