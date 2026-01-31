# Python 3.13+ Best Practices

## Key Features

- **Type System**: Enhanced with union types (int | str), generic types, and improved type checking
- **Performance**: Improved execution speed and memory efficiency
- **Async Features**: Better async/await handling and improved asyncio

## Standard Libraries

- **typing**: Modern type hints and generics
- **pathlib**: Object-oriented file system paths
- **asyncio**: Asynchronous I/O operations
- **contextlib**: Context managers and cleanup utilities

## Recommended Patterns

### Type Hints
```python
from typing import Union, Optional, List, Dict, Generic, TypeVar

# Use union syntax for multiple types
def process_data(value: int | str) -> bool | None:
    ...

# Use generic types
T = TypeVar('T')
class Container(Generic[T]):
    def __init__(self, value: T) -> None:
        self.value = value
```

### Async Programming
```python
import asyncio
from typing import Awaitable

async def async_operation(data: str) -> str:
    await asyncio.sleep(1)  # Simulate async work
    return f"Processed: {data}"

async def main() -> None:
    result = await async_operation("test")
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

## Error Handling
- Use specific exception types
- Implement proper logging
- Follow fail-fast principles
- Handle edge cases gracefully