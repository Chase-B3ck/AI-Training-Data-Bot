import httpx
from bs4 import BeautifulSoup
from typing import Optional
from ..core.logging import get_logger

class DecodoClient:
    def __init__(self, timeout: float = 30.0):
        self.timeout = timeout
        self.logger = get_logger("decodo_client")

    async def fetch(self, url: str) -> Optional[str]:
        if not url.startswith(('http://', 'https://')):
            self.logger.warning(f"Invalid URL: {url}")
            return None

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(url)
                response.raise_for_status()
                self.logger.info(f"Fetched content from {url}")
                return self._extract_text(response.text)
        except Exception as e:
            self.logger.error(f"Failed to fetch {url}: {e}")
            return None

    def _extract_text(self, html: str) -> str:
        try:
            soup = BeautifulSoup(html, 'html.parser')
            for tag in soup(["script", "style"]):
                tag.decompose()
            text = soup.get_text()
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split(" "))
            return ' '.join(chunk for chunk in chunks if chunk)
        except Exception as e:
            self.logger.error(f"Failed to extract text: {e}")
            return html

