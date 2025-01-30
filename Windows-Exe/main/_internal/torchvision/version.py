__version__ = '0.22.0.dev20250121+cu126'
git_version = '438ae28bde73ebcfb6f8fdc4c60b267f40c2bfa2'
from torchvision.extension import _check_cuda_version
if _check_cuda_version() > 0:
    cuda = _check_cuda_version()
