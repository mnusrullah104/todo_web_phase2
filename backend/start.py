"""
Backend startup script with automatic port fallback.

Tries to start on port 8000, falls back to 8001 if busy.
"""
import uvicorn
import socket
import sys
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def is_port_available(port: int) -> bool:
    """Check if a port is available."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("127.0.0.1", port))
            return True
    except OSError:
        return False


def main():
    """Start the backend server with port fallback."""
    ports = [8000, 8001, 8002, 8003, 8004, 8005]

    for port in ports:
        if is_port_available(port):
            logger.info(f"Starting backend server on port {port}...")
            try:
                uvicorn.run(
                    "src.main:app",
                    host="0.0.0.0",
                    port=port,
                    reload=True,
                    log_level="info"
                )
                return
            except Exception as e:
                logger.error(f"Failed to start on port {port}: {e}")
                continue
        else:
            logger.warning(f"Port {port} is already in use, trying next port...")

    logger.error("Could not start server on any available port (8000-8005)")
    sys.exit(1)


if __name__ == "__main__":
    main()
