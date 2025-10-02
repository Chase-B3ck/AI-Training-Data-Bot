import json
from pathlib import Path
from typing import Union
from ..models import Dataset, ExportFormat
from ..core.logging import get_logger

class DatasetExporter:
    def __init__(self):
        self.logger = get_logger("dataset_exporter")

    async def export(self, dataset: Dataset, output_path: Union[str, Path], format: ExportFormat = ExportFormat.JSONL, split_data: bool = True):
        out = Path(output_path)
        out.parent.mkdir(parents=True, exist_ok=True)

        self.logger.info(f"Exporting dataset '{dataset.name}' with {dataset.total_examples} examples to {out} as {format.name}")

        if format == ExportFormat.JSONL:
            await self._export_jsonl(dataset, out)
        else:
            raise ValueError(f"Unsupported export format: {format}")

    async def _export_jsonl(self, dataset: Dataset, out: Path):
        with out.open('w', encoding='utf-8') as f:
            for ex in dataset.examples:
                obj = {
                    'id': str(ex.id),
                    'input_text': ex.input_text,
                    'output_text': ex.output_text,
                    'task_type': ex.task_type,
                    'source_document_id': str(ex.source_document_id) if ex.source_document_id else None,
                    'quality_scores': ex.quality_scores,
                }
                f.write(json.dumps(obj, ensure_ascii=False) + '\n')

        self.logger.info(f"Dataset successfully exported to {out}")
