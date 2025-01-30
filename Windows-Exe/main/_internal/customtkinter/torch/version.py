from typing import Optional

__all__ = ['__version__', 'debug', 'cuda', 'git_version', 'hip']
__version__ = '2.7.0.dev20250120+cu126'
debug = False
cuda: Optional[str] = '12.6'
git_version = '37626ee0e6ff5dc1d38664690bd2ff6c790aab0c'
hip: Optional[str] = None
xpu: Optional[str] = None
