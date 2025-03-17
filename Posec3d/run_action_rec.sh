python demo/demo_skeleton.py \
../train_data/010.mp4 \
../result_dir/test_010.mp4 \
--config configs/skeleton/posec3d/slowonly_r50_8xb32-u48-240e_k400-keypoint_.py \
--checkpoint ../best_acc_top1_epoch_89.pth \
--label-map ../labels.txt


