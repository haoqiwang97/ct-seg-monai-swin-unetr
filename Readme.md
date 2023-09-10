This is a test file. Haoqi test

```zsh
monai-deploy package ct-seg-monai-swin-unetr \
--base nvcr.io/nvidia/pytorch:22.08-py3 \
--model ct-seg-monai-swin-unetr/best_metric_model.pt \
--tag flywheel/ct-seg-monai-swin-unetr:0.1.0
```

```zsh
monai-deploy package -b nvcr.io/nvidia/pytorch:23.07-py3 /Users/haoqiwang/Documents/ct-seg-monai-swin-unetr --tag flywheel/ct-seg-monai-swin-unetr-cpu:0.1.6 -m /Users/haoqiwang/Documents/ct-seg-monai-swin-unetr/best_metric_model.ts 
```